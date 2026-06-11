import os

# --- Update app.py ---
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

state_init = '''if "chat_id" not in st.session_state:
    st.session_state.chat_id = None'''
state_init_new = '''if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
if "action_plan" not in st.session_state:
    st.session_state.action_plan = None'''
if 'st.session_state.action_plan' not in app_content:
    app_content = app_content.replace(state_init, state_init_new)

old_kiosk = '''component_value = kiosk_ui(score=st.session_state.score, chat_response=st.session_state.chat_response, chat_id=st.session_state.chat_id, key="kiosk")'''
new_kiosk = '''component_value = kiosk_ui(score=st.session_state.score, chat_response=st.session_state.chat_response, chat_id=st.session_state.chat_id, action_plan=st.session_state.action_plan, key="kiosk")'''
if old_kiosk in app_content:
    app_content = app_content.replace(old_kiosk, new_kiosk)

old_else = '''        else:
            # Process the 8 parameters through the mathematical Fuzzy Engine
            try:
                # filter out 'action' and 'name'
                lab_data = {k: v for k, v in component_value.items() if k not in ["action", "name"]}
                new_score = fuzzy_engine.assess_patient(lab_data)
                st.session_state.score = new_score
            except Exception as e:
                st.session_state.score = -1
                print(f"Error calculating score: {e}")'''

new_else = '''        else:
            # Process the 8 parameters through the mathematical Fuzzy Engine
            try:
                # filter out 'action' and 'name'
                lab_data = {k: v for k, v in component_value.items() if k not in ["action", "name"]}
                new_score = fuzzy_engine.assess_patient(lab_data)
                st.session_state.score = new_score
                
                if component_value.get("action") == "generate":
                    if deepseek_client is not None:
                        try:
                            lab_report_str = ", ".join([f"{k.upper()}: {v}" for k, v in lab_data.items()])
                            system_msg = "You are an AI Triage Agent. Given a patient's lab report and their Fuzzy Risk Score (0-100), output a highly concise, bulleted list of 2-4 critical recommended clinical actions. Output ONLY the HTML `<li>` tags containing the text (e.g. `<li>Drink more water</li>`). No markdown blocks, no intro, no outro."
                            prompt = f"Risk Score: {new_score}\\nLab Report: {lab_report_str}"
                            response = deepseek_client.chat.completions.create(
                                model="deepseek-chat",
                                messages=[
                                    {"role": "system", "content": system_msg},
                                    {"role": "user", "content": prompt}
                                ]
                            )
                            raw_html = response.choices[0].message.content.strip()
                            if raw_html.startswith("```html"): raw_html = raw_html[7:]
                            if raw_html.startswith("```"): raw_html = raw_html[3:]
                            if raw_html.endswith("```"): raw_html = raw_html[:-3]
                            st.session_state.action_plan = raw_html.strip()
                        except Exception as e:
                            st.session_state.action_plan = f"<li>Error generating AI action plan: {e}</li>"
                    else:
                        st.session_state.action_plan = "<li>DeepSeek client not configured. Defaulting to standard protocols.</li>"
                        
            except Exception as e:
                st.session_state.score = -1
                print(f"Error calculating score: {e}")'''
if old_else in app_content:
    app_content = app_content.replace(old_else, new_else)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)


# --- Update index.html ---
with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

old_generate = '''    function generateReport() {
        currentStep = 4;
        updateUI();
        document.getElementById('risk-score').innerText = "...";
        document.getElementById('risk-badge').innerText = "COMPUTING AI RISK...";
        document.getElementById('risk-badge').style.backgroundColor = "transparent";'''

new_generate = '''    function generateReport() {
        currentStep = 4;
        updateUI();
        document.getElementById('risk-score').innerHTML = "<div style='font-size:24px; animation: pulse 1s infinite; margin-top:20px;'>Analyzing...</div>";
        document.getElementById('risk-badge').innerText = "AI AGENT GENERATING REPORT...";
        document.getElementById('risk-badge').style.backgroundColor = "transparent";
        document.getElementById('action-list').innerHTML = "<li class='finding-item'><div class='finding-content'><div class='dots' style='font-size:20px; color:#3b82f6;'>🧠 AI is generating your personalized Action Plan...</div></div></li>";'''
if old_generate in html_content:
    html_content = html_content.replace(old_generate, new_generate)

old_listener = '''    window.addEventListener("message", function(event) {
      if (event.data.type === "streamlit:render") {
        const args = event.data.args;
        if (args.score !== null && args.score !== undefined && isWaitingForScore) {
            isWaitingForScore = false;
            renderFinalReport(args.score);
        }'''

new_listener = '''    window.addEventListener("message", function(event) {
      if (event.data.type === "streamlit:render") {
        const args = event.data.args;
        if (args.score !== null && args.score !== undefined && isWaitingForScore) {
            isWaitingForScore = false;
            renderFinalReport(args.score, args.action_plan);
        }'''
if old_listener in html_content:
    html_content = html_content.replace(old_listener, new_listener)

old_render = '''    function renderFinalReport(pythonScore) {'''
new_render = '''    function renderFinalReport(pythonScore, actionPlan) {'''
if old_render in html_content:
    html_content = html_content.replace(old_render, new_render)

old_action_logic = '''        if (!actionHtml) actionHtml = `<li class="finding-item safe"><div class="finding-icon">🛡️</div><div class="finding-content"><h4 style="color:var(--safe)">Maintain Health</h4><p>No actionable deviations. Keep up the good work.</p></div></li>`;'''

new_action_logic = '''        if (!actionHtml) actionHtml = `<li class="finding-item safe"><div class="finding-icon">🛡️</div><div class="finding-content"><h4 style="color:var(--safe)">Maintain Health</h4><p>No actionable deviations. Keep up the good work.</p></div></li>`;
        
        // Override with Agentic AI Action Plan if available
        if (actionPlan) {
            actionHtml = `<li class="finding-item safe" style="border-color: #a78bfa; background: rgba(167, 139, 250, 0.1);">
                <div class="finding-icon" style="font-size:36px;">🤖</div>
                <div class="finding-content" style="width: 100%;">
                    <h4 style="color: #a78bfa; font-size: 24px; margin-bottom: 10px;">Agentic Recommended Actions:</h4>
                    <ul style="margin: 0; padding-left: 20px; color: #e2e8f0; font-size: 18px; line-height: 1.6;">
                        ${actionPlan}
                    </ul>
                </div>
            </li>`;
        }'''
if old_action_logic in html_content:
    html_content = html_content.replace(old_action_logic, new_action_logic)

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("SUCCESS")
