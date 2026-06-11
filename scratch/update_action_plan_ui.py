import re

# 1. Update app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

old_system_msg = 'system_msg = "You are an AI Triage Agent. Given a patient\'s lab report and their Fuzzy Risk Score (0-100), output a highly concise, bulleted list of 2-4 critical recommended clinical actions. Output ONLY the HTML `<li>` tags containing the text (e.g. `<li>Drink more water</li>`). No markdown blocks, no intro, no outro."\n'

new_system_msg = '''system_msg = """You are an AI Triage Agent. Given a patient's lab report and their Fuzzy Risk Score (0-100), output an HTML action plan.
Follow EXACTLY this structure, returning ONLY valid HTML:
<div style="background: rgba(15,23,42,0.6); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
    <h3 style="margin:0 0 10px 0; color: #38bdf8;">Risk Score Analysis</h3>
    <p style="margin:0; color:#cbd5e1; line-height: 1.5;">[Brief explanation of why the overall Risk Score is what it is based on the report]</p>
</div>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
    <!-- For EVERY problematic (abnormal) biomarker, generate a card -->
    <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border-left: 4px solid #ef4444;">
        <h4 style="margin:0 0 5px 0; color: white;">[Biomarker Name] <span style="color: #ef4444; font-size: 14px;">([High/Low])</span></h4>
        <p style="margin:0 0 10px 0; color:#cbd5e1; font-size: 13px;">[Brief explanation of why this specific value is problematic]</p>
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px;">
            <strong style="color: #10b981; font-size: 12px; text-transform: uppercase;">Recommended Action</strong>
            <p style="margin: 5px 0 0 0; color: #f8fafc; font-size: 13px;">[1 specific action step]</p>
        </div>
    </div>
</div>
Do not include markdown codeblocks (```html), just the raw HTML code. Do not output anything else."""\n'''

app_content = app_content.replace(old_system_msg, new_system_msg)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

# 2. Update index.html
with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Change action-list ul to div
old_action_list = '''                    <h2 style="font-size: 32px; margin-bottom: 20px;"><strong>Recommended</strong> Actions</h2>
                    <ul class="findings-list full-column" id="action-list">
                        <!-- Populated by JS -->
                    </ul>'''

new_action_list = '''                    <h2 style="font-size: 32px; margin-bottom: 20px;"><strong>AI Recommended</strong> Actions</h2>
                    <div id="action-list" style="width: 100%;">
                        <!-- Populated by JS -->
                    </div>'''
idx_content = idx_content.replace(old_action_list, new_action_list)

# Fix Rule Count text
old_rule_count = '''document.getElementById('admin-rules-count').innerText = `Displaying ${ruleCount} Rule Thresholds`;'''
new_rule_count = '''document.getElementById('admin-rules-count').innerText = `Displaying ${ruleCount} Fuzzy Category Thresholds`;'''
idx_content = idx_content.replace(old_rule_count, new_rule_count)

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(idx_content)

print("SUCCESS")
