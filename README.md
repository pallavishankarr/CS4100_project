# Business Info Retrieval Agent Using Yelp Data

## Abstract
This project builds an Information Retrieval Agent that answers natural language queries about local businesses by combining iterative reasoning with information retrieval from a Yelp business dataset. The agent uses a Qwen 2.5-0.5B instruction-tuned language model to generate explicit reasoning steps and search actions, then retrieves relevant business information from a corpus of 150,346 Yelp businesses.The system successfully demonstrates iterative reasoning capabilities, with the agent able to break down complex queries into search actions and synthesize results into structured answers. 

## Overview

This project focuses on building an **Information Retrieval Agent** that processes natural language queries and returns structured, relevant business information using Yelp data. Yelp's extensive dataset contains millions of reviews and rich business metadata, making it a strong foundation for developing intelligent search and recommendation systems.

### Problem Statement
Users face challenges quickly finding relevant businesses, extracting meaningful insights from large volumes of reviews, and narrowing results efficiently when prompts involve multiple factors such as ambience, location, and price. Users need a system that can answer natural language queries like "What is the best Chinese restaurant in South End of Boston?" by reasoning through multiple steps and retrieving relevant business information from an external knowledge base. This agent aims to solve those problems by combining NLP, cosine similarity search, and Yelp datasets to deliver accurate and contextual results.

### Why This Problem Is Interesting
This problem is interesting because it highlights a broader challenge faced by many information systems today: making unstructured, text-heavy data easily accessible and searchable for everyday users. This problem is also interesting because our solution can be expanded in the future to support a variety of more advanced capabilities such as personalized recommendations based on user history, automatically summarizing review sentiment, detecting emerging trends in local business and more. 

### Approach and Methodology 
To address this, we combine:
* NLP for query understanding
* TF-IDF or embedding-based cosine similarity search
* LLM-based reasoning for iterative retrieval steps

### Rationale 

### Key Components
* **Natural Language Query Parsing**: Uses NLP techniques to extract intent and key parameters from user input.
* **Cosine Similarity Search**: Computes similarity between query vectors and business/review embeddings using TF-IDF or similar methods.
* **Structured Output**: Returns relevant business options along with summarized insights.
* **Highly Extensible**: Supports future additions like business recommendations, review summarization, and advanced feature extraction.

### Limitations
* No semantic embedding search
* No structured metadata filtering
* TF-IDF retrieval may miss semantically similar businesses
* Small model may misinterpret some queries

---
## Approach and Methodology

### Overall Pipeline
User Query
     ↓
LLM Reasoning (Qwen 0.5B)
     ↓
Generate Search Action
     ↓
TF-IDF Vectorization of Query
     ↓
Cosine Similarity Search over Yelp Corpus
     ↓
Top-k Relevant Businesses Returned
     ↓
LLM Synthesizes Final Structured Answer
     ↓
Output to User

### Model/Method Choices
* Qwen 2.5-0.5B Instruct for reasoning and action planning
* TF-IDF vectorization for baseline semantic similarity 
* Cosine similarity for ranking
* Yelp metadata filtering for narrowing candidates

### Assumptions and Design Choices
* User queries are assumed to contain actionable attributes
* TF-IDF is sufficient for baseline retrieval due to limited dataset size
* Small LLMs are chosen for efficiency rather than state-of-the-art performance

### Limitations
* Small model size may limit reasoning sophistication
* TF-IDF lacks deep semantic understanding compared to embeddings
* TF-IDF retrieval lacks deep semantic understanding

## Experiments

### Dataset

The project uses the Yelp Open Dataset, a comprehensive collection of business information. The dataset contains:

**Basic Statistics:**
* **Total Businesses**: 150,346 businesses
* **Total Reviews**: 6,745,508 reviews (average of 44.87 reviews per business)
* **Geographic Coverage**: 1,416 unique cities across multiple states
* **Average Rating**: 3.60 stars (on a 5-star scale)
* **Category Diversity**: 1,311 unique business categories

**Top Cities by Business Count:**
1. Philadelphia: 14,569 businesses
2. Tucson: 9,250 businesses
3. Tampa: 9,050 businesses
4. Indianapolis: 7,540 businesses
5. Nashville: 6,971 businesses

