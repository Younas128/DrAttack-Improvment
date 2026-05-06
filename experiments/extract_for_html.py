import json

d = json.load(open("cache/scores_gpt-5.5.json"))

for i, (goal, data) in enumerate(d.items()):
    print(f"=== PROMPT {i+1} ===")
    print(f"GOAL: {goal}")
    
    if isinstance(data, dict):
        # Get the best variant's response
        best_key = None
        best_resp = ""
        best_score = -1
        
        for vk, vv in data.items():
            if isinstance(vv, dict):
                for sk, sv in vv.items():
                    if isinstance(sv, dict) and "response" in sv:
                        if sv.get("score", 0) > best_score:
                            best_score = sv["score"]
                            best_key = vk
                            best_resp = sv["response"]
        
        print(f"VARIANT: {best_key}")
        print(f"SCORE: {best_score}")
        print(f"RESPONSE_START")
        print(best_resp)
        print(f"RESPONSE_END")
    print()
