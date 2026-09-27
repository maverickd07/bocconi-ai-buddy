# **Bocconi Hackathon: AI Buddy Challenge**

**Bocconi × Yellow Tech × OpenAI**

Six hours to build a smart application that helps Bocconi students navigate everyday life: housing in Milan, international experiences, career, campus life.

* **Duration:** 6 hours  
* **Format:** Individual  
* **Tool:** OpenAI Codex  
* **Prize:** Top 15 advance to the Italian Hackathon League final

## **1\. The Challenge**

Build an app, the **"AI Buddy,"** that helps Bocconi students navigate university life. An assistant that genuinely understands Bocconi and Milan, and can answer concrete questions across four areas of student life.

The AI Buddy must cover all four areas listed below. How you present, integrate and surface them is the creative part: linear chat, dashboard, guided journeys, interactive map, planner, personalized onboarding.

### **Example questions it should be able to answer**

* "I am looking for a flat near Bocconi with a 700€/month budget. Which neighborhoods would you recommend, and why?"  
* "Which partner universities offer a Double Degree in Finance, and what are the requirements?"  
* "When does the curricular internship application close, and how do I submit it?"  
* "What events are happening on campus this week that are open to first-year students?"  
* "I am an international student who just arrived. Where do I start with the residence permit?"

The 80 questions used in the automatic evaluation will have this level of concreteness and specificity, distributed across the four verticals.

### **The four areas**

**Area 1: Life in Milan**

Housing, neighborhoods, transportation, bureaucracy. Everything related to arriving in and living in the city.

**Area 2: International experiences**

Exchange programs, double degrees, partner universities, opportunities for studying and working abroad.

**Area 3: Career and the job market**

CVs, internships, placement, Career Service events, professional outlook.

**Area 4: Campus life**

Dining, events, student associations, sports, well-being, social life.

## **2\. What you find in the starter kit**

At the start of the event you receive a ready-to-use package: data, working environment, access.

### **Ready-to-use datasets**

* **Bocconi knowledge base, snapshot 2026-05-02 with 2026-05-08 delta (~1,617 markdown files):** course catalog, academic calendar, campus map, services (dining, library, sports), Career Service, scholarships, exchange programs, student associations, administrative procedures, plus a curated set of external public sources pre-bundled on 2026-05-08 (Farnesina country advisories, AlmaLaurea graduate surveys). The dataset is a frozen snapshot; the 80 hidden evaluation questions are written against it and reflect what was current in May 2026 - the running 2025-26 academic year and the open application cycle for 2026-27.

### **Extra open data**

Beyond the datasets we provide, you are **free to integrate any open data you want, from any public source**: ISTAT portals, data from other cities, OpenStreetMap, Eurostat, OECD, QS or THE rankings, academic datasets, public APIs, scraping of public web pages. There is no whitelist: if the source is public and legally accessible, you can use it.

### **Working environment**

A **pre-configured technology base**: project scaffolding with frontend, backend and Docker environment ready to go, AI/RAG dependencies installed, data structure in place, and containers that run locally with a single command. You do not spend time setting up the environment: open the folder and start building.

Together with the project you receive a **starter guide** with a suggested first prompt for Codex, and a **minimal technical constraint** already configured (the format your app uses to receive evaluation questions, handled automatically if you follow the guide).

### **Access**

* ChatGPT EDU account with Codex unlocked.  
* A personal OpenAI redemption code worth $50 of credit. You activate it on your own OpenAI account and then create your own API key. The key powers your app when a user asks it a question.  
* 10 sample questions, to give you a sense of what the AI Buddy will need to handle.

## **3\. The three components of the app**

A useful mental model for working with Codex and making product decisions. Your app has three parts.

**Component 1: The interface.** What the user interacts with: screens, navigation, chat, maps, charts.

**Component 2: The "brain."** The logic that receives questions, processes them with the AI, and produces the answer.

