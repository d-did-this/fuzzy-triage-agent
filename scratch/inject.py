import uuid

with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS Injection
css = '''
        /* Chat UI Styles */
        .chat-bubble {
            padding: 15px 20px; border-radius: 18px; max-width: 85%; font-size: 16px; line-height: 1.5;
        }
        .chat-bubble.assistant {
            background: #1e293b; color: #e2e8f0; align-self: flex-start; border-bottom-left-radius: 4px;
        }
        .chat-bubble.user {
            background: #3b82f6; color: white; align-self: flex-end; border-bottom-right-radius: 4px;
        }
        .preset-btn {
            background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 20px; padding: 8px 15px; cursor: pointer; white-space: nowrap; font-size: 14px;
        }
        .preset-btn:hover { background: rgba(255,255,255,0.2); }
        .dots { animation: blink 1.5s infinite steps(4, end); }
        @keyframes blink { 0%, 100% { clip-path: inset(0 100% 0 0); } 33% { clip-path: inset(0 66% 0 0); } 66% { clip-path: inset(0 33% 0 0); } }
'''
if "/* Chat UI Styles */" not in content:
    content = content.replace('</style>', css + '\n    </style>')

# 2. Admin Modal Replacement
old_admin_modal = '''<!-- Admin Modal -->
    <div id="admin-modal" style="display:none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); backdrop-filter: blur(5px); z-index: 10000; align-items: center; justify-content: center;">
       <div style="background: linear-gradient(145deg, #1e293b, #0f172a); padding: 40px; border-radius: 24px; width: 400px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
           <h2 style="margin-top: 0; font-size: 28px; text-align: center; color: white;">System Admin</h2>
           <input type="text" id="admin_user" placeholder="Username" style="width:100%; margin-bottom: 20px; text-align: left; padding: 15px 20px; font-size: 18px;">
           <input type="password" id="admin_pass" placeholder="Password" style="width:100%; margin-bottom: 30px; text-align: left; padding: 15px 20px; font-size: 18px; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 12px;">
           <button class="btn btn-next" style="width: 100%; padding: 15px;" onclick="submitAdmin()">Login</button>
           <button class="btn btn-back" style="width: 100%; padding: 15px; margin-top: 15px;" onclick="document.getElementById('admin-modal').style.display='none'">Cancel</button>
       </div>
    </div>'''

new_admin_modal = '''<!-- Admin Modal -->
    <div id="admin-modal" style="display:none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); backdrop-filter: blur(5px); z-index: 10000; align-items: center; justify-content: center;">
       <div id="admin-login-box" style="background: linear-gradient(145deg, #1e293b, #0f172a); padding: 40px; border-radius: 24px; width: 400px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
           <h2 style="margin-top: 0; font-size: 28px; text-align: center; color: white;">System Admin</h2>
           <input type="text" id="admin_user" placeholder="Username" style="width:100%; margin-bottom: 20px; text-align: left; padding: 15px 20px; font-size: 18px;">
           <input type="password" id="admin_pass" placeholder="Password" style="width:100%; margin-bottom: 30px; text-align: left; padding: 15px 20px; font-size: 18px; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); color: white; border-radius: 12px;">
           <button class="btn btn-next" style="width: 100%; padding: 15px;" onclick="submitAdmin()">Login</button>
           <button class="btn btn-back" style="width: 100%; padding: 15px; margin-top: 15px;" onclick="document.getElementById('admin-modal').style.display='none'">Cancel</button>
       </div>
       
       <div id="admin-dashboard-box" style="display:none; background: linear-gradient(145deg, #1e293b, #0f172a); padding: 40px; border-radius: 24px; width: 500px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
           <h2 style="margin-top: 0; font-size: 28px; color: white;">Admin Dashboard</h2>
           <label style="color:#cbd5e1; font-size:16px;">Simulate Health Alert (e.g. Dengue Outbreak):</label>
           <textarea id="admin_alert" style="width:100%; height:80px; margin-bottom: 20px; margin-top:10px; padding: 10px; font-family:inherit; background:rgba(0,0,0,0.2); color:white; border:1px solid rgba(255,255,255,0.1); border-radius:8px;">None</textarea>
           
           <h3 style="color:white; margin-top:10px;">Agent Reflection</h3>
           <button class="btn" style="width: 100%; background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #ef4444;" onclick="triggerRuleFailure()">Simulate Rule Failure</button>
           
           <button class="btn btn-back" style="width: 100%; margin-top: 30px;" onclick="document.getElementById('admin-modal').style.display='none'">Close Admin Panel</button>
       </div>
    </div>'''
if old_admin_modal in content:
    content = content.replace(old_admin_modal, new_admin_modal)

# 3. Add Chat Drawer HTML just before last </div> in kiosk-container
chat_drawer_html = '''
    <!-- Floating AI Nurse Button -->
    <button onclick="toggleChat()" style="position: fixed; bottom: 40px; right: 40px; z-index: 9000; background: linear-gradient(135deg, #0ea5e9, #2563eb); color: white; border: none; border-radius: 50%; width: 70px; height: 70px; font-size: 30px; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);">💬</button>

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

if 'id="chat-drawer"' not in content:
    kiosk_end = content.rfind('</div>', 0, content.find('<script src="streamlit-component-lib.js">'))
    content = content[:kiosk_end] + chat_drawer_html + content[kiosk_end:]

# 4. Replace submitAdmin() function
old_submit_admin = '''function submitAdmin() {
        let p = document.getElementById('admin_pass').value;
        if(p === "admin123") {
            document.getElementById('admin-modal').style.display = 'none';
            document.getElementById('admin_pass').value = '';
            Streamlit.setComponentValue({action: "open_admin"});
        } else {
            alert("Invalid credentials");
        }
    }'''
    
new_submit_admin = '''function submitAdmin() {
        let p = document.getElementById('admin_pass').value;
        if(p === "admin123") {
            document.getElementById('admin-login-box').style.display = 'none';
            document.getElementById('admin-dashboard-box').style.display = 'block';
            document.getElementById('admin_pass').value = '';
        } else {
            alert("Invalid credentials");
        }
    }
    
    function triggerRuleFailure() {
        alert("Rule Failure Injected into Agent Context!");
        document.getElementById('admin-modal').style.display='none';
        toggleChat(true);
        Streamlit.setComponentValue({action: "simulate_failure"});
    }

    let isChatOpen = false;
    function toggleChat(forceOpen = null) {
        if(forceOpen !== null && typeof forceOpen === "boolean") isChatOpen = forceOpen;
        else isChatOpen = !isChatOpen;
        document.getElementById('chat-drawer').style.right = isChatOpen ? "0" : "-450px";
    }
    
    function sendChat(presetMsg = null) {
        let msg = presetMsg || document.getElementById('chat-input').value;
        if(typeof msg !== "string") msg = document.getElementById('chat-input').value; // catch mouse events
        if(!msg || !msg.trim()) return;
        
        let chatDiv = document.getElementById('chat-messages');
        chatDiv.innerHTML += `<div class="chat-bubble user">${msg}</div>`;
        document.getElementById('chat-input').value = "";
        
        document.getElementById('chat-thinking').style.display = 'block';
        chatDiv.scrollTop = chatDiv.scrollHeight;
        
        let alertContext = document.getElementById('admin_alert') ? document.getElementById('admin_alert').value : "None";
        let nameContext = document.getElementById('name') ? document.getElementById('name').value : "Patient";
        
        // Pass to Streamlit
        Streamlit.setComponentValue({action: "chat_message", prompt: msg, health_alert: alertContext, name: nameContext});
    }
    
    window.lastChatId = null;
    '''
if old_submit_admin in content:
    content = content.replace(old_submit_admin, new_submit_admin)

# 5. Update window.addEventListener
old_listener = '''    window.addEventListener("message", function(event) {
      if (event.data.type === "streamlit:render") {
        const args = event.data.args;
        if (args.score !== null && args.score !== undefined && isWaitingForScore) {
            isWaitingForScore = false;
            renderFinalReport(args.score);
        }
      }
    });'''

new_listener = '''    window.addEventListener("message", function(event) {
      if (event.data.type === "streamlit:render") {
        const args = event.data.args;
        if (args.score !== null && args.score !== undefined && isWaitingForScore) {
            isWaitingForScore = false;
            renderFinalReport(args.score);
        }
        
        if (args.chat_response && args.chat_id && args.chat_id !== window.lastChatId) {
            window.lastChatId = args.chat_id;
            document.getElementById('chat-thinking').style.display = 'none';
            let chatDiv = document.getElementById('chat-messages');
            chatDiv.innerHTML += `<div class="chat-bubble assistant">${args.chat_response}</div>`;
            chatDiv.scrollTop = chatDiv.scrollHeight;
        }
      }
    });'''
if old_listener in content:
    content = content.replace(old_listener, new_listener)

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS")
