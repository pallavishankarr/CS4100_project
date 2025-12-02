Business Info Retrieval Agent — Spec Sheet

Spec Version: v0.1
Date: 2025-XX-XX
Owner: Niam Bashambu
Status: Draft (AI-Enhanced)

Part A — Business Context & Problem Statement
A1. Strategy / Context (Simplified)

Users struggle to quickly find relevant local businesses—especially when queries involve multiple attributes such as cuisine, ambience, location, price, and preferences. Yelp’s dataset is large and unstructured, making it difficult for everyday users to extract personalized, accurate information.

This project builds an Information Retrieval Agent that answers natural language business queries by combining LLM-driven reasoning with cosine similarity search over Yelp data.

A2. Problem Statement (S–C–Q)

Situation: Users want fast, accurate answers about local businesses when using natural language queries.
Complication: Yelp data is large, text-heavy, and unstructured. Users often get irrelevant or broad results.
Question: How can we build an agent that interprets natural language, reasons through multi-step constraints, and retrieves highly relevant businesses?

A3. SMART Goals (Workshop Scope)

Demonstrate a working pipeline that:

Accepts a natural language business query.

Generates 1–2 LLM reasoning/action steps using Qwen 2.5-0.5B.

Performs TF-IDF + cosine similarity search over 500 Yelp businesses.

Returns structured business results under 2 seconds on CPU.

Return 3–5 relevant business results with supporting metadata.

Deliver a simple UI (optional) or Jupyter workflow that shows reasoning + retrieved results.

A4. One-Line Scope

Build a small demo IR agent that takes a natural language query about local businesses and returns ranked, relevant results using LLM reasoning + TF-IDF retrieval over Yelp data.

Part B — Build Plan (Solution Architecture & Design)
B1. Overview

A lightweight Python backend (or Jupyter pipeline) processes queries using a two-stage architecture:

LLM Reasoning (Qwen 2.5-0.5B)
Extracts intent, generates reasoning steps, and determines retrieval constraints.

Retrieval Engine

Converts query → TF-IDF vector

Performs cosine similarity search over Yelp business/review data

Returns top-k most relevant businesses

Fusion + Output
LLM composes structured, user-friendly answers with metadata (rating, categories, attributes).

B1.1 AI Architecture
Stage 1 — Reasoning & Action Planning

The LLM receives the query and produces:

Extracted attributes (e.g., cuisine, ambience, location)

Reasoning steps

A retrieval action like:

“Search for businesses matching Italian + cozy + downtown Boston.”

Stage 2 — Retrieval Layer

TF-IDF vectorization of business descriptions / reviews

Cosine similarity ranking

Optional metadata filtering (categories, city, rating thresholds)

Stage 3 — Answer Synthesis

The LLM receives top-k businesses and returns a final structured answer including:

Business name

Rating

Review snippet summary

Reason it matches the query

B2. Inputs
User Query Input
{
  query: string;       // Required. Example: “Best Chinese restaurant in South End”
  top_k?: number;      // Optional. Default: 5
}

Yelp Corpus

A local dataset of ~500 businesses with:

Name

Address

City, State, ZIP

Stars

Review count

Categories

Attributes

Review texts

B3. Outputs
BusinessResult Object
{
  business_id: string;
  name: string;
  address: string;
  stars: number;
  categories: string[];
  similarity_score: number;
  summary: string;       // LLM-generated
}

API / Final Output
{
  reasoning: string[];       // LLM reasoning steps
  retrieved: BusinessResult[];
}


Returns 3–5 results by default.

reasoning is optional if disabled.

B4. Core Logic / Modules
1. Parse Query

Validate input

Clean text

Pass to LLM for reasoning

2. LLM Reasoning (Qwen 0.5B)

The model produces:

Extracted filters

Suggested retrieval terms

Additional constraints (e.g., “cozy ambience”, “good for dates”)

3. Vectorization + Retrieval

TF-IDF vectorization of business descriptions

Cosine similarity search

Optionally apply city/category filters

4. Structured Output Generation

LLM synthesizes final answers using:

Business metadata

Review snippets

Similarity scores

5. Return JSON

Deliver top-ranked businesses + reasoning steps.

Part C — Testing Plan
C1. Positive Tests
TC-01 — Query with Clear Attributes

Input: “Best Chinese restaurant in South End of Boston”
Expected:

Reasoning extracts: Chinese, South End, restaurant

Top 3–5 matching businesses returned

Summaries reflect relevant reviews