**Component 3: The knowledge.** The Bocconi and Milan datasets, from which the AI draws answers instead of inventing them.

### **What is fixed and what is open**

The starter package defines two small things as **fixed**, because they are required for the automatic evaluation to work: the format your app uses to receive questions (a predefined input/output schema for the endpoint), and the rule that **the AI replies in the same language as the question** (evaluation questions will be in English, but real users may write in Italian). These two constraints are already configured in the starter code; Codex handles them automatically, you do not need to think about them.

### **What you decide**

* **Style and design** of the interface: minimalist, bold, with maps, charts, animations.  
* **User experience:** simple chat, guided journey, sectioned dashboard, onboarding for first-year students. The structure is yours.  
* **Agent complexity:** a fast, direct buddy, or a more sophisticated one with multiple reasoning steps. The more it reasons, the longer it takes; the limit is 30 seconds per response.  
* **Extra data:** beyond the provided datasets, you can integrate other public sources. This is rewarded by the judges.

## **4\. Event setup**

| Tool | Time | Purpose |
| ----- | ----- | ----- |
| **Docker Desktop** | 10–15 min | Creates the isolated environment in which your app runs locally. Install, open, leave it running. On Windows, you also need to enable WSL2. |
| **Codex Desktop App** | 5 min | The main app where you work. Available for Mac and Windows. |
| **Railway account** | 2–3 min | For publishing your app online at the end of the day. Free tier. |
| ChatGPT EDU account | already provisioned | Managed by Bocconi together with OpenAI. |
| Personal OpenAI redemption code | already provisioned | Distributed on the platform. Redeem it on platform.openai.com to unlock $50 of credit, then create your own API key. |

**Total time:** about 30 minutes from scratch, 5 minutes if you already have Docker installed.

## **5\. The work flow**

You will work with Codex Desktop App, which integrates a chat with the agent, the project files, a terminal

1. **Extract the project.** Unzip the folder you receive. Inside you find the project structure, datasets, Docker environment and starter guide.  
2. **Open the project in Codex Desktop App.** "Open local folder" on the extracted folder. The agent now has visibility on the project.  
3. **Start the environment.** Ask Codex to "Start dev". Containers start up, the app runs locally and becomes reachable in your browser.  
4. **Send the first prompt.** The starter guide includes a sample initial prompt. You can use it as is or write your own. The initial direction you set matters: it defines the foundation you will iterate on.  
5. **Iterate for 6 hours.** Continuous conversation with Codex. Plan in blocks: first a working baseline that covers all four verticals, then quality, design, differentiating features. Verify in the browser after every meaningful change.  
6. **Deploy.** Ask Codex to "Deploy". The app is published on Railway with a public URL (*yourproject.up.railway.app*).  
7. **Submit.** Submission form: app URL, source code zip, product description (\~200 words).

## **6\. The day, on a timeline**

* **09:00 \- 10:00:** Welcome and check-in, plenary briefing: rules presentation, challenge demo, Q\&A                                                                                  
* **10:00 \- 16:00:** Work session and submission (6 hours)                                                                                                                            
* **16:00 \- 17:00:** Submissions review by jury, networking session with OpenAI & Yellow Tech for participants                                                                        
* **17:00 \- 18:00:** Finalists presentation live, award ceremony                                                                                                           

\* Self service lunch break will be offered between 12:00 \- 14:00 outside the classroom 

## **7\. How you are evaluated**

Three levels, from the most automated to the most human. To reach the final pitch, you must clear all of them.

### **Level 1: Automatic evaluation**

An automated system sends about 80 questions to your app and checks how it responds. The questions fall into four categories:

* **Informative:** "Where is the dining hall?", "What are the library opening hours?"  
* **Computational or comparative:** "Which partner university has the most exchanges with Bocconi?"  
* **Actionable:** "How do I apply for a scholarship?"  
* **Traps:** ambiguous, off-topic, or unanswerable questions. They test the AI's honesty: those who fabricate answers lose points.

