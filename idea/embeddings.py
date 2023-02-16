"""
Competency question embeddings for similarity, search, and retrieval.
"""
import re
import logging

import pandas as pd
import numpy as np

from torch.utils.tensorboard import SummaryWriter
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

logger = logging.getLogger("idea.extractor")


def agglomerative_clustering(cqs, embeddings, n_clusters=None, metric="cosine",
                             distance_threshold=1.5):
    # Normalisation of CQ embeddings to unit length
    embeddings = embeddings /  np.linalg.norm(embeddings, axis=1, keepdims=True)

    clusterer = AgglomerativeClustering(
        n_clusters=n_clusters,
        metric=metric,
        distance_threshold=distance_threshold) 
    clusterer.fit(embeddings)
    cluster_assignment = clusterer.labels_

    clustered_sentences = {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        if cluster_id not in clustered_sentences:
            clustered_sentences[cluster_id] = []

        clustered_sentences[cluster_id].append(cqs[sentence_id])

    return clustered_sentences


def compute_embeddings(dataset_cq, model="all-MiniLM-L6-v2", device="cpu",
                       out_dir=None, as_tblog=True):
    """
    Compute sentence-level embeddings of competency questions using the given
    and supported SBERT model; optionally saves embeddings as tensors/logs.

    """
    dataset_df = pd.read_csv(dataset_cq)
    questions = list(dataset_df.cq)
    personas = dataset_df["persona"]
    logger.info(f"Found {len(questions)} CQs from {len(set(personas))} personas")

    cleaned_question = []
    for question in questions:  # FIXME to move
        # Collapse complex questions in a sentence
        q = question.replace("\n", "; ")
        # Remove tabular occurrences for metadata
        q = q.replace("\t", " ")
        # Collapse multiple empty spaces
        q = re.sub(r"[ ]+", " ", q)
        # Discard inconsistent punctuation
        q = re.sub(r";[ ]*;", ";", q)
        cleaned_question.append(q)

    model = SentenceTransformer(model, device=device)
    cq_embeddings = model.encode(questions)

    if out_dir and as_tblog:
        writer = SummaryWriter(out_dir)
        metadata = list(zip(cleaned_question, personas))
        writer.add_embedding(cq_embeddings,
                             metadata_header=["cq", "persona"],
                             metadata=metadata, tag='PolifoniaCQ')
        writer.close()

    return cq_embeddings
