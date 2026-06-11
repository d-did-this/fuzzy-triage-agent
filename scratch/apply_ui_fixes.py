import re

# 1. FIX fuzzy_engine.py
with open('fuzzy_engine.py', 'r', encoding='utf-8') as f:
    f_content = f.read()

old_get_thresholds = '''                gt_0 = np.where(mf > 0.001)[0]
                eq_1 = np.where(mf >= 0.999)[0]
                
                if len(gt_0) == 0 or len(eq_1) == 0:
                    thresholds[var_name][cat_name] = "Unknown"
                    continue'''

new_get_thresholds = '''                gt_0 = np.where(mf > 0.001)[0]
                max_val = np.max(mf)
                eq_1 = np.where(mf >= (max_val - 0.001))[0]
                
                if len(gt_0) == 0 or len(eq_1) == 0:
                    thresholds[var_name][cat_name] = "Unknown"
                    continue'''

if old_get_thresholds in f_content:
    f_content = f_content.replace(old_get_thresholds, new_get_thresholds)
    with open('fuzzy_engine.py', 'w', encoding='utf-8') as f:
        f.write(f_content)
else:
    print("WARNING: Could not find old_get_thresholds in fuzzy_engine.py")

# 2. FIX index.html
with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    h_content = f.read()

# Phase 1: CSS Animation & Indicator logic
pulse_css = '''
<style>
@keyframes pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); transform: scale(1); }
    50% { box-shadow: 0 0 15px 10px rgba(59, 130, 246, 0); transform: scale(1.05); }
    100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); transform: scale(1); }
}
.pulse-active {
    animation: pulse-glow 1.5s infinite !important;
    background: linear-gradient(135deg, #10b981, #059669) !important;
}
.ai-indicator-tooltip {
    position: absolute;
    top: 60px;
    right: 0;
    background: #f59e0b;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    display: none;
    animation: bounce 2s infinite;
    white-space: nowrap;
}
.ai-indicator-tooltip::after {
    content: '';
    position: absolute;
    top: -8px;
    right: 20px;
    border-width: 0 8px 8px 8px;
    border-style: solid;
    border-color: transparent transparent #f59e0b transparent;
}
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}
</style>
'''
if '@keyframes pulse-glow' not in h_content:
    h_content = h_content.replace('</head>', pulse_css + '\n</head>')

# Add tooltip to AI Nurse header button
old_ai_nurse_btn = '''<button onclick="toggleChat(true)" style="background: linear-gradient(135deg, #0ea5e9, #2563eb); border: none; color: white; padding: 10px 25px; border-radius: 12px; cursor: pointer; font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 600; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); transition: transform 0.2s;">
                💬 AI Nurse
            </button>'''
new_ai_nurse_btn = '''<div style="position: relative;">
                <button id="header-ai-btn" onclick="toggleChat(true)" style="background: linear-gradient(135deg, #0ea5e9, #2563eb); border: none; color: white; padding: 10px 25px; border-radius: 12px; cursor: pointer; font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 600; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); transition: transform 0.2s;">
                    💬 AI Nurse
                </button>
                <div id="ai-click-indicator" class="ai-indicator-tooltip">Click here to chat with AI Nurse to get more info!</div>
            </div>'''
if old_ai_nurse_btn in h_content:
    h_content = h_content.replace(old_ai_nurse_btn, new_ai_nurse_btn)
elif 'id="header-ai-btn"' not in h_content:
    print("WARNING: Could not find old_ai_nurse_btn")

# Remove bottom Chat button
old_bottom_buttons = '''                    <div style="display: flex; gap: 20px; margin-top: 30px;">
                        <button class="btn btn-next" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 10px; background: transparent; border: 1px solid rgba(255,255,255,0.2); box-shadow: none;" onclick="changeStep(-3)">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path></svg>
                            Redo Assessment
                        </button>
                        <button class="btn btn-generate" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 10px; background: linear-gradient(135deg, #a855f7, #9333ea); box-shadow: 0 10px 20px rgba(168, 85, 247, 0.3);" onclick="openChat()">
                            💬 Chat with AI Nurse
                        </button>
                        <button class="btn btn-generate" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 10px;" onclick="printReport()">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            Download Report
                        </button>
                    </div>'''
new_bottom_buttons = '''                    <div style="display: flex; gap: 20px; margin-top: 30px;">
                        <button class="btn btn-next" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 10px; background: transparent; border: 1px solid rgba(255,255,255,0.2); box-shadow: none;" onclick="changeStep(-3)">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"></polyline><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path></svg>
                            Redo Assessment
                        </button>
                        <button class="btn btn-generate" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 10px;" onclick="printReport()">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                            Download Report
                        </button>
                    </div>'''