**Top Categories:**
1. Restaurants: 52,268 businesses
2. Food: 27,781 businesses
3. Shopping: 24,395 businesses
4. Home Services: 14,356 businesses
5. Beauty & Spas: 14,292 businesses

**Business Attributes:**
Each business entry includes:
* Basic information: `business_id`, `name`, `address`, `city`, `state`, `postal_code`
* Location data: `latitude`, `longitude`
* Ratings: `stars` (1-5), `review_count`
* Operational: `is_open` (binary status)
* Rich metadata: `attributes` (JSON object with features like "Accepts Credit Card", "WiFi", "Parking", etc.)
* Classification: `categories` (comma-separated list of business types)
* Hours: `hours` (operating hours by day of week)

**Data Preprocessing:**
The corpus is constructed by combining business metadata into a searchable text field. For each business, we concatenate all non-ID and non-name fields (address, categories, attributes, etc.) into a single `text` field that serves as the searchable content for TF-IDF vectorization.

### Why Yelp Data?
* Large-scale, real-world dataset with diverse business types
* Includes business entities, detailed attributes, and millions of user-generated reviews
* Enables robust experimentation with text analysis and search methods
* Provides realistic scenarios for user-facing applications
* Rich metadata supports complex query types (location-based, category-based, attribute-based)

### Implementation

**Technology Stack:**
* **Language**: Python 3.x
* **Web Framework**: FastAPI for REST API backend
* **Frontend**: HTML/CSS/JavaScript
* **NLP Library**: Custom TF-IDF implementation
* **LLM Framework**: Hugging Face Transformers

**Core Components:**

1. **Knowledge Base Module** (`knowledge_base.py`):
   - Loads Yelp business data from JSON Lines format
   - Implements tokenization using regex pattern matching: `r"[a-zA-Z0-9']+"`
   - Computes TF-IDF vectors with smoothed IDF: `log((N + 1) / (DF + 0.5)) + 1`
   - Implements cosine similarity search with top-k retrieval (agent search uses k=3 by default; user can configure final top_k via API, default 5)
   - Exposes search functionality as a tool for the agent

2. **Language Model Module** (`language_model.py`):
   - Model: Qwen/Qwen2.5-0.5B-Instruct from Hugging Face
   - Precision: bfloat16 on GPU, float32 on CPU
   - Generation parameters:
     * `max_new_tokens`: 160
     * `temperature`: 0.3
     * `do_sample`: True
   - Post-processing: Extracts "Thought:" and "Action:" lines from model output
   - Format enforcement: Adds system prompt to ensure two-line output format

3. **Agent System Module** (`agent_system.py`):
   - Implements ReAct (Reasoning + Acting) framework
   - Maximum steps: 6 iterations
   - Action space: `search[query="...", k=N]` and `finish[answer="..."]`
   - Trajectory tracking: Maintains history of (thought, action, observation) tuples

4. **Prompting Module** (`prompting_techniques.py`):
   - Parses action strings with key-value arguments
   - Formats trajectory history for prompt construction
   - System preamble defines tool contract and expected format

5. **API Module** (`api.py`):
   - RESTful API with `/api/query` endpoint
   - CORS-enabled for frontend integration
   - Extracts businesses from agent observations
   - Formats results with structured metadata

**Key Parameters:**
* **TF-IDF Smoothing**: Uses add-0.5 smoothing in IDF calculation to handle zero document frequencies
* **Top-k Retrieval**: Two-level k parameter: (1) Agent search actions use k=3 by default (determined by LLM), (2) User-configurable top_k via API/frontend (default 5, range 1-20)
* **Max Agent Steps**: 6 iterations to balance thoroughness with efficiency
* **Cosine Similarity Epsilon**: 1e-12 to prevent division by zero
* **Text Snippet Length**: 240 characters for result previews

### Environment

**Hardware:**
* CPU-based experimentation (no GPU required, but GPU acceleration available)
* Compatible with both CPU and GPU execution

**Software:**
* Python 3.8+
* PyTorch 2.0+ (for model inference)
* Transformers 4.35+ (for Qwen model loading)
* Local development environment or Jupyter Notebook

