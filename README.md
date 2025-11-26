# Business Info Retrieval Agent Using Yelp Data

## Overview

This project focuses on building an **Information Retrieval Agent** that processes natural language queries and returns structured, relevant business information using Yelp data. Yelp's extensive dataset contains millions of reviews and rich business metadata, making it a strong foundation for developing intelligent search and recommendation systems.

Users often face challenges such as:

* Quickly finding relevant businesses
* Extracting meaningful insights from large volumes of reviews
* Narrowing results efficiently when prompts involve multiple factors (e.g., ambience, location, price)

This agent aims to solve those problems by combining NLP, cosine similarity search, and Yelp datasets to deliver accurate and contextual results.

---

## Features

* **Natural Language Query Parsing**: Uses NLP techniques to extract intent and key parameters from user input.
* **Cosine Similarity Search**: Computes similarity between query vectors and business/review embeddings using TF-IDF or similar methods.
* **Structured Output**: Returns relevant business options along with summarized insights.
* **Highly Extensible**: Supports future additions like business recommendations, review summarization, and advanced feature extraction.

---

## System Architecture

```
Yelp Data (Reviews + Business Attributes)
                ↓
        NLP Query Parsing
                ↓
        Parameter Extraction
                ↓
Cosine Similarity Search (TF-IDF or embeddings)
                ↓
    Structured Results + Insights Display
```

### Components

* **Data Layer**: Accesses Yelp business metadata, reviews, and attributes.
* **NLP Layer**: Identifies user intent, filters, and key features.
* **Search Layer**: Uses cosine similarity to match query meaning to relevant business/review data.
* **Output Layer**: Presents a structured and user-friendly response.

---

## Why Yelp Data?

* Large-scale, real-world dataset
* Includes business entities, detailed attributes, and millions of user-generated reviews
* Enables robust experimentation with text analysis and search methods
* Provides realistic scenarios for user-facing applications

---

## Technologies Used

* **Python**
* **NLP Libraries** (spaCy, NLTK, or similar)
* **TF-IDF Vectorization**
* **Cosine Similarity Search**
* **Provided Starter Code** (Included in assignment/project resources)

---

## Potential Extensions

* Business recommendation engine
* Sentiment and topic summarization for reviews
* Feature extraction (e.g., parking availability, ambience descriptors)
* Ranking models using ML or embeddings

---

## Getting Started

1. Load Yelp dataset (businesses + reviews + attributes)
2. Process text using NLP pipeline for cleaning + entity extraction
3. Build TF-IDF vectors for reviews or combined features
4. Implement cosine similarity retrieval
5. Build structured output format for user queries

---

## Example Query

**User**: *"Find me a cozy Italian restaurant near downtown that’s good for date nights"*

**Agent Output**:

* Extracted intent: Restaurant search
* Key parameters: Italian, cozy ambience, downtown, good for date nights
* Ranked businesses based on similarity + filters
* Display summary insights (price, review sentiments, attributes)

---

## License

This project is for academic and research purposes.

---

## Acknowledgments

Yelp Open Dataset
Starter code provided as part of course/project materials.
