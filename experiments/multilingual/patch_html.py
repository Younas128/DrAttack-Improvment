import re

with open('js_data.txt', 'r', encoding='utf-8') as f:
    js_data = f.read()

with open('../index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace urduTexts
html = re.sub(r'let urduTexts\s*=\s*\{.*?\}\s*;?', '', html, flags=re.DOTALL)
# Replace urduTexts_gpt4
html = re.sub(r'let urduTexts_gpt4\s*=\s*\{.*?\}\s*;?', '', html, flags=re.DOTALL)
# Replace pashtoTexts
html = re.sub(r'let pashtoTexts\s*=\s*\{.*?\}\s*;?', '', html, flags=re.DOTALL)
# Replace pashtoTexts_gpt4
html = re.sub(r'let pashtoTexts_gpt4\s*=\s*\{.*?\}\s*;?', '', html, flags=re.DOTALL)

# Find where to insert (before function handleChange)
insert_pos = html.find('function handleChange(')
if insert_pos == -1:
    print('Could not find insert pos')
else:
    html = html[:insert_pos] + js_data + '\n\n  ' + html[insert_pos:]
    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated index.html successfully')