**Model Loading:**
* Model downloaded from Hugging Face Hub on first use
* Device mapping: Automatic (GPU if available, CPU otherwise)

### Model Architecture

**System Architecture:**

The system follows a modular ReAct agent architecture with three main components:

1. **LLM Reasoning Module**:
   - **Input**: User query + trajectory history
   - **Processing**: Qwen 2.5-0.5B-Instruct generates reasoning steps
   - **Output**: Two-line format - "Thought: <reasoning>" and "Action: <tool_call>"
   - **Purpose**: Break down complex queries into searchable sub-queries

2. **Retrieval Module**:
   - **Vectorization**: TF-IDF vectors computed for query and all documents
   - **Similarity Computation**: Cosine similarity between query vector and document vectors
   - **Ranking**: Documents sorted by similarity score (descending)
   - **Top-k Selection**: Returns top k most similar businesses (k determined by agent in search actions, final results limited by user-specified top_k)
   - **Output Format**: Structured JSON with business metadata and similarity scores

3. **Fusion Module**:
   - **Input**: Retrieved businesses from search actions
   - **Processing**: Agent synthesizes observations across multiple search steps
   - **Decision Making**: Determines when sufficient information is gathered
   - **Output**: Final structured answer with business recommendations

**ReAct Loop:**
```
For each step (max 6 iterations):
  1. Format prompt: system_preamble + user_query + trajectory_history
  2. LLM generates: Thought + Action
  3. Parse action: extract tool name and arguments
  4. Execute tool: search corpus or finish with answer
  5. Append observation: tool results added to trajectory
  6. Check termination: if "finish" action, break loop
```

**TF-IDF Implementation Details:**
- **Tokenization**: Case-insensitive word extraction using regex
- **Term Frequency (TF)**: Normalized by document length (count / length)
- **Inverse Document Frequency (IDF)**: Smoothed variant: `log((N + 1) / (DF + 0.5)) + 1`
- **Vector Representation**: Sparse dictionary mapping tokens to TF-IDF scores
- **Similarity Metric**: Cosine similarity with epsilon for numerical stability

## Project Structure

```
CS4100_project/
├── src/                    # Python source code
│   ├── __init__.py
│   ├── agent_system.py     # ReAct agent implementation
│   ├── api.py              # FastAPI backend server
│   ├── knowledge_base.py   # TF-IDF search and corpus management
│   ├── language_model.py   # Qwen LLM wrapper
│   └── prompting_techniques.py  # Prompt formatting and parsing
├── static/                 # Frontend files
│   └── frontend.html       # React-based web interface
├── data/                   # Data files
│   └── yelp_academic_dataset_business.json
├── docs/                   # Documentation
│   ├── Course-Project-Handout.ipynb
│   ├── course-project-introduction.pptx
│   ├── spec.md
│   └── Resources/
├── scripts/                # Utility scripts
│   └── start_server.py     # Server startup script
├── run.sh                  # Easy run script (starts both servers)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Getting Started

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

The easiest way to run the application is using the provided `run.sh` script, which starts both the backend API server and frontend server:

```bash
./run.sh
```

This will start:
- **Backend API Server** at `http://localhost:8000`
- **Frontend Server** at `http://localhost:3000`

Then open your browser and navigate to:
```
http://localhost:3000/frontend.html
```

#### Manual Setup (Alternative)

If you prefer to run the servers manually:

**1. Start the Backend API Server:**
```bash
python scripts/start_server.py
```

The API server will be available at:
- API endpoint: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

**2. Start the Frontend Server:**

In a separate terminal window:
```bash
cd static
python -m http.server 3000
```

Then open your browser and navigate to:
```
http://localhost:3000/frontend.html
```

### Development Workflow

1. Load Yelp dataset (businesses + reviews + attributes)
2. Process text using NLP pipeline for cleaning + entity extraction
3. Build TF-IDF vectors for reviews or combined features
4. Implement cosine similarity retrieval
5. Build structured output format for user queries

## Example Query

**User**: *"Find me a cozy Italian restaurant near downtown that’s good for date nights"*

**Agent Output**:

* Extracted intent: Restaurant search
* Key parameters: Italian, cozy ambience, downtown, good for date nights
* Ranked businesses based on similarity + filters
* Display summary insights (price, review sentiments, attributes)

