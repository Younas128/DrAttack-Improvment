"""
Sentence Tokenizer: Text embedding and semantic similarity scoring

This module provides:
- Text_Embedding_Ada class for obtaining embeddings via OpenAI's text-embedding-ada-002
- Caching mechanism to avoid duplicate embedding API calls
- Numpy-based operations
"""

import numpy as np
import time
from .GPTWrapper import _client

class Text_Embedding_Ada:
    """
    Text embedding class using OpenAI's text-embedding-ada-002.
    """

    def __init__(self, model="text-embedding-ada-002"):
        self.model = model
        self.client = _client
        self.embedding_cache = {}

    def get_embedding(self, text):
        """
        Get embedding for text. Returns numpy array shaped (1, 1, dim).
        """
        text = text.replace("\n", " ")

        if text in self.embedding_cache:
            return self.embedding_cache[text]

        ret = None
        wait = 5
        max_retries = 10

        for attempt in range(max_retries):
            try:
                response = self.client.embeddings.create(
                    input=[text],
                    model=self.model
                )
                embedding_values = response.data[0].embedding
                ret = np.array(embedding_values, dtype=np.float32).reshape(1, 1, -1)
                break
            except Exception as e:
                error_msg = str(e).lower()
                if "rate" in error_msg or "429" in error_msg:
                    wait_time = wait * (2 ** attempt)
                    print(f"Embedding rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"Embedding error: {e}. Retrying in {wait}s...")
                    time.sleep(wait)

        if ret is None:
            raise RuntimeError(f"Failed to get embedding after {max_retries} retries")

        self.embedding_cache[text] = ret
        return ret