TC-02 — Query with Ambience

Input: “Cozy Italian restaurant good for date nights”
Expected:

Extracts cuisine + ambience + use case

Businesses with associated attributes returned

Similarity scores reasonable

TC-03 — Query with Multiple Constraints

Input: “Cheap Mexican food near downtown with outdoor seating”
Expected:

LLM extracts: price, cuisine, outdoor seating

Rankings incorporate both text and metadata

C2. Negative / Edge Tests
TC-04 — No Matching Cuisine

Query references cuisine not present (e.g., Eritrean food).
Expected: fallback to nearest matches or empty result list.

TC-05 — Vague Query

“Something good to eat.”
Expected:

LLM asks for refinements or returns general popular options.

Part D — Trace / Prompt Retention

(Optional) Save LLM reasoning + retrieval metadata:

/trace/retrieval.jsonl

{
  "timestamp": "...",
  "query": "...",
  "reasoning": [...],
  "top_k_raw": [...],
  "filters": {...}
}

Part E — School Assignment Requirements
Rubric Fit
Category	Weight	How This Project Satisfies It
Business Logic & Value	30%	Problem is clear, tied to real-world Yelp data, high impact.
Agentic Execution	30%	Uses LLM reasoning + multi-step retrieval loop.
Technical Functionality	25%	Implements TF-IDF IR system + structured output.
Creativity & UX	15%	Flexible natural language search, extensible to recommendations.
Part F — Setup & Installation
F1. Prerequisites

Python 3.8+

Jupyter or FastAPI

Qwen 2.5–0.5B (HuggingFace)

scikit-learn

pandas

numpy

F2. Data Setup

Download Yelp subset (500 businesses).

Run preprocessing script:

Clean text

Merge reviews + metadata

Generate TF-IDF matrix

F3. Running the Pipeline
Option 1 — Jupyter Notebook

Run cells sequentially

Input queries directly

Displays reasoning + results

Option 2 — API (FastAPI)

Endpoints:

GET /api/health

POST /api/query { query: string }



Part H — Frontend (Added)
H1. Purpose
Provide a lightweight, responsive frontend that demonstrates the IR agent in action. It should allow users to enter natural language queries, view LLM reasoning steps, and inspect retrieved business results with metadata and similarity scores.


H2. Tech Stack
- React (single-file demo component for rapid prototyping)
- Tailwind CSS for styling (utility-first; no external styles required)
- Fetch API to call backend endpoints (e.g., POST /api/query)
- Optional: Vite or Create React App for local dev


H3. Pages & Components (single-demo file)
- QueryBar: input + top_k control + submit button
- ReasoningPanel: displays LLM reasoning steps (collapsible)
- ResultsList: list of BusinessResult cards with name, stars, categories, address, similarity_score, and LLM summary
- ResultCard: single business display with 'View Reviews' toggle showing top review snippets
- Loading & Error states


H4. UX Flow
1. User enters a query and optionally top_k (default 5).
2. Frontend posts to POST /api/query with JSON { query, top_k }.
3. Backend returns { reasoning, retrieved }.
4. Frontend shows reasoning (if present) and a ranked list of results.
5. User can click a ResultCard for more metadata or to copy address.


H5. Accessibility & Responsiveness
- Keyboard-accessible inputs and buttons
- Responsive grid/list layout for cards


H6. Integration Contract (API)
POST /api/query
Request: { query: string, top_k?: number }
Response: { reasoning?: string[], retrieved: BusinessResult[] }
BusinessResult: { business_id, name, address, stars, categories, similarity_score, summary }


H7. Demo Constraints & Goals
- Keep the UI small (single-file demo), no build-time dependencies required other than standard React + Tailwind.
- Demonstrate reasoning + retrieval side-by-side.
- Be presentable for a class demo or slide recording.

Part G — System Prompt for Cursor
SYSTEM
You are an experienced ML engineer. Your job is to turn the attached spec.md into a functional IR agent using Yelp data.

Follow these expectations:
- Use Python (FastAPI or Jupyter).
- LLM: Qwen 2.5-0.5B for reasoning.
- Retrieval: TF-IDF + cosine similarity.
- Treat spec as source of truth.
- Keep code readable and simple.

Workflow:
1. Read entire spec.
2. Summarize architecture.
3. Scaffold the project structure.
4. Implement retrieval and LLM reasoning.
5. Display structured results for 3–5 businesses.
6. After each step, output:
   WHAT I DID
   WHAT I NEED NEXT


implement front end
END OF SPEC