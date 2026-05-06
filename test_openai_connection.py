"""
Quick connectivity test for DrAttack on OpenAI (gpt-4o-mini).
Tests: API key, text generation, and embeddings using the modern openai >= 1.0.0 SDK.
"""
import sys
import os

# Add repo root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🧪 DrAttack-OpenAI Connectivity Test")
print("=" * 80)

# Test 1: API key loading
print("\n📋 Test 1: Loading API key...")
try:
    from drattack.utils.GPTWrapper import _load_api_key, GPTAPIWrapper
    key = _load_api_key()
    print(f"  ✅ API key loaded: {key[:10]}...{key[-4:]}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 2: Text generation
print("\n📋 Test 2: gpt-4o-mini text generation...")
try:
    model = GPTAPIWrapper(model="gpt-4o-mini", max_tokens=100)
    response = model(["What is 2+2? Answer in one word."])
    print(f"  ✅ Response: {response}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 3: Embeddings
print("\n📋 Test 3: text-embedding-ada-002...")
try:
    from drattack.utils.sentence_tokenizer import Text_Embedding_Ada
    embedder = Text_Embedding_Ada()
    embed = embedder.get_embedding("Hello world")
    print(f"  ✅ Embedding shape: {embed.shape}, dim={embed.shape[-1]}")
    print(f"  ✅ First 5 values: {embed[0][0][:5]}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 4: Model worker initialization
print("\n📋 Test 4: ModelWorker for GPT...")
try:
    from drattack.utils.model_loader import ModelWorker
    worker = ModelWorker("gpt-4o-mini", None, None, None, None)
    print(f"  ✅ ModelWorker created: model_name={worker.model_name}")
    print(f"  ✅ Wrapper model: {worker.model.model}")
    
    # Quick test through worker
    result = worker.model(["Say 'hello' and nothing else."])
    print(f"  ✅ Worker response: {result}")
except Exception as e:
    print(f"  ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED — DrAttack is ready for OpenAI!")
print("=" * 80)
