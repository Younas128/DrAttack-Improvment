"""
Model Loader: Initialize and manage different types of LLM backends

This module handles:
- Initializing API-based models (Gemini) via wrapper classes
- Optionally loading open-source models (Llama2, Vicuna) from HuggingFace
- Optionally initializing GPT models via OpenAI API
- Setting up conversation templates for each model
- Managing multi-processing worker threads for model inference

Supported Models:
  - API-based: gemini-2.0-flash, gemini-2.5-flash, gemini-2.5-pro
  - API-based (requires OpenAI key): gpt-4, gpt-3.5-turbo
  - Open-source (requires GPU): Llama-2-7b-chat, Llama-2-13b-chat, Vicuna-7B
"""

import os
import sys
from copy import deepcopy

from .GeminiWrapper import GeminiAPIWrapper

# Conditional imports for models that require additional dependencies
_torch_available = False
_fastchat_available = False
_gpt_available = False

try:
    import torch
    import torch.multiprocessing as mp
    _torch_available = True
except ImportError:
    pass

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    pass

try:
    from fastchat.model import get_conversation_template
    _fastchat_available = True
except ImportError:
    pass

from .GPTWrapper import GPTAPIWrapper
_gpt_available = True


class ModelWorker(object):

    def __init__(self, model_path, model_kwargs, tokenizer, conv_template, device):
        
        if "gemini" in model_path:
            self.model_name = "gemini"
            self.model = GeminiAPIWrapper(model_name=model_path)
            self.tokenizer = lambda x: x
            self.conv_template = "You are a helpful assistant."
            self.tasks = None
            self.results = None
            self.process = None

        elif "gpt" in model_path:
            if not _gpt_available:
                raise ImportError("GPT support requires OpenAI API key. Create api_keys/openai_key.txt")
            self.model_name = "gpt"
            self.model = GPTAPIWrapper(model=model_path)
            self.tokenizer = lambda x: x
            self.conv_template = "You are a helpful assistant."
            self.tasks = None
            self.results = None
            self.process = None

        elif "vicuna" in model_path:
            if not _torch_available:
                raise ImportError("Vicuna requires PyTorch. Install with: pip install torch")
            self.model_name = "vicuna"
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                trust_remote_code=True,
                **model_kwargs
            ).to(device).eval()
            self.tokenizer = tokenizer
            self.conv_template = conv_template
            self.tasks = mp.JoinableQueue()
            self.results = mp.JoinableQueue()
            self.process = None

        elif "llama" in model_path:
            if not _torch_available:
                raise ImportError("Llama requires PyTorch. Install with: pip install torch")
            self.model_name = "llama"
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                trust_remote_code=True,
                **model_kwargs
            ).to(device).eval()
            self.tokenizer = tokenizer
            self.conv_template = conv_template
            self.tasks = mp.JoinableQueue()
            self.results = mp.JoinableQueue()
            self.process = None

        else:
            raise ValueError(f"Unknown model path: {model_path}. Supported: gemini, gpt, vicuna, llama")

    @staticmethod
    def run(model, tasks, results):
        while True:
            task = tasks.get()
            if task is None:
                break
            ob, fn, args, kwargs = task
            if fn == "grad":
                with torch.enable_grad():
                    results.put(ob.grad(*args, **kwargs))
            else:
                with torch.no_grad():
                    if fn == "logits":
                        results.put(ob.logits(*args, **kwargs))
                    elif fn == "contrast_logits":
                        results.put(ob.contrast_logits(*args, **kwargs))
                    elif fn == "test":
                        results.put(ob.test(*args, **kwargs))
                    elif fn == "test_loss":
                        results.put(ob.test_loss(*args, **kwargs))
                    else:
                        results.put(fn(*args, **kwargs))
            tasks.task_done()

    def start(self):
        if self.tasks is not None and _torch_available:
            self.process = mp.Process(
                target=ModelWorker.run,
                args=(self.model, self.tasks, self.results)
            )
            self.process.start()
            print(f"Started worker {self.process.pid}")
        return self
    
    def stop(self):
        if self.tasks is not None:
            self.tasks.put(None)
            if self.process is not None:
                self.process.join()
            if _torch_available:
                torch.cuda.empty_cache()
        return self

    def __call__(self, ob, fn, *args, **kwargs):
        if self.tasks is not None:
            self.tasks.put((deepcopy(ob), fn, args, kwargs))
        return self

def get_worker(params, eval=False):

    if ('gpt' not in params.model_path) and ('gemini' not in params.model_path):
        # Open-source model path
        if not _torch_available:
            raise ImportError("Open-source models require PyTorch")
        if not _fastchat_available:
            raise ImportError("Open-source models require FastChat: pip install fschat==0.2.23")

        tokenizer = AutoTokenizer.from_pretrained(
            params.tokenizer_path,
            trust_remote_code=True,
            **params.tokenizer_kwarg
        )
        if 'oasst-sft-6-llama-30b' in params.tokenizer_path:
            tokenizer.bos_token_id = 1
            tokenizer.unk_token_id = 0
        if 'guanaco' in params.tokenizer_path:
            tokenizer.eos_token_id = 2
            tokenizer.unk_token_id = 0
        if 'llama-2' in params.tokenizer_path:
            tokenizer.pad_token = tokenizer.unk_token
            tokenizer.padding_side = 'left'
        if 'falcon' in params.tokenizer_path:
            tokenizer.padding_side = 'left'
        if not tokenizer.pad_token:
            tokenizer.pad_token = tokenizer.eos_token

        print(f"Loaded tokenizer")

        raw_conv_template = get_conversation_template(params.conversation_template)

        if raw_conv_template.name == 'zero_shot':
            raw_conv_template.roles = tuple(['### ' + r for r in raw_conv_template.roles])
            raw_conv_template.sep = '\n'
        elif raw_conv_template.name == 'llama-2':
            raw_conv_template.sep2 = raw_conv_template.sep2.strip()

        conv_template = raw_conv_template
        print(f"Loaded conversation template")
        worker = ModelWorker(
                params.model_path,
                params.model_kwarg,
                tokenizer,
                conv_template,
                params.device
            )

        if not eval:
            worker.start()

        print('Loaded target LLM model')
    
    else:
        # API-based model (Gemini or GPT)
        tokenizer = [None]
        worker = ModelWorker(
                params.model_path,
                None,
                None,
                None,
                None
            )
        print(f'Loaded API model: {params.model_path}')
    return worker