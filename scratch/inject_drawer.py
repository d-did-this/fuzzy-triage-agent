with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_chat_drawer = '''
    <!-- Enhanced Chat Drawer -->
    <div id="chat-drawer" style="position: fixed; right: -650px; top: 0; width: 650px; height: 100vh; background: rgba(15, 23, 42, 0.98); backdrop-filter: blur(30px); border-left: 1px solid rgba(255,255,255,0.1); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); z-index: 9999; display: flex; flex-direction: column; box-shadow: -10px 0 50px rgba(0,0,0,0.5);">
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
    content = content.replace('</div>\n\n<script>', '</div>\n' + new_chat_drawer + '\n<script>')

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
