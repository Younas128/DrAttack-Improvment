import json

d = json.load(open("cache/scores_gpt-5.5.json"))
for i, (k, v) in enumerate(d.items()):
    print(f"=== GOAL {i+1}: {k} ===")
    if isinstance(v, dict):
        for subk, subv in v.items():
            val_str = str(subv)
            if len(val_str) > 500:
                val_str = val_str[:500] + "..."
            print(f"  {subk}: {val_str}")
    else:
        print(f"  Value: {str(v)[:500]}")
    print()