if old_bottom_buttons in h_content:
    h_content = h_content.replace(old_bottom_buttons, new_bottom_buttons)

# Phase 3: Lower is better indicator
old_score_label = '''<div class="score-label">Score</div>'''
new_score_label = '''<div class="score-label">Score</div>
                                 <div style="font-size: 10px; color: rgba(255,255,255,0.5); margin-top: -2px;">(Lower is Better)</div>'''
if old_score_label in h_content:
    h_content = h_content.replace(old_score_label, new_score_label)

# Phase 4 & 5: Admin Panel UI updates
old_admin_box = '''           <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05);">
               <label style="color:#cbd5e1; font-size:16px; display:block; margin-bottom:10px;">🩺 Health Alert Preset:</label>
               <select id="admin_alert_preset" onchange="setHealthAlert()" style="width:100%; padding: 12px; background: rgba(15,23,42,0.8); color: white; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; font-size: 16px; margin-bottom: 10px;">
                   <option value="None">No Active Alerts (Normal)</option>
                   <option value="Dengue Outbreak">Dengue Outbreak (Endemic Level)</option>
                   <option value="Extreme Heatwave">Extreme Heatwave (Dehydration Risk)</option>
                   <option value="COVID-19 Spike">COVID-19 Spike</option>
               </select>
               <div style="font-size: 13px; color: #94a3b8;">Select an alert to dynamically alter the AI's clinical context.</div>
           </div>
           
           <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05);">
               <h3 style="color:white; margin-top:0; margin-bottom: 15px;">🧠 Agent Reflection Tools</h3>
               <button class="btn" style="width: 100%; background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #ef4444; margin-bottom: 10px;" onclick="triggerRuleFailure()">Simulate Rule Failure (Over-Correction)</button>
               <div style="display: flex; gap: 10px;">
                   <button class="btn" style="flex: 1; padding: 12px; font-size: 14px; background: rgba(59, 130, 246, 0.2); border-color: #3b82f6; color: #60a5fa;" onclick="openAdminLogs()">View Experience Logs</button>
                   <button class="btn" style="flex: 1; padding: 12px; font-size: 14px; background: rgba(16, 185, 129, 0.2); border-color: #10b981; color: #34d399;" onclick="openAdminRules()">View Active Rules</button>
               </div>
           </div>'''

new_admin_box = '''           <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05);">
               <label style="color:#cbd5e1; font-size:16px; display:block; margin-bottom:10px;">🩺 Health Alert Preset:</label>
               <select id="admin_alert_preset" onchange="checkCustomAlert()" style="width:100%; padding: 12px; background: rgba(15,23,42,0.8); color: white; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; font-size: 16px; margin-bottom: 10px;">
                   <option value="None">No Active Alerts (Normal)</option>
                   <option value="Dengue Outbreak">Dengue Outbreak (Endemic Level)</option>
                   <option value="Extreme Heatwave">Extreme Heatwave (Dehydration Risk)</option>
                   <option value="COVID-19 Spike">COVID-19 Spike</option>
                   <option value="Custom">Custom Situation...</option>
               </select>
               <textarea id="admin_custom_alert" placeholder="Enter custom health alert here..." style="display:none; width:100%; height:80px; margin-bottom: 10px; padding: 10px; font-family:inherit; background:rgba(0,0,0,0.2); color:white; border:1px solid rgba(255,255,255,0.1); border-radius:8px;" onchange="setHealthAlert()"></textarea>
               <div style="font-size: 13px; color: #94a3b8;">Select an alert to dynamically alter the AI's clinical context.</div>
           </div>
           
           <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05);">
               <h3 style="color:white; margin-top:0; margin-bottom: 15px;">🧠 Agent Reflection Tools</h3>
               
               <div style="background: rgba(239, 68, 68, 0.05); border-left: 3px solid #ef4444; padding: 12px; margin-bottom: 15px; border-radius: 0 8px 8px 0;">
                   <h4 style="margin: 0 0 5px 0; color: #fca5a5; font-size: 14px;">What does this do?</h4>
                   <p style="margin: 0; color: #cbd5e1; font-size: 12px; line-height: 1.4;">Simulating a rule failure forces the AI to reflect on a past mistake (e.g. over-correcting a threshold) so you can observe its self-correction logic in real-time.</p>
               </div>
               
               <button class="btn" style="width: 100%; background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #ef4444; margin-bottom: 15px;" onclick="triggerRuleFailure()">Simulate Rule Failure (Over-Correction)</button>
               
               <div style="display: flex; gap: 10px;">
                   <button class="btn" style="flex: 1; padding: 12px; font-size: 14px; background: rgba(59, 130, 246, 0.2); border-color: #3b82f6; color: #60a5fa;" onclick="openAdminLogs()">View Experience Logs</button>
                   <button class="btn" style="flex: 1; padding: 12px; font-size: 14px; background: rgba(16, 185, 129, 0.2); border-color: #10b981; color: #34d399;" onclick="openAdminRules()">View Active Rules</button>
               </div>
           </div>'''
