with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove floating Admin button
admin_btn = '''    <button onclick="openAdminLogin()" style="position: absolute; top: 20px; left: 20px; z-index: 9999; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-family: 'Outfit', sans-serif; font-size: 14px; display: flex; align-items: center; gap: 8px; transition: all 0.3s;">
        🛡️ Admin
    </button>'''
if admin_btn in content:
    content = content.replace(admin_btn, '')

# 2. Rebuild Header to include the 3 buttons
old_header = '''    <div class="header">
        <div style="display: flex; align-items: center; gap: 20px; position: relative;">
            <h1>HealthAgent Pro</h1>
            <button class="btn" style="padding: 8px 15px; font-size: 14px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); cursor: pointer;" onclick="document.getElementById('ai-arch-dropdown').style.display = document.getElementById('ai-arch-dropdown').style.display === 'none' ? 'block' : 'none'">⚙️ Architecture</button>
            <div id="ai-arch-dropdown" style="display: none; position: absolute; top: 100%; left: 0; margin-top: 15px; width: 450px; background: rgba(15, 23, 42, 0.98); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 25px; z-index: 1000; box-shadow: 0 10px 40px rgba(0,0,0,0.8);">
                <div style="font-size: 20px; color: white; margin-bottom: 20px; font-weight: bold; border-bottom: 1px dashed rgba(255,255,255,0.1); padding-bottom: 15px;">Explainable AI Architecture</div>
                <div style="font-size: 15px; color: #cbd5e1; display: flex; flex-direction: column; gap: 15px; line-height: 1.5;">
                    <div><strong style="color: #60a5fa;">Phase 1: Data-Driven (FCM):</strong> Mathematical boundaries dynamically discovered via Fuzzy C-Means clustering on synthetic data.</div>
                    <div><strong style="color: #fbbf24;">Phase 2: Knowledge-Driven (FIS):</strong> 50 clinically validated Mamdani IF-THEN rules calculating a continuous risk score.</div>
                    <div><strong style="color: #10b981;">Phase 3: Agentic Triage:</strong> Autonomous generation of personalized telehealth reports based on fuzzy outputs.</div>
                </div>
            </div>
        </div>
        <div class="progress-bar">
            <div class="progress-dot active" id="dot-1"></div>
            <div class="progress-dot" id="dot-2"></div>
            <div class="progress-dot" id="dot-3"></div>
            <div class="progress-dot" id="dot-4"></div>
        </div>
    </div>'''

new_header = '''    <div class="header">
        <div>
            <h1>HealthAgent Pro</h1>
        </div>
        <div class="progress-bar">
            <div class="progress-dot active" id="dot-1"></div>
            <div class="progress-dot" id="dot-2"></div>
            <div class="progress-dot" id="dot-3"></div>
            <div class="progress-dot" id="dot-4"></div>
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <button onclick="document.getElementById('admin-modal').style.display='flex'" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 12px; cursor: pointer; font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 500; display: flex; align-items: center; gap: 8px; transition: all 0.3s;">
                🛡️ Admin
            </button>
            <button onclick="document.getElementById('arch-modal').style.display='flex'" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 10px 20px; border-radius: 12px; cursor: pointer; font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 500; display: flex; align-items: center; gap: 8px; transition: all 0.3s;">
                ⚙️ Architecture
            </button>
            <button onclick="toggleChat(true)" style="background: linear-gradient(135deg, #0ea5e9, #2563eb); border: none; color: white; padding: 10px 25px; border-radius: 12px; cursor: pointer; font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 600; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4); transition: transform 0.2s;">
                💬 AI Nurse
            </button>
        </div>
    </div>
    
    <!-- Architecture Modal -->
    <div id="arch-modal" style="display:none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.85); backdrop-filter: blur(5px); z-index: 10000; align-items: center; justify-content: center;">
       <div style="background: linear-gradient(145deg, #1e293b, #0f172a); padding: 50px; border-radius: 24px; width: 600px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
           <h2 style="margin-top: 0; font-size: 32px; text-align: left; color: white; border-bottom: 1px dashed rgba(255,255,255,0.2); padding-bottom: 20px; margin-bottom: 30px;">⚙️ Explainable AI Architecture</h2>
           
           <div style="font-size: 18px; color: #cbd5e1; display: flex; flex-direction: column; gap: 25px; line-height: 1.6;">
               <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                   <strong style="color: #60a5fa; font-size: 22px; display: block; margin-bottom: 10px;">Phase 1: Data-Driven (FCM)</strong> 
                   Mathematical boundaries are dynamically discovered via Fuzzy C-Means clustering on synthetic data.
               </div>
               <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                   <strong style="color: #fbbf24; font-size: 22px; display: block; margin-bottom: 10px;">Phase 2: Knowledge-Driven (FIS)</strong> 
                   50 clinically validated Mamdani IF-THEN rules evaluate parameters to calculate a continuous risk score.
               </div>
               <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05);">
                   <strong style="color: #10b981; font-size: 22px; display: block; margin-bottom: 10px;">Phase 3: Agentic Triage</strong> 
                   Autonomous generation of personalized telehealth reports based on fuzzy outputs.
               </div>
           </div>
           
           <button class="btn btn-next" style="width: 100%; padding: 15px; margin-top: 30px; font-size: 18px;" onclick="document.getElementById('arch-modal').style.display='none'">Close</button>
       </div>
    </div>'''
if old_header in content:
    content = content.replace(old_header, new_header)

# 3. Remove Floating AI Nurse Button
fab = '''<!-- Floating AI Nurse Button -->
    <button onclick="toggleChat()" style="position: fixed; bottom: 40px; right: 40px; z-index: 9000; background: linear-gradient(135deg, #0ea5e9, #2563eb); color: white; border: none; border-radius: 50%; width: 70px; height: 70px; font-size: 30px; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);">💬</button>'''
if fab in content:
    content = content.replace(fab, '')

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS")