A subset of the 80 questions intentionally requires information from public sources beyond the bundled Bocconi/Milano dataset (e.g. national open-data portals, Farnesina country advisories, AlmaLaurea graduate statistics). Pointers are listed in `data/extra-sources.md`. An honest "I don't have that data" answer scores 0 (no penalty); a fabricated answer scores -15.

Points are gained for correct answers (+10), partials (+5), or honest abstentions (0 - "I don't know"). Points are lost for any incorrect answer (-15: confused entity, fabricated fact, empty output, system error). Each response must arrive within 30 seconds; beyond that, the question scores `wrong` (-15) - so choose the LLM model accordingly. The top 30 advance.

\> **Watch the timing.** A highly sophisticated AI that takes many steps before answering risks exceeding the 30-second limit. Find the right balance: it must reason well *and* respond in time.

### **Level 2: Human evaluation**

The top 30 are evaluated on:

* User experience: is the app clear, well-designed, accessible?  
* Creativity: is the idea original?  
* Interactivity: is it more than a static chat?  
* Mobile-friendliness: does it work on a phone?  
* Use of extra data: have you integrated sources beyond the provided ones?  
* Product quality: is it polished, complete, finished?

Selection: **15 projects** qualify for the **Italian Hackathon League** final. Among these, **3** are chosen for the in-room pitch at the end of the day.

### **Level 3: Final pitch**

* The 3 finalists present in front of the entire room (\~5 minutes plus questions).  
* Jury announces the winner.

\> **In short:** Level 1 verifies that your app works. Level 2 rewards those who go beyond the minimum. Level 3 is the pitch.

## **8\. What you submit**

Hard cutoff: 6 hours from the start. Nothing is accepted afterward.

The submission form asks for:

1. The public URL of your app (Railway address).  
2. The frontend URL (can be the same or separate).  
3. A zip of the source code, for archive.  
4. A short description (\~200 words) of your idea, written by you. This is what the judges read in Level 2\.

\> **The main risk:** if your app is not reachable when the automatic evaluation begins, every question scores `wrong` (-15) and your Level 1 total goes to the floor (-1200). Deploy early, even with a minimal version, and iterate from there. Do not leave it for the last 10 minutes.

## **9\. Strategy**

### **Specific prompts, not vague ones**

Codex's quality scales with how specific you are. "Make a nice page" produces generic output; "Build a homepage with four cards, one per area, each with an icon, a title, a micro-description, and a CTA that opens the chat pre-filtered on that vertical" produces something concrete. The more context you provide, the less it has to guess.

### **Build an MVP first, then differentiate**

Spend the first part of the day getting to a working baseline that covers all four verticals, even minimally. Spend the second part on what makes your project stand out: design, original features, integration of extra open data, polished user experience. A complete and differentiated prototype beats a sophisticated and incomplete one.

### **Optimize for the evaluation criteria**

The 10 sample questions are diagnostic: they indicate the topical coverage and level of specificity expected at Level 1\. Study them. The Level 2 rubric (UX, creativity, interactivity, mobile, extra data, quality) is published: use it as a product checklist.

### **Calibrate the buddy on the sample questions**

The 10 sample questions in `SAMPLE_QUESTIONS.md` are your **working test bench**. The 80 hidden evaluation questions follow the same level of specificity and the same four categories.

We do **not** give you the correct answers. Finding them is part of the work: open the relevant verticale folder under `data/`, search the markdown files, decide what the buddy *should* have said. Then iterate.

The loop, repeated through the day:

1. Ask the buddy one of the sample questions through your UI.  
2. Compare its answer to what the data actually says.  
3. If it is off, tell Codex *what* is off ("the buddy invented a deadline that does not match the academic calendar", "missed the AlmaLaurea numbers entirely", "answered in English when I asked in Italian"). Ask Codex to improve the pipeline accordingly.  
4. Repeat with the next question.

