# Business Info Retrieval Agent Using Yelp Data

## Abstract
This project builds an Information Retrieval Agent that answers natural language queries about local business by combining iterative reasoning with information retrieval from a Yelp business dataset. The agent uses a Qwen 2.5-0.5B instruction-tuned language model to generate explicit reasoning steps and search actions, then retrieves relevant business information based on a corpus of 500 Yelp business. 

**NEED TO ADD OUTCOMES AFTER TESTING**

## Overview

This project focuses on building an **Information Retrieval Agent** that processes natural language queries and returns structured, relevant business information using Yelp data. Yelp's extensive dataset contains millions of reviews and rich business metadata, making it a strong foundation for developing intelligent search and recommendation systems.

### Problem Statement
 Users face challenges quickly finding relevant businesses, extracting meaningful insights from large volumes of reviews, and narrowing results efficiently when prompts involve multiple factors such as ambience, location, and price. Users need a system that can answer natural language queries like "What is the best CHinese restaurant in South End of Boston?" by resoning through multiple steps and retreiving relevant business information from an external knowledge base. This agent aims to solve those problems by combining NLP, cosine similarity search, and Yelp datasets to deliver accurate and contextual results.

### Why This Problem Is Interesting
This problem is interesting because it highlights a broader challenge faced by many information systems today: making unstructured, test-heavy data easily acessible and searchable for everyday uesrs. This problem is also interesting because our solutionc an be expanded in the future to support a variety of more advanced capabilities such as personalized recommendations based on user history, automatically summarizing review sentiment, detecting emerging trends in local business and more. 

### Approach and Methodology 
To address this, we combine:
* NLP for query understanding
* TF-IDF or embedding-based cosine similarity search
* LLM-based reasoning for iterative retrieval stps

### Rationale 

### Key Components
* **Natural Language Query Parsing**: Uses NLP techniques to extract intent and key parameters from user input.
* **Cosine Similarity Search**: Computes similarity between query vectors and business/review embeddings using TF-IDF or similar methods.
* **Structured Output**: Returns relevant business options along with summarized insights.
* **Highly Extensible**: Supports future additions like business recommendations, review summarization, and advanced feature extraction.

### Limitations
* No semantic embedding search
* No structured metadata filtering
* Limited to 500 business subset
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
* User queries are assumed to containe actionable attributes
* TF-IDF is sufficient for baseline retrieval due to limited dataset size
* Small LLMs are chosen for efficiency rather than state-of-the-art performance

### Limitations
* Small model size may limit reasoning sophistication
* TF-IDF lacks deep semantic understanding compared to embeddings
* Dataset contains only 500 businesses, limiting coverage

## Experiment Setup

### Dataset
The project uses a subset of the Yelp Open Dataset, consisting of:
* 500 businesses
* Business attributes: name, location (address, city, state, postal code), stars, number of reviews,  attributes (ex. Accepts Credit Card), categories (ex. Accupuncture, Hours)

#### Why Yelp Data?
* Large-scale, real-world dataset
* Includes business entities, detailed attributes, and millions of user-generated reviews
* Enables robust experimentation with text analysis and search methods
* Provides realistic scenarios for user-facing applications

### Implementation
* Python-based pipeline
* TF-IDF vectorizer 
* Cosine similarity scoring
* Qwen 2.5-0.5B instruction LM for decision-making

### Environment
* CPU-based experimentation
* Local development environment/Jupyter Notebook

### Model Architecture
* LLM reasoning module: Receives query -> outputs reasoning steps -> triggers search
* Retrieval module: TF-IDF -> similarity matrix -> top-k results
* Fusion module: LLM formats final structured output

## Getting Started

### Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

The application consists of a backend API server and a frontend interface. You'll need to run both:

#### 1. Start the Backend API Server

In one terminal window, start the API server:
```bash
python start_server.py
```

The API server will be available at:
- API endpoint: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

#### 2. Start the Frontend

In a separate terminal window, start a simple HTTP server to serve the frontend:

**Option A: Using Python's built-in HTTP server (Python 3)**
```bash
python -m http.server 3000
```

**Option B: Using Python's built-in HTTP server (Python 2)**
```bash
python -m SimpleHTTPServer 3000
```

Then open your browser and navigate to:
```
http://localhost:3000/frontend.html
```

The frontend will connect to the backend API running on port 8000.

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

## Discussion

## Conclusion

## Potential Extensions

* Business recommendation engine
* Sentiment and topic summarization for reviews
* Feature extraction (e.g., parking availability, ambience descriptors)
* Ranking models using ML or embeddings

## License

This project is for academic and research purposes.


## Acknowledgments

Yelp Open Dataset
Starter code provided as part of course/project materials.
