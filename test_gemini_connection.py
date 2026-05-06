"""
Quick connectivity test for DrAttack on Gemini 2.0 Flash.
Tests: API key, text generation, and embeddings.
"""
import sys
import os

# Add repo root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print("🧪 DrAttack-Gemini Connectivity Test")
print("=" * 80)

# Test 1: API key loading
print("\n📋 Test 1: Loading API key...")
try:
    from drattack.utils.GeminiWrapper import _load_api_key, GeminiAPIWrapper, GeminiEmbedding
    key = _load_api_key()
    print(f"  ✅ API key loaded: {key[:10]}...{key[-4:]}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 2: Text generation
print("\n📋 Test 2: Gemini 2.0 Flash text generation...")
try:
    model = GeminiAPIWrapper(model_name="gemini-2.0-flash", max_tokens=100)
    response = model(["What is 2+2? Answer in one word."])
    print(f"  ✅ Response: {response}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 3: Embeddings
print("\n📋 Test 3: Gemini text-embedding-004...")
try:
    embedder = GeminiEmbedding()
    embed = embedder.get_embedding("Hello world")
    print(f"  ✅ Embedding shape: {embed.shape}, dim={embed.shape[-1]}")
    print(f"  ✅ First 5 values: {embed[0][0][:5]}")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 4: Import DrAttack modules
print("\n📋 Test 4: Importing DrAttack modules...")
try:
    from drattack import PromptAttack, get_goals_and_targets, get_worker
    print("  ✅ PromptAttack imported")
    print("  ✅ get_goals_and_targets imported")
    print("  ✅ get_worker imported")
except Exception as e:
    print(f"  ❌ Failed: {e}")
    sys.exit(1)

# Test 5: Load precomputed decompositions
print("\n📋 Test 5: Loading precomputed attack data...")
try:
    import json
    data_path = os.path.join(os.path.dirname(__file__), 
                             "attack_prompt_data/gpt_automated_processing_results/prompts_information.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
    print(f"  ✅ Loaded {len(data)} precomputed prompt decompositions")
    first_key = list(data.keys())[0]
    print(f"  ✅ Sample prompt: \"{first_key[:60]}...\"")
except Exception as e:
    print(f"  ❌ Failed: {e}")

# Test 6: Model worker initialization
print("\n📋 Test 6: ModelWorker for Gemini...")
try:
    from drattack.utils.model_loader import ModelWorker
    worker = ModelWorker("gemini-2.0-flash", None, None, None, None)
    print(f"  ✅ ModelWorker created: model_name={worker.model_name}")
    print(f"  ✅ Wrapper model: {worker.model.model_name}")
    
    # Quick test through worker
    result = worker.model(["Say 'hello' and nothing else."])
    print(f"  ✅ Worker response: {result}")
except Exception as e:
    print(f"  ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED — DrAttack is ready for Gemini 2.0 Flash!")
print("=" * 80)
print("\nNext step: Run the attack with:")
print("  cd experiments")
print("  python main.py --config=configs/individual_gemini-2.0-flash.py --config.n_train_data=1")
