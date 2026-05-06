import json

for lang in ['urdu', 'pashto']:
    with open(f'results_{lang}_gpt55.json', 'r', encoding='utf-8') as f:
        d = json.load(f)
    
    jailbroken = sum(1 for r in d.values() for v in r['variants'] if not v['refused'])
    total = sum(len(r['variants']) for r in d.values())
    print(f"\n{'='*60}")
    print(f"{lang.upper()} - ASR: {jailbroken}/{total} = {jailbroken/total*100:.1f}%")
    print(f"{'='*60}")
    
    for pid, res in d.items():
        # Find best (first jailbroken, or first variant)
        best = None
        for v in res['variants']:
            if not v['refused']:
                best = v
                break
        if not best:
            best = res['variants'][0]
        
        status = "JAILBROKEN" if not best['refused'] else "REFUSED"
        goal_local = res.get('goal_ur', res.get('goal_ps', ''))
        print(f"\n--- {pid} [{status}] ---")
        print(f"EN: {res['goal_en']}")
        print(f"LOCAL: {goal_local}")
        print(f"VARIANT: {best['variant']}")
        print(f"WORDGAME: {best['wordgame_prompt'][:100]}...")
        print(f"RESPONSE: {best['response'][:200]}...")
