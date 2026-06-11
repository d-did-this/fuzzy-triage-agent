with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Stretch out the progress bar
old_progress = '''.progress-bar { display: flex; align-items: center; gap: 15px; position: relative; }'''
new_progress = '''.progress-bar { display: flex; align-items: center; justify-content: space-between; width: 350px; position: relative; }'''
if old_progress in content:
    content = content.replace(old_progress, new_progress)

# 2. Fix naming
content = content.replace("HealthAgent Companion", "HealthAgent AI Nurse")
content = content.replace("AI Companion", "AI Nurse")

# 3. Fix the "Redo Assessment" bug by adding a timestamp to `data` in `generateReport()`
import re
old_generate = '''        let data = {
            name: document.getElementById('name').value.trim() || "Patient",
            hb: parseFloat(document.getElementById('hb_text').value),
            wbc: parseFloat(document.getElementById('wbc_text').value),
            plt: parseFloat(document.getElementById('plt_text').value),
            neu: parseFloat(document.getElementById('neu_text').value),
            mcv: parseFloat(document.getElementById('mcv_text').value),
            rdw: parseFloat(document.getElementById('rdw_text').value),
            egfr: parseFloat(document.getElementById('egfr_text').value),
            creat: parseFloat(document.getElementById('creat_text').value),
            action: "generate"
        };'''

new_generate = '''        let data = {
            name: document.getElementById('name').value.trim() || "Patient",
            hb: parseFloat(document.getElementById('hb_text').value),
            wbc: parseFloat(document.getElementById('wbc_text').value),
            plt: parseFloat(document.getElementById('plt_text').value),
            neu: parseFloat(document.getElementById('neu_text').value),
            mcv: parseFloat(document.getElementById('mcv_text').value),
            rdw: parseFloat(document.getElementById('rdw_text').value),
            egfr: parseFloat(document.getElementById('egfr_text').value),
            creat: parseFloat(document.getElementById('creat_text').value),
            action: "generate",
            run_id: Date.now()
        };'''

if old_generate in content:
    content = content.replace(old_generate, new_generate)

# Also ensure Python ignores run_id
# We will do this in a separate step or just assume `app.py` filters it. 
# Wait, `app.py` does: `lab_data = {k: v for k, v in component_value.items() if k not in ["action", "name"]}`
# So it will pass `run_id` to `fuzzy_engine.assess_patient()`.
# This will crash fuzzy_engine because it only expects the 8 lab values!
# We MUST modify app.py to ignore run_id.

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

old_filter = '''lab_data = {k: v for k, v in component_value.items() if k not in ["action", "name"]}'''
new_filter = '''lab_data = {k: v for k, v in component_value.items() if k not in ["action", "name", "run_id"]}'''
if old_filter in app_content:
    app_content = app_content.replace(old_filter, new_filter)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("SUCCESS")
