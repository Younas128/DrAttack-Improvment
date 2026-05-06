import re

with open('../../index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the hardcoded limits in handleChange
html = html.replace('if (i >= 7) return;', 'if (i >= modelTexts[selectedExample].length) return;')
html = html.replace(
    "const color = (i === 2) ? 'rgba(156,211,251,255)' : (i === 6) ? 'rgba(244,181,173,255)' : null;",
    "const color = (i === 2) ? 'rgba(156,211,251,255)' : (i === modelTexts[selectedExample].length - 1) ? 'rgba(244,181,173,255)' : null;"
)

with open('../../index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Patched index.html handleChange limits')
