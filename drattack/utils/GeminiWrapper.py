"""
Gemini API Wrapper: Interface for Google's Gemini models (2.0/2.5 series)

This module provides a unified wrapper around Google's Gen AI SDK:
- Handles authentication via API key from config file or environment variable
- Implements support for Gemini 2.0 Flash, 2.5 Flash, and 2.5 Pro models
- Manages API interactions, retry logic, and response formatting
- Handles Gemini-specific safety blocks and error responses
- Supports both single-turn and multi-turn conversations

Supported Models: gemini-2.0-flash, gemini-2.5-flash, gemini-2.5-pro
"""

import os
import time
from pathlib import Path
from google import genai
from google.genai import types


def _load_api_key():
    """Load Google API key from file or environment variable."""
    # Try environment variable first
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()

    # Try common file locations
    possible_paths = [
        Path(__file__).parent.parent.parent / "api_keys" / "google_api_key.txt",
        Path("api_keys/google_api_key.txt"),
        Path("../../api_keys/google_api_key.txt"),
    ]
    for path in possible_paths:
        if path.exists():
            with open(path, "r") as f:
                return f.read().strip()

    raise FileNotFoundError(
        "Google API key not found. Set GOOGLE_API_KEY environment variable "
        "or create api_keys/google_api_key.txt"
    )


# Load API key and initialize client
GOOGLE_API_KEY = _load_api_key()
_client = genai.Client(api_key=GOOGLE_API_KEY)


class GeminiAPIWrapper:
    """Wrapper for Google Gemini API matching the DrAttack interface."""

    def __init__(self, model_name="gemini-2.0-flash", max_tokens=2048):

        # Support for attack framework
        self.name = "google-gemini"

        # Normalize model name
        if model_name in ("gemini", "gemini-pro"):
            self.model_name = "gemini-2.0-flash"  # default to flash
        elif not model_name.startswith("gemini-"):
            self.model_name = f"gemini-{model_name}"
        else:
            self.model_name = model_name

        self.max_tokens = max_tokens
        self.client = _client

        # Safety settings - set to least restrictive for research
        self.safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_NONE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_NONE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_NONE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_NONE",
            ),
        ]

    def __call__(self, prompt_list, verbose=True):
        """
        Send prompts to Gemini and get response.
        
        For single message: prompt_list = ["message"]
        For multi-turn: prompt_list = ["user1", "assistant1", "user2"]
        """
        if len(prompt_list) == 1:
            return self._single_turn(prompt_list[0], verbose=verbose)
        else:
            return self._multi_turn(prompt_list, verbose=verbose)

    def _single_turn(self, prompt, verbose=True, num_retries=10, wait=5):
        """Send a single prompt to Gemini."""
        if verbose:
            print(f"Calling Gemini ({self.model_name})... Input length: {len(prompt)}")

        for attempt in range(num_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=self.max_tokens,
                        safety_settings=self.safety_settings,
                    ),
                )

                # Check if response was blocked
                if response.candidates and response.candidates[0].content:
                    text = response.text
                    if text:
                        return text.strip()

                # Response was blocked by safety filters
                if verbose:
                    print("Gemini blocked the response (safety filter)")
                return "I cannot assist with that request."

            except Exception as e:
                error_msg = str(e).lower()
                if "blocked" in error_msg or "safety" in error_msg:
                    if verbose:
                        print(f"Gemini safety block: {e}")
                    return "I cannot assist with that request."
                elif "rate" in error_msg or "quota" in error_msg or "429" in error_msg:
                    wait_time = wait * (2 ** attempt)
                    if verbose:
                        print(f"Rate limited. Waiting {wait_time}s... (attempt {attempt+1}/{num_retries})")
                    time.sleep(wait_time)
                else:
                    if verbose:
                        print(f"[ERROR] {e}. Waiting {wait}s... (attempt {attempt+1}/{num_retries})")
                    time.sleep(wait)

        return "Sorry, Gemini failed to respond after multiple retries."

    def _multi_turn(self, prompt_list, verbose=True, num_retries=10, wait=5):
        """Send a multi-turn conversation to Gemini."""
        if verbose:
            print(f"Calling Gemini ({self.model_name}) multi-turn... {len(prompt_list)} messages")

        # Build conversation contents
        contents = []
        for i, prompt in enumerate(prompt_list):
            if i % 2 == 0:
                contents.append(types.Content(
                    role="user",
                    parts=[types.Part(text=prompt)]
                ))
            else:
                contents.append(types.Content(
                    role="model",
                    parts=[types.Part(text=prompt)]
                ))

        for attempt in range(num_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        max_output_tokens=self.max_tokens,
                        safety_settings=self.safety_settings,
                    ),
                )

                if response.candidates and response.candidates[0].content:
                    text = response.text
                    if text:
                        return text.strip()

                if verbose:
                    print("Gemini blocked the multi-turn response (safety filter)")
                return "I cannot assist with that request."

            except Exception as e:
                error_msg = str(e).lower()
                if "blocked" in error_msg or "safety" in error_msg:
                    if verbose:
                        print(f"Gemini safety block: {e}")
                    return "I cannot assist with that request."
                elif "rate" in error_msg or "quota" in error_msg or "429" in error_msg:
                    wait_time = wait * (2 ** attempt)
                    if verbose:
                        print(f"Rate limited. Waiting {wait_time}s... (attempt {attempt+1}/{num_retries})")
                    time.sleep(wait_time)
                else:
                    if verbose:
                        print(f"[ERROR] {e}. Waiting {wait}s... (attempt {attempt+1}/{num_retries})")
                    time.sleep(wait)

        return "Sorry, Gemini failed to respond after multiple retries."


class GeminiEmbedding:
    """
    Gemini-based text embedding using text-embedding-004.
    Drop-in replacement for OpenAI Ada-002 embeddings.
    """

    def __init__(self, model="text-embedding-004"):
        self.model = model
        self.client = _client
        self.embedding_cache = {}

    def get_embedding(self, text):
        """
        Get embedding for text. Returns numpy array shaped (1, 1, dim).
        Compatible with the original Ada-002 interface.
        """
        import numpy as np

        text = text.replace("\n", " ")

        # Memoization
        if text in self.embedding_cache:
            return self.embedding_cache[text]

        ret = None
        wait = 5
        max_retries = 10

        for attempt in range(max_retries):
            try:
                response = self.client.models.embed_content(
                    model=self.model,
                    contents=text,
                )
                # Extract embedding values
                embedding_values = response.embeddings[0].values
                ret = np.array(embedding_values, dtype=np.float32).reshape(1, 1, -1)
                break

            except Exception as e:
                error_msg = str(e).lower()
                if "rate" in error_msg or "quota" in error_msg or "429" in error_msg:
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