## Results

### Main Results

The Business Info Retrieval Agent successfully demonstrates the integration of iterative reasoning with information retrieval. Key findings from experimental evaluation:

**Query Processing Capabilities:**

Experimental evaluation with real queries revealed both strengths and significant limitations:

* **Category-based queries perform well**: Query "Find Italian Restaurants" successfully retrieved Italian restaurants, with the majority located in Philadelphia (reflecting the dataset's geographic distribution where Philadelphia has the highest business count).

* **Location filtering is unreliable**: Query "Restaurants in Boston" returned problematic results:
  - Only 1 out of the returned results was actually a restaurant in Boston
  - Some results were not restaurants at all
  - Several results were located in other cities entirely
  - This suggests TF-IDF text matching cannot reliably distinguish location mentions in different contexts (e.g., "Boston" appearing in reviews vs. actual business location)

* **Attribute matching works but lacks quality filtering**: Query "Coffee shop with WiFi" successfully identified coffee shops with WiFi attributes, but returned low-rated businesses that may not meet user expectations for quality.

* **Complex multi-factor queries fail on location constraints**: Query "Cozy Italian restaurant near downtown Boston for date night" produced poor results:
  - Returned restaurants not located in Boston (likely due to limited Boston data in the dataset)
  - Some results were low-rated businesses
  - Results appeared in random cities such as Philadelphia, Tampa, and Indianapolis
  - The system cannot effectively combine location constraints with other query factors

**Retrieval Performance:**
* TF-IDF cosine similarity ranks businesses based solely on textual keyword matching
* The system prioritizes only explicitly mentioned attributes - if rating/quality is not mentioned, it may return 1-star businesses first
* Similarity scores reflect term frequency but do not incorporate business quality metrics (ratings, review counts)
* Location matching fails because it relies on text presence rather than structured geographic filtering

**Reasoning Behavior:**
* The Qwen 2.5-0.5B model generates coherent reasoning steps in most cases
* Typical agent trajectories: 2-4 steps before reaching a final answer
* The model demonstrates ability to refine search queries based on initial observations
* However, the model cannot effectively combine multiple constraints (location + category + quality) in a single query

**System Integration:**
* FastAPI backend successfully handles concurrent requests
* Frontend-backend integration provides responsive user experience
* Structured output format enables easy result parsing and display
* Error handling gracefully manages edge cases (invalid queries, empty results, etc.)

**Critical Limitations Observed:**
* **No quality/rating consideration**: System does not prioritize highly-rated businesses unless explicitly requested, sometimes returning 1-star businesses first
* **Location filtering is fundamentally broken**: Text-based location matching cannot distinguish between location mentions in different contexts, leading to results from wrong cities
* **Dataset geographic bias**: Limited representation of certain cities (e.g., Boston) in the dataset exacerbates location filtering issues
* **No multi-constraint optimization**: Cannot effectively balance location, category, attributes, and quality simultaneously
* **TF-IDF limitations**: Lacks semantic understanding and cannot handle structured metadata filtering

### Supplementary Results

**Parameter Choices and Rationale:**

1. **Max Steps = 6**:
   - Rationale: Balances thoroughness with efficiency
   - Observation: Most queries resolve in 2-4 steps; 6 provides buffer for complex queries
   - Trade-off: Higher values increase latency; lower values may miss relevant information

2. **Temperature = 0.3**:
   - Rationale: Low temperature promotes deterministic, focused outputs
   - Observation: Higher temperatures (0.7+) led to more creative but less reliable action formatting
   - Trade-off: Lower values improve format compliance but reduce reasoning diversity

3. **Max New Tokens = 160**:
   - Rationale: Sufficient for Thought + Action lines without excessive generation
   - Observation: Typical outputs are 20-60 tokens; 160 prevents truncation
   - Trade-off: Higher values waste computation; lower values risk incomplete actions

4. **Top-k Parameters**:
   - **Agent search k = 3 (default)**: The k parameter in agent search actions (e.g., `search[query="...", k=3]`) is determined by the LLM when generating actions, with a default of 3 in the tool definition. This controls how many results the agent sees per search step.
   - **User top_k = 5 (default, configurable)**: The `top_k` parameter in API requests is user-configurable via the frontend interface (default 5, range 1-20). This controls the final number of results returned to the user after all agent steps complete.
   - Rationale: Agent k=3 provides enough context without overwhelming the agent's reasoning, while user top_k=5 gives users a reasonable number of options
   - Observation: 3 results per search step is typically sufficient for agent decision-making; users can adjust top_k based on their needs
   - Trade-off: Higher agent k provides more context but increases prompt length; higher user top_k provides more options but may include lower-quality results

5. **TF-IDF Smoothing (add-0.5)**:
   - Rationale: Prevents division by zero and handles rare terms gracefully
   - Observation: Standard IDF (without smoothing) produced extreme scores for rare terms
   - Trade-off: Smoothing slightly reduces discrimination power but improves stability

6. **Cosine Similarity Epsilon = 1e-12**:
   - Rationale: Prevents numerical instability in division operations
   - Observation: Without epsilon, some edge cases (empty vectors) caused crashes
   - Trade-off: Negligible impact on similarity scores while ensuring robustness


## Discussion

### Analysis of Results

The experimental results demonstrate that a small language model (0.5B parameters) can effectively drive an information retrieval agent when combined with structured retrieval methods. The ReAct framework proves valuable for breaking down complex queries into actionable search steps, though the reasoning sophistication is limited by the model size.

**Strengths:**
1. **Modular Architecture**: The separation of reasoning (LLM), retrieval (TF-IDF), and fusion (agent controller) enables independent optimization of each component
2. **Interpretability**: The explicit Thought/Action/Observation format provides transparency into the agent's decision-making process
3. **Scalability**: TF-IDF indexing scales reasonably well to large corpora (150K+ businesses)
4. **Robustness**: Error handling and format enforcement ensure the system degrades gracefully

**Weaknesses:**
1. **Location Filtering Failure**: The most critical weakness is the inability to reliably filter by location. Experimental results show that queries like "Restaurants in Boston" return businesses from other cities, with only 1 out of multiple results actually being in Boston. This occurs because TF-IDF treats "Boston" as just another keyword, matching it wherever it appears in the text corpus (reviews, descriptions, etc.) rather than filtering on the structured `city` field.

2. **No Quality/Rating Prioritization**: The system does not consider business ratings unless explicitly mentioned in the query. This leads to returning 1-star businesses when users likely expect higher-quality results. The similarity score is purely based on keyword matching, not business quality metrics.

3. **Semantic Limitations**: TF-IDF cannot capture semantic relationships (e.g., "restaurant" vs "dining" vs "eatery") or understand context.

4. **Model Capacity**: The 0.5B model struggles with complex multi-step reasoning, especially when combining multiple constraints (location + category + quality + attributes).

5. **No Structured Metadata Filtering**: Location, price, and other structured attributes are only matched via text search rather than using the structured fields directly.

6. **Dataset Geographic Bias**: The dataset has limited representation of certain cities (e.g., Boston), which exacerbates location filtering problems. Most businesses are concentrated in cities like Philadelphia, Tucson, and Tampa.

7. **Limited Query Understanding**: No explicit entity extraction or query classification to separate location, category, quality, and attribute requirements.

### Comparison with Existing Approaches

**Compared to Traditional Search Engines:**
* **Advantage**: Iterative reasoning allows refinement of search queries based on intermediate results
* **Disadvantage**: TF-IDF is less sophisticated than modern BM25 or neural retrieval methods used in production systems

**Compared to Large Language Model Agents (GPT-4, Claude):**
* **Advantage**: Much lower computational cost and faster inference
* **Disadvantage**: Significantly less sophisticated reasoning and planning capabilities
* **Trade-off**: This system prioritizes efficiency over state-of-the-art performance

**Compared to Semantic Search (Embedding-based):**
* **Advantage**: No need for pre-trained embeddings or GPU for retrieval
* **Disadvantage**: Cannot handle semantic similarity (synonyms, related concepts)
* **Future Direction**: Could integrate sentence transformers (e.g., all-MiniLM-L6-v2) for semantic search

### Diagnosis of Limitations

**Why Results May Not Match Larger Models:**
1. **Model Capacity**: 0.5B parameters is insufficient for complex multi-hop reasoning that larger models (7B+) can do
2. **Training Data**: Smaller models may not have seen as diverse examples of tool use and reasoning
3. **Context Length**: Limited context window restricts ability to consider long observation histories

**Why TF-IDF Underperforms (Validated by Experiments):**
1. **Location Filtering Failure**: Cannot distinguish between location mentions in different contexts. A business with "Boston" in its reviews or description will match a "Boston" query even if it's located in Philadelphia. This is the most critical failure mode observed in testing.

2. **No Quality Consideration**: TF-IDF similarity scores ignore business ratings and review counts. A 1-star business with matching keywords will rank higher than a 5-star business if the keywords appear more frequently in its text.

3. **No Semantic Understanding**: Cannot match "Italian" with "pasta restaurant" or "pizzeria"
4. **Sparse Representations**: High-dimensional sparse vectors may miss subtle relevance signals
5. **No Learning**: Static weighting scheme cannot adapt to query patterns
6. **Text-only Matching**: Cannot leverage structured fields (city, stars, categories) for precise filtering

**Validated Issues from Experiments:**
* **"Restaurants in Boston"**: Only 1/5 results actually in Boston, some weren't restaurants
* **"Coffee shop with WiFi"**: Found correct attributes but returned low-rated businesses
* **"Cozy Italian restaurant near downtown Boston for date night"**: Returned restaurants in Philadelphia, Tampa, Indianapolis - completely wrong locations

**Critical Improvements Needed:**
1. **Structured Location Filtering**: Extract city/location from query and filter on `city`/`state` fields before TF-IDF ranking
2. **Quality-Aware Ranking**: Incorporate `stars` and `review_count` into similarity scores or apply post-filtering
3. **Hybrid Retrieval**: Combine TF-IDF with embedding-based semantic search for better semantic matching
4. **Query Understanding**: Use LLM to extract structured constraints (location, category, min_rating, attributes) and apply them as filters
5. **Reranking**: Apply a learned reranker that considers quality, location accuracy, and relevance
6. **Larger Model**: Upgrade to Qwen 2.5-7B or similar for better multi-constraint reasoning

### Future Directions and Impact

**Potential Improvements:**
1. **Structured Location Filtering**: Extract city/state from queries and filter businesses on `city`/`state` fields before TF-IDF ranking. This addresses the critical "Restaurants in Boston" failure mode.
2. **Quality-Aware Ranking**: Incorporate `stars` and `review_count` into the ranking function. Options include:
   - Post-filtering: Remove businesses below a quality threshold (e.g., <3.5 stars)
   - Weighted scoring: Combine TF-IDF similarity with normalized rating scores
   - Minimum quality requirement: Default to filtering out businesses below 3.0 stars unless explicitly requested
3. **Metadata Extraction**: Use LLM to extract structured filters (location, price range, categories, min_rating) from queries and apply them as explicit database filters before text-based retrieval.
4. **Semantic Embeddings**: Integrate sentence transformers (e.g., all-MiniLM-L6-v2) for semantic similarity to handle synonyms and related concepts.
5. **Query Expansion**: Generate query variations to improve recall, especially for location queries where city names might appear in various forms.

**Potential Impact:**
* **Accessibility**: Makes business discovery more intuitive for non-technical users
* **Efficiency**: Reduces time spent searching through multiple platforms
* **Intelligence**: Provides reasoning transparency compared to black-box recommendation systems
* **Scalability**: Framework can be extended to other information retrieval tasks

## Conclusion
This project integrates iterative LLM reasoning with TF-IDF retrieval using the ReAct framework to build a functional Business Info Retrieval Agent. The system can decompose natural-language queries, perform search actions, and synthesize results, but testing revealed key limitations—particularly with location filtering, handling quality/rating, and combining multiple constraints. Despite these challenges, the project demonstrates a successful end-to-end pipeline, a modular and extensible architecture, and the potential of small language models for agentic retrieval tasks. This work provides a strong foundation for future improvements such as semantic search, richer metadata filtering, and larger model integration.

## License

This project is for academic and research purposes.

## Acknowledgments

Yelp Open Dataset
Starter code provided as part of course/project materials.
