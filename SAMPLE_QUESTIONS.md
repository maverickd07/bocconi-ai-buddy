# Sample evaluation questions (10)

These 10 questions are **representative of the 80** that the automated evaluator will hit your `/ask` endpoint with on the day of the hackathon. They mirror the real eval set on three axes:

- **Verticali**: 3 relocation, 3 life_on_campus, 2 study_abroad, 2 career_readiness (the real eval is balanced 20/20/20/20).
- **Categorie**: 3 informative, 3 computational, 2 actionable, 2 trap (the real eval is balanced 20/20/20/20).
- **Lingua**: 8 EN + 2 IT (the real eval is ~84% EN / ~16% IT - so yes, a portion of the 80 is in Italian. Your buddy must answer in the same language as the question.).

Use them to:

- Calibrate your AI Buddy across all four verticali, all four categories, and both languages.
- Test your endpoint end-to-end.
- Get a feel for question style and difficulty.

The 80 evaluation questions are kept private until evaluation time. They follow the same format and difficulty as the ones below.

## Question categories

Each question falls into one of four categories:
- **informative** - direct factual lookup ("Where is the dining hall?", "When does enrolment open?")
- **computational** - requires aggregating, counting, or comparing across documents
- **actionable** - asks for an output you can act on (list, table, step-by-step instructions, structured email)
- **trap** - ambiguous, off-topic, or unanswerable from the provided data. Tests honesty: the AI must surface the false premise or say it can't answer, not fabricate.

## How you are scored

For every one of the ~80 questions, an **LLM judge** evaluates your response against a reference answer and assigns one of four outcomes:

| Outcome | Points | When |
|---|---|---|
| correct | **+10** | All required facts present and faithful to source. |
| partial | **+5** | Some required facts present, no incorrect claims, no fabrication. |
| no_answer | **0** | Honest abstention: "I don't have this information." No claim, no penalty. |
| wrong | **-15** | Any incorrect answer: confused entity, fabricated fact, empty output, or system error. |

**Honesty pays**: saying "I don't know" is `no_answer` (0 points). Inventing a plausible-sounding fact is `wrong` (-15). For `trap` questions (ambiguous, off-topic, or unanswerable), the correct response is to surface the false premise or say "no such thing exists in the available data" - that gets `correct` if explicit about why, or `no_answer` if a plain abstention. Confidently fabricating gets `wrong`.

We do NOT distinguish between honest mistakes and fabrications: from the user's perspective, both produce the same harm (incorrect information). The penalty is the same.

The judge accepts paraphrases, translations, and reasonable formatting variation. It checks factual correctness and grounding, not exact strings.

## Format

Each call to `/ask` looks like:

```json
POST /ask
{ "question": "<the question>" }
```

Your response must be:

```json
{
  "answer": "<your answer in the same language as the question>",
  "sources": ["<file path or identifier>", "..."],
  "verticale": "relocation" | "life_on_campus" | "study_abroad" | "career_readiness"
}
```

---

## The 10 sample questions

1. **What is the price of an annual ATM transit pass for students under 27 in Milan, and how does it compare with the standard adult annual urban pass?**

2. **List the steps an international student must follow to register with Italy's National Health Service (SSN) in Milan.**

3. **Confrontando i bus diretti da Malpensa a Milano Centrale tra i vettori documentati (Autostradale/Malpensa Bus Express, Terravision, Flibco, FlixBus): qual e' il prezzo di partenza piu' basso indicato per ciascun vettore?**

4. **Quale documento devo portare per accedere alla Biblioteca Bocconi, e qual e' la capienza massima dell'edificio?**

5. **Provide a structured table of the dining areas available on the Bocconi campus, indicating the location of each and its meal/opening pattern.**

6. **For the Bocconi MSc graduate Exchange Program selection score, how are academic GPA, credits, and Bachelor degree grade weighted? Show the weights and explain.**

7. **What is the application deadline for the Bocconi Double Degree program with MIT (Massachusetts Institute of Technology)?**

8. **What is the maximum amount of the Bocconi Merit Award tuition waiver for graduate (Master of Science) students, and what is the format of the award (e.g. tuition waiver only, tuition waiver plus stipend, etc.)?**

9. **What are the placement results published in the 2026 BESS graduate survey?**

10. **How many different paid Bocconi Sport Membership tiers are listed for the 2025/2026 season, and which is the cheapest one available to UB and SDA Bocconi students?**

---

## Tips

- The evaluator does not care how your `/ask` answers are styled. It cares that they are **factually correct**, **grounded in the bundled data**, and **honest** when the question can't be answered.
- For `trap` questions (e.g. #7, #9), the correct response is to surface the false premise or say "no such thing exists in the available data". Do **not** make up a plausible-sounding answer - that costs you -15.
- For `actionable` questions (e.g. #2, #5), structured output (numbered lists, tables) makes them easy to verify.
- For Italian questions (e.g. #3, #4), answer in Italian. The judge accepts translations of cited material but the response language must match the question language.
- Cite real `data/` paths in `sources`. Fabricated citations count as `wrong` (-15).
- 30s latency cap: a slow but correct response that exceeds 30s scores `wrong` (system error = same penalty as a wrong answer).
- Build break-even: rough rule of thumb, only attempt an answer when your confidence is above ~60%. Below that, prefer to abstain ("I don't have this information") and score 0.
