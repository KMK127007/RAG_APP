# llm.py
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from settings import LLM_MODEL, LLM_DEVICE, MCP_ENDPOINT
import requests
import logging

class LLMWrapper:
    def __init__(self, model_name=LLM_MODEL, device=LLM_DEVICE):
        self.model_name = model_name
        self.device = device
        # load model & tokenizer lazily to avoid long startup time if not needed
        print("LLM wrapper initialised with model:", model_name)

    def _load(self):
        if not hasattr(self, "generator"):
            print("Loading LLM model (this may take a while)...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, use_fast=True)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            # push to device if supported; keep simple here
            self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device_map="auto" if self.device == "cuda" else None)

    def generate(self, prompt, max_new_tokens=512, temperature=0.2):
        # If you have a MCP server, route via MCP instead (stub)
        if MCP_ENDPOINT:
            try:
                payload = {"prompt": prompt, "max_tokens": max_new_tokens}
                r = requests.post(MCP_ENDPOINT, json=payload, timeout=5)
                if r.ok:
                    return r.json().get("text")
            except Exception as e:
                logging.info("MCP call failed, falling back to local model: %s", e)
        # fallback local
        self._load()
        out = self.generator(prompt, max_new_tokens=max_new_tokens, do_sample=False)
        text = out[0].get("generated_text", "")
        return text