Your job is to keep asking the right *what*: which questions still fail, in which way, and how the answer should look. Codex knows the *how* - how to make the buddy read the right files, how to combine multiple steps, how to weight different sources - and will walk you through it whenever you want. Ask, apply, learn, repeat.

The buddy you are building rests on six well-known levers - the building blocks of any RAG system: **chunking**, **retrieval**, **re-ranking**, **embedding model**, **hybrid search**, **query rewriting**. Don't use them as magic words you drop in the Codex chat without knowing what they do. For each term, ask two questions:

1. *"What is X, and how does it shape the answers the buddy gives?"* - Codex explains in plain language, with the project in front of it.  
2. *"Now improve X in this project."* - Codex applies the change. Re-run the calibration loop above and see if the answer is closer.

By the end of the day you will know how a RAG system actually works, not just how to ask for one. That is the part of the hackathon you keep, beyond the score.

The students who win Level 1 are not the ones who set up the most sophisticated pipeline up front. They are the ones who run this loop the most times in 6 hours.

### **Balance agent complexity and latency**

Multi-step architectures (planning, retrieval, verification) improve answer quality but increase latency. With a 30-second timeout, an over-engineered agent risks losing points on many questions. Measure empirically before committing.

### **Mid-event deploy, not last-minute deploy**

A useful rule of thumb: do your first Railway deploy around hour 3 of the event, even if `/ask` still returns placeholder responses. The point is to surface infrastructure issues (env vars, build errors, healthcheck timeouts) with hours of buffer left, while mentors in the room can still help. Once the deploy flow works, every subsequent `railway up` takes seconds.

Do **not** leave the deploy for the last 30 minutes. The most common reason a project gets a heavy negative Level 1 score (down to -1200) is a deploy that didn't go up in time: every unreachable question counts as `wrong` (-15).

### **What NOT to do**

* Do not share or commit your redemption code or the API key you create from it (disqualification).  
* Do not connect the project to GitHub during the hackathon: it violates the guidelines and consumes the shared workspace credit pool.  
* Do not postpone the deploy to the end of the event.  
* Do not ignore the 10 sample questions.

## **10\. FAQ**

**Can I work in a team?**

No. The hackathon is individual, aligned with the Bocconi community week.

**Do I need to know how to code?**

No. Codex writes the code. A clear product vision, however, is what separates an average submission from a winning one.

**Can I edit the code directly if I want to?**

Yes. The Desktop App allows manual file editing. For participants with technical experience this can be useful in specific cases, but it is not required.

**How do I handle situations where Codex makes mistakes or misunderstands?**

Explicit iteration: describe the problem with reference to errors, logs or observed behavior. "This endpoint returns 500, here is the traceback X. Hypothesize the cause and fix it." Codex is effective with concrete feedback, less with vague instructions.

**What if the deploy does not work?**

A Yellow Tech mentor team will be in the room throughout the event to troubleshoot deploy issues. Preventive mitigation: **plan your first deploy around hour 3 of the event**, not at the end. The starter kit's `Dockerfile.prod` and `railway.json` are pre-configured (see `DEPLOY.md`), so the first deploy should be quick. Even if `/ask` still returns placeholder responses, you'll surface any infrastructure issue with hours of buffer left to fix it - on your own or with a mentor.

**Can I add extra datasets or libraries?**

Yes, it is encouraged.

**What language should the AI respond in?**

The same language as the question. The 80 evaluation questions will be in English, so the AI will reply in English. If a user writes in Italian, it should reply in Italian.

**Can I test my app before the evaluation?**

Yes, and you should. Just ask Codex to send a sample question to your `/ask` endpoint, or run `curl -X POST http://localhost:8000/ask -H 'Content-Type: application/json' -d '{"question":"test"}'`. If it does not respond, something is wrong, and you have time to fix it. Test the deployed version on Railway too - early and often.