if old_admin_box in h_content:
    h_content = h_content.replace(old_admin_box, new_admin_box)

old_rules_modal = '''       <!-- Rules Modal (Inside Admin) -->
       <div id="admin-rules-modal" style="display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #0f172a; padding: 30px; border-radius: 20px; width: 800px; max-height: 80vh; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 30px 60px rgba(0,0,0,0.6); z-index: 10001; flex-direction: column;">
           <h2 style="margin-top: 0; color: white; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">
               Active Fuzzy Thresholds
               <button onclick="document.getElementById('admin-rules-modal').style.display='none'" style="background:none; border:none; color:white; cursor:pointer; font-size:24px;">✕</button>
           </h2>
           <div style="overflow-y: auto; flex-grow: 1; margin-top: 15px;">
               <table style="width: 100%; border-collapse: collapse; color: #e2e8f0; font-size: 14px;">
                   <thead>
                       <tr style="background: rgba(255,255,255,0.05); text-align: left;">
                           <th style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">Variable</th>
                           <th style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">Category</th>
                           <th style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">Numerical Range [a, b, c, d]</th>
                       </tr>
                   </thead>
                   <tbody id="admin-rules-tbody">
                   </tbody>
               </table>
           </div>
       </div>'''
new_rules_modal = '''       <!-- Rules Modal (Inside Admin) -->
       <div id="admin-rules-modal" style="display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #0f172a; padding: 30px; border-radius: 20px; width: 800px; max-height: 80vh; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 30px 60px rgba(0,0,0,0.6); z-index: 10001; flex-direction: column;">
           <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">
               <div>
                   <h2 style="margin: 0; color: white;">Active Fuzzy Thresholds</h2>
                   <div id="admin-rules-count" style="color: #10b981; font-size: 14px; font-weight: bold; margin-top: 5px;">Displaying 0 Rules</div>
               </div>
               <button onclick="document.getElementById('admin-rules-modal').style.display='none'" style="background:none; border:none; color:white; cursor:pointer; font-size:24px; transition: color 0.2s;" onmouseover="this.style.color='#ef4444'" onmouseout="this.style.color='white'">✕</button>
           </div>
           
           <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; padding: 12px; margin-top: 15px; border-radius: 0 8px 8px 0;">
               <p style="margin: 0; color: #a7f3d0; font-size: 13px; line-height: 1.5;">This table displays the exact mathematical boundaries <strong>[Start, Peak Start, Peak End, End]</strong> that define what constitutes 'Low', 'Normal', or 'High' for each clinical variable. The AI can dynamically shift these thresholds in response to Health Alerts.</p>
           </div>
           
           <div style="overflow-y: auto; flex-grow: 1; margin-top: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); background: rgba(0,0,0,0.2);">
               <table style="width: 100%; border-collapse: collapse; color: #e2e8f0; font-size: 14px;" class="admin-table">
                   <thead>
                       <tr style="background: rgba(255,255,255,0.05); text-align: left; text-transform: uppercase; font-size: 12px; letter-spacing: 1px;">
                           <th style="padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); color:#94a3b8;">Variable</th>
                           <th style="padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); color:#94a3b8;">Category</th>
                           <th style="padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); color:#94a3b8;">Numerical Range [a, b, c, d]</th>
                       </tr>
                   </thead>
                   <tbody id="admin-rules-tbody">
                   </tbody>
               </table>
           </div>
       </div>
       <style>
           .admin-table tbody tr:nth-child(even) { background: rgba(255,255,255,0.02); }
           .admin-table tbody tr:hover { background: rgba(255,255,255,0.05); }
       </style>'''
if old_rules_modal in h_content:
    h_content = h_content.replace(old_rules_modal, new_rules_modal)

# JS Updates
old_js_admin = '''    function setHealthAlert() {
        let val = document.getElementById('admin_alert_preset').value;
        Streamlit.setComponentValue({action: "set_health_alert", health_alert: val});
    }'''
new_js_admin = '''    function checkCustomAlert() {
        let val = document.getElementById('admin_alert_preset').value;
        let customBox = document.getElementById('admin_custom_alert');
        if (val === "Custom") {
            customBox.style.display = "block";
        } else {
            customBox.style.display = "none";
            setHealthAlert();
        }
    }

    function setHealthAlert() {
        let presetVal = document.getElementById('admin_alert_preset').value;
        let finalVal = presetVal;
        if (presetVal === "Custom") {
            finalVal = document.getElementById('admin_custom_alert').value;
        }
        Streamlit.setComponentValue({action: "set_health_alert", health_alert: finalVal});
    }'''
