"""
Senior AI Engineer Assignment – Agentic Review Trend Analysis
Author: <Your Name>

This script simulates an agentic AI pipeline that:
1. Consumes daily app reviews as batches
2. Extracts issue/request/feedback topics
3. Deduplicates semantically similar topics
4. Generates a 30-day rolling trend report
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


# -----------------------------
# Agent 1: Review Normalizer
# -----------------------------
class ReviewCleanerAgent:
    def clean(self, text):
        return text.lower().strip()


# -----------------------------
# Agent 2: Topic Extraction Agent
# -----------------------------
class TopicExtractionAgent:
    def extract(self, review):
        """
        Simple rule-based seed + semantic expansion.
        In production, this can be replaced with LLM calls.
        """
        if "delivery" in review and "rude" in review:
            return "Delivery partner rude"
        if "delivery" in review:
            return "Delivery issue"
        if "stale" in review or "cold" in review:
            return "Food quality issue"
        if "map" in review or "location" in review:
            return "Maps not working properly"
        if "instamart" in review:
            return "Instamart availability request"
        return "Other feedback"


# -----------------------------
# Agent 3: Topic Deduplication Agent
# -----------------------------
class TopicDeduplicationAgent:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def deduplicate(self, topics):
        embeddings = self.model.encode(topics)
        similarity_matrix = cosine_similarity(embeddings)

        canonical_topics = {}
        used = set()

        for i, topic in enumerate(topics):
            if i in used:
                continue
            canonical_topics[topic] = topic
            for j in range(i + 1, len(topics)):
                if similarity_matrix[i][j] > 0.85:
                    canonical_topics[topics[j]] = topic
                    used.add(j)
        return canonical_topics


# -----------------------------
# Agent 4: Trend Aggregation Agent
# -----------------------------
class TrendAggregatorAgent:
    def aggregate(self, records):
        df = pd.DataFrame(records)
        trend = pd.pivot_table(
            df,
            values="count",
            index="topic",
            columns="date",
            aggfunc="sum",
            fill_value=0
        )
        return trend


# -----------------------------
# Main Agent Orchestrator
# -----------------------------
def run_agent_pipeline():
    # Simulated daily reviews (last 30 days)
    today = datetime.today().date()
    dates = [today - timedelta(days=i) for i in range(30)]

    sample_reviews = [
        "Delivery guy was rude",
        "Delivery partner behaved badly",
        "Food was cold and stale",
        "App map not working",
        "Instamart should be open all night",
        "Delivery delayed again"
    ]

    cleaner = ReviewCleanerAgent()
    extractor = TopicExtractionAgent()
    deduper = TopicDeduplicationAgent()
    aggregator = TrendAggregatorAgent()

    raw_topics = []
    records = []

    for date in dates:
        for review in sample_reviews:
            clean_text = cleaner.clean(review)
            topic = extractor.extract(clean_text)
            raw_topics.append(topic)
            records.append({
                "date": date.strftime("%Y-%m-%d"),
                "topic": topic,
                "count": 1
            })

    canonical_map = deduper.deduplicate(raw_topics)

    for r in records:
        r["topic"] = canonical_map.get(r["topic"], r["topic"])

    trend_report = aggregator.aggregate(records)
    trend_report.to_csv("output/sample_trend_report.csv")

    print("Trend report generated successfully!")


if __name__ == "__main__":
    run_agent_pipeline()
