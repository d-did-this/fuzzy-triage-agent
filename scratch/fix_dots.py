with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the CSS for bigger progress dots
old_css = '''.progress-dot { width: 24px; height: 24px; border-radius: 50%; background: #1e293b; border: 2px solid #334155; transition: all 0.4s ease; z-index: 1; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; color: #94a3b8; }'''

new_css = '''.progress-dot { width: 36px; height: 36px; border-radius: 50%; background: #1e293b; border: 2px solid #334155; transition: all 0.4s ease; z-index: 1; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; color: #94a3b8; }'''

if old_css in content:
    content = content.replace(old_css, new_css)

# 2. Update the HTML for the final dot
old_html = '''<div class="progress-dot" id="dot-4">4</div>'''
new_html = '''<div class="progress-dot" id="dot-4" style="font-size: 20px;">🏁</div>'''

if old_html in content:
    content = content.replace(old_html, new_html)

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