if old_js_admin in h_content:
    h_content = h_content.replace(old_js_admin, new_js_admin)

old_open_rules = '''    function openAdminRules() {
        let tbody = document.getElementById('admin-rules-tbody');
        tbody.innerHTML = '';
        if(window.adminRules && Object.keys(window.adminRules).length > 0) {
            for(let varName in window.adminRules) {
                for(let cat in window.adminRules[varName]) {
                    let rangeStr = JSON.stringify(window.adminRules[varName][cat]);
                    let tr = document.createElement('tr');
                    tr.innerHTML = `<td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.05); font-weight:bold; color:#f8fafc;">${varName.toUpperCase()}</td>
                                    <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.05); color:#34d399;">${cat}</td>
                                    <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.05); font-family:monospace; color:#cbd5e1;">${rangeStr}</td>`;
                    tbody.appendChild(tr);
                }
            }
        } else {
            tbody.innerHTML = '<tr><td colspan="3" style="padding:20px; text-align:center;">No rules found.</td></tr>';
        }
        document.getElementById('admin-rules-modal').style.display = 'flex';
    }'''
new_open_rules = '''    function openAdminRules() {
        let tbody = document.getElementById('admin-rules-tbody');
        tbody.innerHTML = '';
        let ruleCount = 0;
        if(window.adminRules && Object.keys(window.adminRules).length > 0) {
            for(let varName in window.adminRules) {
                for(let cat in window.adminRules[varName]) {
                    ruleCount++;
                    let rangeStr = JSON.stringify(window.adminRules[varName][cat]);
                    let catColor = cat === 'Severe' || cat === 'High' ? '#ef4444' : (cat === 'Low' ? '#3b82f6' : '#10b981');
                    let tr = document.createElement('tr');
                    tr.innerHTML = `<td style="padding:15px; border-bottom:1px solid rgba(255,255,255,0.05); font-weight:bold; color:#f8fafc;">${varName.toUpperCase()}</td>
                                    <td style="padding:15px; border-bottom:1px solid rgba(255,255,255,0.05); color:${catColor}; font-weight:500;">${cat}</td>
                                    <td style="padding:15px; border-bottom:1px solid rgba(255,255,255,0.05); font-family:monospace; color:#cbd5e1; letter-spacing: 0.5px;">${rangeStr}</td>`;
                    tbody.appendChild(tr);
                }
            }
        } else {
            tbody.innerHTML = '<tr><td colspan="3" style="padding:20px; text-align:center;">No rules found.</td></tr>';
        }
        document.getElementById('admin-rules-count').innerText = `Displaying ${ruleCount} Rule Thresholds`;
        document.getElementById('admin-rules-modal').style.display = 'flex';
    }'''
if old_open_rules in h_content:
    h_content = h_content.replace(old_open_rules, new_open_rules)

# Phase 1 & Phase 2: JS logic for Report Title and Button Blinking
old_generate = '''                document.getElementById('overall-report-text').innerHTML = args.action_plan.replace(/\\n/g, "<br>");
                document.getElementById('risk-badge').innerText = tier;
                document.getElementById('risk-badge').style.background = tier_color;'''

new_generate = '''                let prefName = document.getElementById('preferred-name').value || "Patient";
                let greetingHtml = `<h3 style="color:#38bdf8; margin-top:0;">Hello ${prefName}, here is your triage report:</h3>`;
                document.getElementById('overall-report-text').innerHTML = greetingHtml + args.action_plan.replace(/\\n/g, "<br>");
                document.getElementById('risk-badge').innerText = tier;
                document.getElementById('risk-badge').style.background = tier_color;
                
                // Add Blinking to AI Nurse Button
                let aiBtn = document.getElementById('header-ai-btn');
                let aiInd = document.getElementById('ai-click-indicator');
                if(aiBtn) aiBtn.classList.add('pulse-active');
                if(aiInd) aiInd.style.display = 'block';'''

if old_generate in h_content:
    h_content = h_content.replace(old_generate, new_generate)

old_toggle_chat = '''        document.getElementById('chat-input').focus();'''
new_toggle_chat = '''        document.getElementById('chat-input').focus();
        
        // Remove blink when opened
        let aiBtn = document.getElementById('header-ai-btn');
        let aiInd = document.getElementById('ai-click-indicator');
        if(aiBtn) aiBtn.classList.remove('pulse-active');
        if(aiInd) aiInd.style.display = 'none';'''
if old_toggle_chat in h_content:
    h_content = h_content.replace(old_toggle_chat, new_toggle_chat)


with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(h_content)

print("SUCCESS")
