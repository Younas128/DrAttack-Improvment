import re

with open('js_data_multiturn.txt', 'r', encoding='utf-8') as f:
    js_data = f.read()

with open('../../index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace urduTexts
html = re.sub(r'let urduTexts\s*=\s*\{.*?\}\s*;?', '', html, flags=re.DOTALL)
# Replace urduTexts_gpt4
html = re.sub(r'let urduTexts_gpt4\s*=\s*\{.*?\}\s*;?', '', html, flags=re.DOTALL)
# Replace pashtoTexts
html = re.sub(r'let pashtoTexts\s*=\s*\{.*?\}\s*;?', '', html, flags=re.DOTALL)
# Replace pashtoTexts_gpt4
html = re.sub(r'let pashtoTexts_gpt4\s*=\s*\{.*?\}\s*;?', '', html, flags=re.DOTALL)

# Insert new JS data
insert_pos = html.find('function handleChange(')
if insert_pos != -1:
    html = html[:insert_pos] + js_data + '\n\n  ' + html[insert_pos:]

# Now modify handleChange to support up to 6 elements
# find "if (i >= 5) return;" and replace with "if (i >= 7) return;"
html = html.replace('if (i >= 5) return;', 'if (i >= 7) return;')

# We want color change for final assistant response (which is now i===6)
# Original: const color = (i === 2) ? 'rgba(156,211,251,255)' : (i === 4) ? 'rgba(244,181,173,255)' : null;
# New: const color = (i === 2) ? 'rgba(156,211,251,255)' : (i === 6) ? 'rgba(244,181,173,255)' : null;
html = html.replace(
    "const color = (i === 2) ? 'rgba(156,211,251,255)' : (i === 4) ? 'rgba(244,181,173,255)' : null;",
    "const color = (i === 2) ? 'rgba(156,211,251,255)' : (i === 6) ? 'rgba(244,181,173,255)' : null;"
)

with open('../../index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated index.html successfully')
