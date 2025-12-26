# Agentic AI Review Trend Analysis – Senior AI Engineer Assignment

## Overview
This project implements an **agentic AI system** that consumes daily Google Play Store
reviews and generates a **30-day rolling trend analysis** of issues, requests, and feedback.

The solution is designed for **high recall**, **semantic correctness**, and **product usability**.

---

## Problem Statement
Product teams require a reliable way to track **evolving user issues and requests** without
fragmentation caused by semantically similar but differently worded feedback.

Traditional topic modeling approaches (LDA, TopicBERT) fail to maintain accuracy at scale.
Hence, an **Agentic AI approach** is used.

---

## Agentic Architecture

### 1. Review Cleaner Agent
- Normalizes incoming review text
- Removes noise and formatting inconsistencies

### 2. Topic Extraction Agent
- Extracts issue/request/feedback topics
- Uses intent-based rules (LLM-replaceable)

### 3. Topic Deduplication Agent (Key Focus)
- Converts topics into semantic embeddings
- Merges similar topics using cosine similarity
- Ensures:
  - “Delivery guy was rude”
  - “Delivery partner behaved badly”
  → **Delivery partner rude**

### 4. Trend Aggregation Agent
- Aggregates topic frequency per day
- Produces a rolling **T-30 to T** trend table

---

## Input
- Google Play Store app link
- Target date T
- Daily review batches (simulated in this submission)

---

## Output
A tabular trend report:
- Rows: Topics
- Columns: Dates (T-30 → T)
- Cells: Frequency of topic occurrence

Sample output available in:
