with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract the broken Chat Drawer from JS and fix the template literal
broken_chat_drawer = '''
    <!-- Chat Drawer -->
    <div id="chat-drawer" style="position: absolute; right: -450px; top: 0; width: 450px; height: 100vh; background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(20px); border-left: 1px solid rgba(255,255,255,0.1); transition: right 0.3s ease; z-index: 9999; display: flex; flex-direction: column;">
        <div style="padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0; color: #3b82f6; font-size:24px;">🩺 AI Triage Nurse</h3>
            <button onclick="toggleChat()" style="background: transparent; border: none; color: white; font-size: 24px; cursor: pointer;">✕</button>
        </div>
        <div id="chat-messages" style="flex-grow: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px;">
            <div class="chat-bubble assistant">Hello! I'm your AI Triage Nurse. Once you generate your report, you can ask me anything about it.</div>
        </div>
        <div id="chat-thinking" style="display: none; padding: 10px 20px; color: #94a3b8; font-style: italic;">
            👩‍⚕️ AI Nurse is thinking<span class="dots">...</span>
        </div>
        <div style="padding: 10px 20px; display: flex; gap: 10px; overflow-x: auto;">
            <button class="preset-btn" onclick="sendChat('Explain my score')">📊 Explain Score</button>
            <button class="preset-btn" onclick="sendChat('Dietary advice')">🥗 Diet</button>
            <button class="preset-btn" onclick="sendChat('Any red flags?')">⚠️ Red Flags</button>
        </div>
        <div style="padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; gap: 10px;">
            <input type="text" id="chat-input" placeholder="Ask a question..." style="flex-grow: 1; padding: 10px 15px; border-radius: 20px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); color: white; font-size: 16px;" onkeypress="if(event.key === 'Enter') sendChat()">
            <button onclick="sendChat()" style="background: #3b82f6; border: none; width: 45px; height: 45px; border-radius: 50%; color: white; cursor: pointer; font-size: 18px;">➤</button>
        </div>
    </div>
'''

if broken_chat_drawer in content:
    content = content.replace(broken_chat_drawer, '')

# Now insert the newly designed Chat Drawer correctly just before <script>
new_chat_drawer = '''
    <!-- Enhanced Chat Drawer -->
    <div id="chat-drawer" style="position: absolute; right: -650px; top: 0; width: 650px; height: 100vh; background: rgba(15, 23, 42, 0.98); backdrop-filter: blur(30px); border-left: 1px solid rgba(255,255,255,0.1); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); z-index: 9999; display: flex; flex-direction: column; box-shadow: -10px 0 50px rgba(0,0,0,0.5);">
        <div style="padding: 25px; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.2);">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="width: 45px; height: 45px; background: linear-gradient(135deg, #3b82f6, #8b5cf6); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);">✨</div>
                <h3 style="margin: 0; color: white; font-size:26px; font-weight: 600;">HealthAgent Companion</h3>
            </div>
            <div style="display: flex; gap: 10px;">
                <button onclick="toggleFullscreenChat()" style="background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: white; font-size: 18px; cursor: pointer; padding: 8px 12px; transition: all 0.2s;">⛶</button>
                <button onclick="toggleChat(false)" style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 8px; color: #ef4444; font-size: 20px; cursor: pointer; padding: 8px 15px; transition: all 0.2s;">✕</button>
            </div>
        </div>
        <div id="chat-messages" style="flex-grow: 1; padding: 30px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px; background: linear-gradient(to bottom, rgba(15,23,42,0) 0%, rgba(0,0,0,0.2) 100%);">
            <div class="chat-bubble assistant">Hello! I'm your AI Companion. Once you generate your report, you can ask me anything about it.</div>
        </div>
        <div id="chat-thinking" style="display: none; padding: 10px 30px; color: #94a3b8; font-style: italic; font-size: 16px;">
            ✨ Companion is thinking<span class="dots">...</span>
        </div>
        <div style="padding: 15px 30px; display: flex; gap: 12px; overflow-x: auto; border-top: 1px solid rgba(255,255,255,0.05);">
            <button class="preset-btn" onclick="sendChat('Explain my score')">📊 Explain Score</button>
            <button class="preset-btn" onclick="sendChat('What should I eat?')">🥗 Dietary Advice</button>
            <button class="preset-btn" onclick="sendChat('Any critical red flags?')">⚠️ Red Flags</button>
        </div>
        <div style="padding: 25px 30px; background: rgba(0,0,0,0.3); border-top: 1px solid rgba(255,255,255,0.1); display: flex; gap: 15px; align-items: center;">
            <input type="text" id="chat-input" placeholder="Type your message here..." style="flex-grow: 1; padding: 15px 25px; border-radius: 30px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); color: white; font-size: 18px; outline: none; transition: all 0.3s;" onfocus="this.style.borderColor='#3b82f6'" onblur="this.style.borderColor='rgba(255,255,255,0.2)'" onkeypress="if(event.key === 'Enter') sendChat()">
            <button onclick="sendChat()" style="background: linear-gradient(135deg, #3b82f6, #2563eb); border: none; width: 55px; height: 55px; border-radius: 50%; color: white; cursor: pointer; font-size: 20px; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); transition: transform 0.2s;">➤</button>
        </div>
    </div>
'''
if 'id="chat-drawer"' not in content:
    content = content.replace('</div>\n<script src="streamlit-component-lib.js">', new_chat_drawer + '\n</div>\n<script src="streamlit-component-lib.js">')

# 2. Fix the header title to act as reload
old_h1 = '''<h1>HealthAgent Pro</h1>'''
new_h1 = '''<h1 style="cursor: pointer; transition: transform 0.2s;" onclick="location.reload()" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">HealthAgent Pro</h1>'''
content = content.replace(old_h1, new_h1)

# 3. Patient Profile Required Check
old_name_label = '''<label class="control-label" style="display:block; margin-bottom:15px; font-size: 24px;">Patient Profile<br><span style="font-size: 16px; color: var(--text-muted); font-weight: normal;">Full Name (Optional)</span></label>
                            <input type="text" id="name" placeholder="Enter patient name..." style="width: 100%; padding: 15px 20px; border-radius: 12px; font-size: 20px;">'''
new_name_label = '''<label class="control-label" style="display:block; margin-bottom:15px; font-size: 24px;">Patient Profile<br><span style="font-size: 16px; color: #ef4444; font-weight: normal;">Preferred Name (Required)</span></label>
                            <input type="text" id="name" placeholder="Enter a preferred name..." style="width: 100%; padding: 15px 20px; border-radius: 12px; font-size: 20px; border: 1px solid #ef4444;" oninput="this.style.borderColor = this.value.trim() ? 'rgba(255,255,255,0.1)' : '#ef4444'; validateName()">'''
content = content.replace(old_name_label, new_name_label)

# 4. Modify the Next button logic to check for name
old_btn_next = '''<button class="btn btn-next" onclick="nextStep(2)">Begin Assessment ➔</button>'''
new_btn_next = '''<button class="btn btn-next" id="btn-begin" onclick="if(document.getElementById('name').value.trim()) { nextStep(2); } else { alert('Please enter a preferred name first!'); }">Begin Assessment ➔</button>'''
content = content.replace(old_btn_next, new_btn_next)

# 5. Fix JS toggleChat logic (the drawer width is now 650px)
old_toggle = '''    function toggleChat(forceOpen = null) {
        if(forceOpen !== null && typeof forceOpen === "boolean") isChatOpen = forceOpen;
        else isChatOpen = !isChatOpen;
        document.getElementById('chat-drawer').style.right = isChatOpen ? "0" : "-450px";
    }'''
