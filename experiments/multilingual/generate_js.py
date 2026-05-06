import json
import os

with open('results_urdu_v2_gpt4omini.json', 'r', encoding='utf-8') as f: u4 = json.load(f)
with open('results_urdu_v2_gpt55.json', 'r', encoding='utf-8') as f: u5 = json.load(f)
with open('results_pashto_v2_gpt4omini.json', 'r', encoding='utf-8') as f: p4 = json.load(f)
with open('results_pashto_v2_gpt55.json', 'r', encoding='utf-8') as f: p5 = json.load(f)

def clean(s):
    return s.replace('\n', '<br/>').replace('"', '&quot;').replace("'", "&apos;").replace('\r', '')

with open('js_data.txt', 'w', encoding='utf-8') as out:
    out.write('  let urduTexts_gpt4 = {\n')
    for i in range(1,7):
        p = f'prompt{i}'
        r = u4[p]
        out.write(f'      {p}: ["TBD", "<b>{r["goal_ur"]}</b>", "{clean(u5[p]["response"][:100])}... (REFUSED in GPT-5.5)", "{clean(r["wordgame"])}<br/><br/>{clean(r["task_prompt"])}", "<span style=\'color:#e74c3c;font-weight:bold;\'>&#x26A0; JAILBROKEN (GPT-4o-mini Urdu):</span><br/>{clean(r["response"])}"],\n')
    out.write('  };\n\n')

    out.write('  let urduTexts = {\n')
    for i in range(1,7):
        p = f'prompt{i}'
        r = u5[p]
        out.write(f'      {p}: ["TBD", "<b>{r["goal_ur"]}</b>", "{clean(r["response"][:100])}", "{clean(r["wordgame"])}<br/><br/>{clean(r["task_prompt"])}", "<span style=\'color:#2ecc71;font-weight:bold;\'>&#x2705; REFUSED (GPT-5.5 Urdu):</span><br/>{clean(r["response"])}"],\n')
    out.write('  };\n\n')

    out.write('  let pashtoTexts_gpt4 = {\n')
    for i in range(1,7):
        p = f'prompt{i}'
        r = p4[p]
        out.write(f'      {p}: ["TBD", "<b>{r["goal_ps"]}</b>", "{clean(p5[p]["response"][:100])}... (REFUSED in GPT-5.5)", "{clean(r["wordgame"])}<br/><br/>{clean(r["task_prompt"])}", "<span style=\'color:#e74c3c;font-weight:bold;\'>&#x26A0; JAILBROKEN (GPT-4o-mini Pashto):</span><br/>{clean(r["response"])}"],\n')
    out.write('  };\n\n')
    
    out.write('  let pashtoTexts = {\n')
    for i in range(1,7):
        p = f'prompt{i}'
        r = p5[p]
        out.write(f'      {p}: ["TBD", "<b>{r["goal_ps"]}</b>", "{clean(r["response"][:100])}", "{clean(r["wordgame"])}<br/><br/>{clean(r["task_prompt"])}", "<span style=\'color:#2ecc71;font-weight:bold;\'>&#x2705; REFUSED (GPT-5.5 Pashto):</span><br/>{clean(r["response"])}"],\n')
    out.write('  };\n')
