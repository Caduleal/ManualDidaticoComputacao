import re
file_path = 'Manual.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(qualquer lugar\.\s*</p>\s*)</div>'
replacement = r'\1 <p class="text-brand-800 text-justify font-normal mt-2 text-[10px] bg-slate-50 p-2 rounded border border-slate-100">\n        A revisão e otimização do código-fonte foram realizadas com o auxílio da ferramenta Gemini (Google, 2026).\n       </p>\n      </div>'

new_content = re.sub(pattern, replacement, content)

if new_content != content:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('replaced')
else:
    print('not found')
