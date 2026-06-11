import re

with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the admin dashboard box
old_dashboard = '''       <div id="admin-dashboard-box" style="display:none; background: linear-gradient(145deg, #1e293b, #0f172a); padding: 40px; border-radius: 24px; width: 500px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
           <h2 style="margin-top: 0; font-size: 28px; color: white;">Admin Dashboard</h2>
           <label style="color:#cbd5e1; font-size:16px;">Simulate Health Alert (e.g. Dengue Outbreak):</label>
           <textarea id="admin_alert" style="width:100%; height:80px; margin-bottom: 20px; margin-top:10px; padding: 10px; font-family:inherit; background:rgba(0,0,0,0.2); color:white; border:1px solid rgba(255,255,255,0.1); border-radius:8px;">None</textarea>
           
           <h3 style="color:white; margin-top:10px;">Agent Reflection</h3>
           <button class="btn" style="width: 100%; background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #ef4444;" onclick="triggerRuleFailure()">Simulate Rule Failure</button>
           
           <button class="btn btn-back" style="width: 100%; margin-top: 30px;" onclick="document.getElementById('admin-modal').style.display='none'">Close Admin Panel</button>
       </div>'''

new_dashboard = '''       <div id="admin-dashboard-box" style="display:none; background: linear-gradient(145deg, #1e293b, #0f172a); padding: 40px; border-radius: 24px; width: 500px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 50px rgba(0,0,0,0.5); max-height: 90vh; overflow-y: auto;">
           <h2 style="margin-top: 0; font-size: 28px; color: white; display: flex; justify-content: space-between; align-items: center;">
               Admin Dashboard
               <button onclick="document.getElementById('admin-modal').style.display='none'" style="background:none; border:none; color:white; cursor:pointer; font-size:24px;">✕</button>
           </h2>
           
           <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 16px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05);">
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
           </div>
       </div>
       
       <!-- Logs Modal (Inside Admin) -->
       <div id="admin-logs-modal" style="display:none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #0f172a; padding: 30px; border-radius: 20px; width: 800px; max-height: 80vh; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 30px 60px rgba(0,0,0,0.6); z-index: 10001; flex-direction: column;">
           <h2 style="margin-top: 0; color: white; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">
               Agent Experience Logs
               <button onclick="document.getElementById('admin-logs-modal').style.display='none'" style="background:none; border:none; color:white; cursor:pointer; font-size:24px;">✕</button>
           </h2>
           <div style="overflow-y: auto; flex-grow: 1; margin-top: 15px;">
               <table style="width: 100%; border-collapse: collapse; color: #e2e8f0; font-size: 14px;">
                   <thead>
                       <tr style="background: rgba(255,255,255,0.05); text-align: left;">
                           <th style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">Timestamp</th>
                           <th style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">Action</th>
                           <th style="padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">Reasoning</th>
                       </tr>
                   </thead>
                   <tbody id="admin-logs-tbody">
                   </tbody>
               </table>
           </div>
       </div>
       
       <!-- Rules Modal (Inside Admin) -->
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

if old_dashboard in content:
    content = content.replace(old_dashboard, new_dashboard)
else:
    print("WARNING: Could not find old_dashboard in index.html")

# 2. Update JS payload handling
old_listener = '''    window.addEventListener("message", function(event) {
      if (event.data.type === "streamlit:render") {
        const args = event.data.args;
        if (args.score !== null && args.score !== undefined && isWaitingForScore) {'''

new_listener = '''    window.adminLogs = [];
    window.adminRules = {};
    window.addEventListener("message", function(event) {
      if (event.data.type === "streamlit:render") {
        const args = event.data.args;
        if (args.logs) window.adminLogs = args.logs;
        if (args.rules) window.adminRules = args.rules;
        
        if (args.score !== null && args.score !== undefined && isWaitingForScore) {'''

if old_listener in content:
    content = content.replace(old_listener, new_listener)
else:
    print("WARNING: Could not find old_listener in index.html")

# 3. Add JS functions for the new modals
new_js_funcs = '''
    function setHealthAlert() {
        let val = document.getElementById('admin_alert_preset').value;
        Streamlit.setComponentValue({action: "set_health_alert", health_alert: val});
    }
    
    function openAdminLogs() {
        let tbody = document.getElementById('admin-logs-tbody');
        tbody.innerHTML = '';
        if(window.adminLogs && window.adminLogs.length > 0) {
            window.adminLogs.forEach(log => {
                let tr = document.createElement('tr');
                tr.innerHTML = `<td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.05);">${log.timestamp}</td>
                                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.05); color:#60a5fa;">${log.action}</td>
                                <td style="padding:10px; border-bottom:1px solid rgba(255,255,255,0.05);">${log.reason}</td>`;
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="3" style="padding:20px; text-align:center;">No logs recorded yet.</td></tr>';
        }
        document.getElementById('admin-logs-modal').style.display = 'flex';
    }
    
    function openAdminRules() {
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
    }
'''

content = content.replace('function openAdminLogin() {', new_js_funcs + '\n    function openAdminLogin() {')

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