new_toggle = '''    let isFullscreenChat = false;
    function toggleChat(forceOpen = null) {
        if(forceOpen !== null && typeof forceOpen === "boolean") isChatOpen = forceOpen;
        else isChatOpen = !isChatOpen;
        
        let drawer = document.getElementById('chat-drawer');
        if (isChatOpen) {
            drawer.style.right = "0";
        } else {
            drawer.style.right = isFullscreenChat ? "-100vw" : "-650px";
            if(isFullscreenChat) toggleFullscreenChat(); // reset
        }
    }
    
    function toggleFullscreenChat() {
        isFullscreenChat = !isFullscreenChat;
        let drawer = document.getElementById('chat-drawer');
        if (isFullscreenChat) {
            drawer.style.width = "100vw";
            drawer.style.right = "0";
        } else {
            drawer.style.width = "650px";
            drawer.style.right = "0";
        }
    }
    
    function validateName() {
        let name = document.getElementById('name').value.trim();
        let btn = document.getElementById('btn-begin');
        if (name) {
            btn.style.opacity = '1';
            btn.style.pointerEvents = 'auto';
        } else {
            btn.style.opacity = '0.5';
        }
    }
'''
if "function toggleFullscreenChat" not in content:
    content = content.replace(old_toggle, new_toggle)

# 6. Update "Agentic Recommended Actions" text and add disclaimer
old_action = '''<h4 style="color: #a78bfa; font-size: 24px; margin-bottom: 10px;">Agentic Recommended Actions:</h4>
                    <ul style="margin: 0; padding-left: 20px; color: #e2e8f0; font-size: 18px; line-height: 1.6;">
                        ${actionPlan}
                    </ul>'''
new_action = '''<h4 style="color: #a78bfa; font-size: 24px; margin-bottom: 10px;">✨ AI Recommended Actions:</h4>
                    <ul style="margin: 0; padding-left: 20px; color: #e2e8f0; font-size: 18px; line-height: 1.6;">
                        ${actionPlan}
                    </ul>
                    <div style="margin-top: 15px; font-size: 14px; color: #94a3b8; font-style: italic; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 10px;">
                        *Disclaimer: This action plan is dynamically generated by an AI assistant based on fuzzy logic outputs. It is not professional medical advice. Please consult a qualified healthcare provider for clinical decisions.
                    </div>'''
content = content.replace(old_action, new_action)

# 7. Update progress dots design
old_dots_css = '''        .progress-dot { width: 16px; height: 16px; border-radius: 50%; background: #334155; transition: all 0.4s ease; }
        .progress-dot.active { background: var(--primary); box-shadow: 0 0 10px var(--primary-glow); transform: scale(1.2); }'''

new_dots_css = '''        .progress-bar { display: flex; align-items: center; gap: 15px; position: relative; }
        .progress-bar::before { content: ''; position: absolute; top: 50%; left: 10px; right: 10px; height: 2px; background: #334155; z-index: 0; transform: translateY(-50%); }
        .progress-dot { width: 24px; height: 24px; border-radius: 50%; background: #1e293b; border: 2px solid #334155; transition: all 0.4s ease; z-index: 1; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; color: #94a3b8; }
        .progress-dot.active { background: var(--primary); border-color: var(--primary); box-shadow: 0 0 15px var(--primary-glow); color: white; transform: scale(1.1); }
        .progress-dot.completed { background: var(--primary); border-color: var(--primary); color: white; }'''
content = content.replace(old_dots_css, new_dots_css)

old_dots_html = '''        <div class="progress-bar">
            <div class="progress-dot active" id="dot-1"></div>
            <div class="progress-dot" id="dot-2"></div>
            <div class="progress-dot" id="dot-3"></div>
            <div class="progress-dot" id="dot-4"></div>
        </div>'''
new_dots_html = '''        <div class="progress-bar">
            <div class="progress-dot active" id="dot-1">1</div>
            <div class="progress-dot" id="dot-2">2</div>
            <div class="progress-dot" id="dot-3">3</div>
            <div class="progress-dot" id="dot-4">4</div>
        </div>'''
content = content.replace(old_dots_html, new_dots_html)

old_update_ui = '''        for(let i=1; i<=totalSteps; i++) {
            document.getElementById('dot-'+i).className = (i === currentStep) ? 'progress-dot active' : 'progress-dot';
        }'''
new_update_ui = '''        for(let i=1; i<=totalSteps; i++) {
            let dot = document.getElementById('dot-'+i);
            if (i < currentStep) dot.className = 'progress-dot completed';
            else if (i === currentStep) dot.className = 'progress-dot active';
            else dot.className = 'progress-dot';
        }'''
content = content.replace(old_update_ui, new_update_ui)

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
