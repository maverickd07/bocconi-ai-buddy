"""Bocconi AI Buddy - backend entry point.

Implements the RAG pipeline over the bundled Bocconi and Open Data and
exposes a single POST /ask endpoint. See AGENTS.md for the full spec.
"""

from __future__ import annotations

import json
import logging
import os
import re
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import faiss
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import APIConnectionError, APIError, APITimeoutError, OpenAI, RateLimitError
from pydantic import BaseModel, Field

load_dotenv()
logger = logging.getLogger("bocconi-buddy")

app = FastAPI(title="Bocconi AI Buddy")

# CORS: allow the deployed frontend (and localhost during dev) to call /ask.
# Set FRONTEND_URL on Railway to your frontend service's public URL,
# e.g. https://buddy-frontend-yourname.up.railway.app
_allowed = [
    o.strip()
    for o in (os.environ.get("FRONTEND_URL") or "*").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed or ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


Verticale = Literal[
    "relocation",
    "life_on_campus",
    "study_abroad",
    "career_readiness",
]

VERTICALS: tuple[Verticale, ...] = (
    "relocation",
    "life_on_campus",
    "study_abroad",
    "career_readiness",
)

FALLBACK_ANSWER = "I don't have this information in the available data"
EMBEDDING_MODEL = "text-embedding-3-large"
ANSWER_MODEL = "gpt-4o-mini"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MANIFEST_PATH = DATA_DIR / "manifest.json"
INDEX_DIR = DATA_DIR / "index" / "faiss_text-embedding-3-large"
INDEX_PATH = INDEX_DIR / "index.faiss"
CHUNKS_PATH = INDEX_DIR / "chunks.jsonl"
STATE_PATH = INDEX_DIR / "state.json"

CHUNK_WORDS = 420
CHUNK_OVERLAP = 70
EMBED_BATCH_SIZE = 64
PRESELECT_K = 350
TOP_K_PER_VERTICAL = 6

MIN_VERTICAL_SCORE = 0.20
MIN_VERTICAL_MARGIN = 0.015
MIN_ANSWER_SCORE = 0.24

RETRYABLE_EXCEPTIONS = (RateLimitError, APIError, APIConnectionError, APITimeoutError)


@dataclass(slots=True)
class ChunkRecord:
    text: str
    source: str
    verticale: Verticale


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    verticale: Verticale


class KnowledgeBase:
    """Loads or builds the local FAISS index and executes semantic search."""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.loaded = False
        self.index: faiss.Index | None = None
        self.chunks: list[ChunkRecord] = []
        self.client: OpenAI | None = None

    def ensure_loaded(self) -> None:
        if self.loaded:
            return

        with self.lock:
            if self.loaded:
                return

            self.client = OpenAI(timeout=20.0, max_retries=0)
            if INDEX_PATH.exists() and CHUNKS_PATH.exists():
                self._load_index_from_disk()
            else:
                self._build_index_from_data()
            self.loaded = True

    def _load_index_from_disk(self) -> None:
        self.index = faiss.read_index(str(INDEX_PATH))
        self.chunks = []

        with CHUNKS_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw:
                    continue
                item = json.loads(raw)
                self.chunks.append(
                    ChunkRecord(
                        text=item["text"],
                        source=item["source"],
                        verticale=item["verticale"],
                    )
                )

        if self.index.ntotal != len(self.chunks):
            raise RuntimeError(
                "FAISS index and chunk metadata are inconsistent. Delete "
                "backend/data/index/faiss_text-embedding-3-large and retry."
            )

    def _build_index_from_data(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        file_entries: list[dict[str, str]] = manifest["files"]

        all_chunks: list[ChunkRecord] = []
        for entry in file_entries:
            rel_path = entry.get("path")
            verticale = entry.get("verticale")
            if not rel_path or verticale not in VERTICALS:
                continue

            file_path = DATA_DIR / rel_path
            if not file_path.exists():
                continue

            raw = file_path.read_text(encoding="utf-8", errors="ignore")
            cleaned = _clean_markdown(raw)
            for chunk_text in _chunk_text(cleaned):
                all_chunks.append(
                    ChunkRecord(
                        text=chunk_text,
                        source=f"data/{rel_path}",
                        verticale=verticale,
                    )
                )

        if not all_chunks:
            raise RuntimeError("No chunks found while building FAISS index.")

        vectors: list[list[float]] = []
        for start in range(0, len(all_chunks), EMBED_BATCH_SIZE):
            batch = all_chunks[start : start + EMBED_BATCH_SIZE]
            embeddings = _embed_texts(self.client, [c.text for c in batch])
            vectors.extend(embeddings)

        matrix = np.asarray(vectors, dtype=np.float32)
        _normalize(matrix)

        index = faiss.IndexFlatIP(matrix.shape[1])
        index.add(matrix)

        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        faiss.write_index(index, str(INDEX_PATH))

        with CHUNKS_PATH.open("w", encoding="utf-8") as f:
            for chunk in all_chunks:
                f.write(
                    json.dumps(
                        {
                            "text": chunk.text,
                            "source": chunk.source,
                            "verticale": chunk.verticale,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )

        STATE_PATH.write_text(
            json.dumps(
                {
                    "embedding_model": EMBEDDING_MODEL,
                    "answer_model": ANSWER_MODEL,
                    "chunks": len(all_chunks),
                    "built_at_epoch": int(time.time()),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        self.index = index
        self.chunks = all_chunks

    def search(self, question: str, k: int) -> tuple[np.ndarray, np.ndarray]:
        if not self.index or not self.chunks:
            raise RuntimeError("Knowledge base not loaded.")

        query = np.asarray(_embed_texts(self.client, [question])[0], dtype=np.float32).reshape(
            1, -1
        )
        _normalize(query)
        scores, indices = self.index.search(query, k)
        return scores[0], indices[0]


kb = KnowledgeBase()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    question = request.question.strip()
    if not question:
        return AskResponse(
            answer=FALLBACK_ANSWER,
            sources=[],
            verticale="life_on_campus",
        )

    keyword_verticale = _keyword_verticale(question)

    try:
        kb.ensure_loaded()
    except Exception as exc:
        logger.exception("Failed to load or build knowledge base: %s", exc)
        return AskResponse(
            answer=FALLBACK_ANSWER,
            sources=[],
            verticale=keyword_verticale or "life_on_campus",
        )

    try:
        k = min(PRESELECT_K, len(kb.chunks))
        scores, indices = kb.search(question=question, k=k)
    except Exception as exc:
        logger.exception("Vector search failed: %s", exc)
        return AskResponse(
            answer=FALLBACK_ANSWER,
            sources=[],
            verticale=keyword_verticale or "life_on_campus",
        )

    verticale, margin, candidates = _detect_and_filter_verticale(
        scores=scores,
        indices=indices,
        chunks=kb.chunks,
        keyword_verticale=keyword_verticale,
    )

    if not candidates:
        return AskResponse(answer=FALLBACK_ANSWER, sources=[], verticale=verticale)

    top_score = candidates[0][0]
    if margin < MIN_VERTICAL_MARGIN or top_score < MIN_ANSWER_SCORE:
        return AskResponse(
            answer=FALLBACK_ANSWER,
            sources=_sources_from_candidates(candidates),
            verticale=verticale,
        )

    context_blocks = []
    for i, (score, chunk) in enumerate(candidates, start=1):
        context_blocks.append(f"[{i}] source={chunk.source} score={score:.3f}\n{chunk.text}")
    context = "\n\n".join(context_blocks)

    system_prompt = (
        "You are Bocconi AI Buddy. Answer only with facts grounded in the provided "
        "context snippets. If context is insufficient, contradictory, or does not "
        f"contain the answer, return exactly: \"{FALLBACK_ANSWER}\". "
        "Do not fabricate details and do not add invented facts."
    )
    user_prompt = (
        f"Question:\n{question}\n\n"
        f"Detected verticale: {verticale}\n\n"
        f"Context snippets:\n{context}\n\n"
        "Write a concise and helpful answer in the same language as the question."
    )

    try:
        answer = _generate_answer(kb.client, system_prompt=system_prompt, user_prompt=user_prompt)
    except Exception as exc:
        logger.exception("LLM generation failed: %s", exc)
        return AskResponse(
            answer=FALLBACK_ANSWER,
            sources=_sources_from_candidates(candidates),
            verticale=verticale,
        )

    if not answer or _looks_like_abstention(answer):
        answer = FALLBACK_ANSWER

    return AskResponse(
        answer=answer,
        sources=_sources_from_candidates(candidates),
        verticale=verticale,
    )


def _with_retries(func):
    delay = 1.0
    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            return func()
        except RETRYABLE_EXCEPTIONS as exc:
            last_exc = exc
            if attempt == 2:
                break
            time.sleep(delay)
            delay = min(delay * 2.0, 8.0)
    if last_exc:
        raise last_exc
    raise RuntimeError("Unknown retry failure")


def _embed_texts(client: OpenAI | None, texts: list[str]) -> list[list[float]]:
    if client is None:
        raise RuntimeError("OpenAI client is not initialized.")
    cleaned = [t.strip() if t.strip() else " " for t in texts]

    def _call():
        response = client.with_options(timeout=20.0).embeddings.create(
            model=EMBEDDING_MODEL,
            input=cleaned,
        )
        return [row.embedding for row in response.data]

    return _with_retries(_call)


def _generate_answer(client: OpenAI | None, *, system_prompt: str, user_prompt: str) -> str:
    if client is None:
        raise RuntimeError("OpenAI client is not initialized.")

    def _call():
        response = client.with_options(timeout=22.0).chat.completions.create(
            model=ANSWER_MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return (response.choices[0].message.content or "").strip()

    return _with_retries(_call)


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5 :]
    return text


def _clean_markdown(text: str) -> str:
    body = _strip_frontmatter(text)
    body = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"`{1,3}", "", body)
    body = re.sub(r"\s+", " ", body)
    return body.strip()


def _chunk_text(text: str) -> list[str]:
    words = text.split()
    if len(words) < 50:
        return []

    step = CHUNK_WORDS - CHUNK_OVERLAP
    chunks: list[str] = []
    for i in range(0, len(words), step):
        part = words[i : i + CHUNK_WORDS]
        if len(part) < 90:
            continue
        chunks.append(" ".join(part))
    return chunks


def _normalize(matrix: np.ndarray) -> None:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    matrix /= norms


def _keyword_verticale(question: str) -> Verticale | None:
    q = question.lower()
    rules: dict[Verticale, tuple[str, ...]] = {
        "relocation": (
            "housing",
            "accommodation",
            "rent",
            "milan",
            "metro",
            "bus",
            "transport",
            "commute",
            "residence",
            "visa",
            "permesso",
            "alloggio",
            "affitto",
        ),
        "life_on_campus": (
            "campus",
            "event",
            "association",
            "club",
            "well-being",
            "wellbeing",
            "inclusion",
            "library",
            "sport",
            "student life",
        ),
        "study_abroad": (
            "exchange",
            "erasmus",
            "double degree",
            "abroad",
            "international",
            "partner university",
            "study abroad",
            "overseas",
        ),
        "career_readiness": (
            "career",
            "internship",
            "cv",
            "resume",
            "job",
            "placement",
            "salary",
            "employment",
            "recruiting",
            "interview",
        ),
    }

    scores: dict[Verticale, int] = {v: 0 for v in VERTICALS}
    for verticale, words in rules.items():
        for w in words:
            if w in q:
                scores[verticale] += 1

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return None
    return best


def _detect_and_filter_verticale(
    *,
    scores: np.ndarray,
    indices: np.ndarray,
    chunks: list[ChunkRecord],
    keyword_verticale: Verticale | None,
) -> tuple[Verticale, float, list[tuple[float, ChunkRecord]]]:
    grouped: dict[Verticale, list[tuple[float, ChunkRecord]]] = {v: [] for v in VERTICALS}
    for score, idx in zip(scores, indices):
        if idx < 0:
            continue
        chunk = chunks[int(idx)]
        grouped[chunk.verticale].append((float(score), chunk))

    vertical_scores: dict[Verticale, float] = {}
    for verticale, items in grouped.items():
        if not items:
            vertical_scores[verticale] = -1.0
            continue
        local_top = items[0][0]
        local_avg = float(np.mean([s for s, _ in items[:4]]))
        mix = 0.75 * local_top + 0.25 * local_avg
        if keyword_verticale == verticale:
            mix += 0.03
        vertical_scores[verticale] = mix

    ranked = sorted(vertical_scores.items(), key=lambda kv: kv[1], reverse=True)
    best_verticale, best_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else -1.0
    margin = best_score - second_score

    if best_score < MIN_VERTICAL_SCORE and keyword_verticale:
        best_verticale = keyword_verticale
        margin = MIN_VERTICAL_MARGIN

    selected = grouped[best_verticale][:TOP_K_PER_VERTICAL]
    selected = [item for item in selected if item[0] >= max(MIN_ANSWER_SCORE - 0.06, 0.12)]
    return best_verticale, margin, selected


def _sources_from_candidates(candidates: list[tuple[float, ChunkRecord]]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for _, chunk in candidates:
        if chunk.source in seen:
            continue
        seen.add(chunk.source)
        out.append(chunk.source)
    return out


def _looks_like_abstention(answer: str) -> bool:
    a = answer.strip().lower()
    if not a:
        return True
    markers = (
        "i don't know",
        "i do not know",
        "not enough information",
        "insufficient information",
        "cannot answer",
        "can't answer",
        "no information",
        FALLBACK_ANSWER.lower(),
    )
    return any(marker in a for marker in markers)
