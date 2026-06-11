import re

with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the Greeting Logic in renderFinalReport
old_overall_logic = '''        // Overall Report Logic
        let overallText = "";
        const nameInput = document.getElementById('name').value;
        const patientRef = nameInput ? `for patient <strong>${nameInput}</strong>` : "for the current profile";

        if (dangerCount > 0) {
            overallText = `Based on the comprehensive analysis of 8 physiological markers ${patientRef}, <strong><span style="color:var(--danger)">${dangerCount} critical abnormalities</span></strong> were detected. The systemic triage profile is categorized as <strong>HIGH RISK</strong>. Immediate clinical intervention and specialist referral are strongly recommended. Please download the diagnostic report below and present it to the ER or primary care provider.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--danger)';
        } else if (warningCount > 0) {
            overallText = `Based on the comprehensive analysis ${patientRef}, <strong><span style="color:var(--warning)">${warningCount} parameters</span></strong> present moderate deviations from optimal biological baselines. The triage profile is categorized as <strong>MODERATE RISK</strong>. Preventative care measures, lifestyle modifications, and follow-up monitoring within 1-2 weeks are advised.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--warning)';
        } else {
            overallText = `All 8 physiological markers analyzed ${patientRef} are perfectly aligned within optimal biological ranges. The systemic triage profile is categorized as <strong>NORMAL RISK</strong>. The AI recommends continuing current lifestyle and nutritional habits. No clinical intervention is required at this time.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--safe)';
        }
        document.getElementById('overall-report-text').innerHTML = overallText;'''

new_overall_logic = '''        // Overall Report Logic
        let overallText = "";
        const nameInput = document.getElementById('name').value || "Patient";
        const patientRef = nameInput !== "Patient" ? `for patient <strong>${nameInput}</strong>` : "for the current profile";
        
        let greetingHtml = `<h3 style="color:#38bdf8; margin-top:0;">Hello ${nameInput}, here is your triage report:</h3>`;

        if (dangerCount > 0) {
            overallText = `Based on the comprehensive analysis of 8 physiological markers ${patientRef}, <strong><span style="color:var(--danger)">${dangerCount} critical abnormalities</span></strong> were detected. The systemic triage profile is categorized as <strong>HIGH RISK</strong>. Immediate clinical intervention and specialist referral are strongly recommended. Please download the diagnostic report below and present it to the ER or primary care provider.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--danger)';
        } else if (warningCount > 0) {
            overallText = `Based on the comprehensive analysis ${patientRef}, <strong><span style="color:var(--warning)">${warningCount} parameters</span></strong> present moderate deviations from optimal biological baselines. The triage profile is categorized as <strong>MODERATE RISK</strong>. Preventative care measures, lifestyle modifications, and follow-up monitoring within 1-2 weeks are advised.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--warning)';
        } else {
            overallText = `All 8 physiological markers analyzed ${patientRef} are perfectly aligned within optimal biological ranges. The systemic triage profile is categorized as <strong>NORMAL RISK</strong>. The AI recommends continuing current lifestyle and nutritional habits. No clinical intervention is required at this time.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--safe)';
        }
        document.getElementById('overall-report-text').innerHTML = greetingHtml + `<p style="margin-top:10px;">${overallText}</p>`;'''

content = content.replace(old_overall_logic, new_overall_logic)

# 2. Update the Action Plan Injection to trigger pulse
old_action_plan_injection = '''        // Override with Agentic AI Action Plan if available
        if (actionPlan) {
            actionHtml = `<li class="finding-item safe" style="border-color: #a78bfa; background: rgba(167, 139, 250, 0.1);">
                <div class="finding-icon" style="font-size:36px;">🤖</div>
                <div class="finding-content" style="width: 100%;">
                    <h4 style="color: #a78bfa; font-size: 24px; margin-bottom: 10px;">✨ AI Recommended Actions:</h4>
                    <ul style="margin: 0; padding-left: 20px; color: #e2e8f0; font-size: 18px; line-height: 1.6;">
                        ${actionPlan}
                    </ul>
                    <div style="margin-top: 15px; font-size: 14px; color: #94a3b8; font-style: italic; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 10px;">
                        *Disclaimer: This action plan is dynamically generated by an AI assistant based on fuzzy logic outputs. It is not professional medical advice. Please consult a qualified healthcare provider for clinical decisions.
                    </div>
                </div>
            </li>`;
        }'''

new_action_plan_injection = '''        // Override with Agentic AI Action Plan if available
        if (actionPlan) {
            actionHtml = `<li class="finding-item safe" style="border-color: #a78bfa; background: rgba(167, 139, 250, 0.1); padding: 0; border: none;">
                <div class="finding-content" style="width: 100%;">
                    ${actionPlan}
                    <div style="margin-top: 15px; font-size: 14px; color: #94a3b8; font-style: italic; border-top: 1px dashed rgba(255,255,255,0.1); padding-top: 10px;">
                        *Disclaimer: This action plan is dynamically generated by an AI assistant based on fuzzy logic outputs. It is not professional medical advice. Please consult a qualified healthcare provider for clinical decisions.
                    </div>
                </div>
            </li>`;
            
            // Add Blinking to AI Nurse Button
            let aiBtn = document.getElementById('header-ai-btn');
            let aiInd = document.getElementById('ai-click-indicator');
            if(aiBtn) aiBtn.classList.add('pulse-active');
            if(aiInd) aiInd.style.display = 'block';
        }'''

content = content.replace(old_action_plan_injection, new_action_plan_injection)

# 3. Update toggleChat to remove blink
old_toggle_chat = '''        if (isChatOpen) {
            drawer.style.right = "0";
        } else {'''

new_toggle_chat = '''        if (isChatOpen) {
            drawer.style.right = "0";
            let aiBtn = document.getElementById('header-ai-btn');
            let aiInd = document.getElementById('ai-click-indicator');
            if(aiBtn) aiBtn.classList.remove('pulse-active');
            if(aiInd) aiInd.style.display = 'none';
        } else {'''

content = content.replace(old_toggle_chat, new_toggle_chat)

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS")
