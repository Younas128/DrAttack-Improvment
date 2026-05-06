"""
GPT API Wrapper: Interface for OpenAI GPT models (GPT-4, GPT-4o, GPT-3.5-turbo)

This module provides a unified wrapper around OpenAI's ChatCompletion API using the modern >=1.0.0 SDK:
- Handles authentication via API key from config file
- Implements retry logic with exponential backoff for rate limiting
- Supports both single and multi-turn conversations
"""

import os
import time
from pathlib import Path
from openai import OpenAI, RateLimitError, APIError, APITimeoutError

def _load_api_key():
    """Load OpenAI API key from file or environment variable."""
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key.strip()

    possible_paths = [
        Path(__file__).parent.parent.parent / "api_keys" / "openai_key.txt",
        Path("api_keys/openai_key.txt"),
        Path("../../api_keys/openai_key.txt"),
    ]
    for path in possible_paths:
        if path.exists():
            with open(path, "r") as f:
                return f.read().strip()

    raise FileNotFoundError("OpenAI API key not found. Create api_keys/openai_key.txt")

_client = OpenAI(api_key=_load_api_key())

class GPTAPIWrapper:
    def __init__(self, model="gpt-4o-mini", max_tokens=2048):
        self.name = "openai-gpt"
        self.model = model
        self.max_tokens = max_tokens
        self.client = _client

    def __call__(self, prompt_list, verbose=True):
        if len(prompt_list) == 1:
            return self._single_turn(prompt_list[0], verbose=verbose)
        else:
            return self._multi_turn(prompt_list, verbose=verbose)

    def _single_turn(self, prompt, verbose=True, num_retries=10, wait=5):
        if verbose:
            print(f"Calling OpenAI ({self.model})... Input length: {len(prompt)}")

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        return self._send_request(messages, verbose, num_retries, wait)

    def _multi_turn(self, prompt_list, verbose=True, num_retries=10, wait=5):
        if verbose:
            print(f"Calling OpenAI ({self.model}) multi-turn... {len(prompt_list)} messages")

        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for i, prompt in enumerate(prompt_list):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": prompt})

        return self._send_request(messages, verbose, num_retries, wait)

    def _send_request(self, messages, verbose, num_retries, wait):
        for attempt in range(num_retries):
            try:
                kwargs = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 1.0 if ('gpt-5' in self.model or 'o1' in self.model) else 0.0,
                    "max_tokens": self.max_tokens
                }
                
                if 'gpt-5' in self.model or 'gpt-4o' in self.model or 'o1' in self.model:
                    kwargs['max_completion_tokens'] = kwargs.pop('max_tokens')

                response = self.client.chat.completions.create(**kwargs)
                
                if response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content.strip()
                return "Error: Empty response from model."
            
            except RateLimitError as e:
                wait_time = wait * (2 ** attempt)
                if verbose:
                    print(f"Rate limited. Waiting {wait_time}s... (attempt {attempt+1}/{num_retries})")
                time.sleep(wait_time)
            except APITimeoutError as e:
                if verbose:
                    print(f"Timeout. Waiting {wait}s... (attempt {attempt+1}/{num_retries})")
                time.sleep(wait)
            except APIError as e:
                error_str = str(e)
                # Non-retryable safety blocks from the API
                non_retryable = ['invalid_prompt', 'cyber_policy', 'content_policy',
                                 'safety reasons', 'flagged for possible']
                if any(code in error_str for code in non_retryable):
                    if verbose:
                        print(f"[BLOCKED] Content safety block (non-retryable): {e}")
                    return "I'm sorry, but I can't assist with that request."
                if verbose:
                    print(f"[ERROR] API Error: {e}. Retrying...")
                time.sleep(wait)
            except Exception as e:
                if verbose:
                    print(f"[ERROR] {e}. Waiting {wait}s... (attempt {attempt+1}/{num_retries})")
                time.sleep(wait)

        return "Sorry, OpenAI failed to respond after multiple retries."