import re

with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = '''        if (dangerCount > 0) {
            overallText = `Based on the comprehensive analysis of 8 physiological markers ${patientRef}, <strong><span style="color:var(--danger)">${dangerCount} critical abnormalities</span></strong> were detected. The systemic triage profile is categorized as <strong>HIGH RISK</strong>. Immediate clinical intervention and specialist referral are strongly recommended. Please download the diagnostic report below and present it to the ER or primary care provider.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--danger)';
        } else if (warningCount > 0) {
            overallText = `Based on the comprehensive analysis ${patientRef}, <strong><span style="color:var(--warning)">${warningCount} parameters</span></strong> present moderate deviations from optimal biological baselines. The triage profile is categorized as <strong>MODERATE RISK</strong>. Preventative care measures, lifestyle modifications, and follow-up monitoring within 1-2 weeks are advised.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--warning)';
        } else {
            overallText = `All 8 physiological markers analyzed ${patientRef} are perfectly aligned within optimal biological ranges. The systemic triage profile is categorized as <strong>NORMAL RISK</strong>. The AI recommends continuing current lifestyle and nutritional habits. No clinical intervention is required at this time.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--safe)';
        }'''

new_logic = '''        let abnText = "";
        if (dangerCount > 0 && warningCount > 0) {
            abnText = `${dangerCount} critical abnormalities and ${warningCount} moderate deviations were detected.`;
        } else if (dangerCount > 0) {
            abnText = `${dangerCount} critical abnormalities were detected.`;
        } else if (warningCount > 0) {
            abnText = `${warningCount} parameters present moderate deviations.`;
        } else {
            abnText = `No physiological abnormalities were detected.`;
        }

        if (pythonScore >= 70) {
            overallText = `Based on the comprehensive analysis of 8 physiological markers ${patientRef}, <strong><span style="color:var(--danger)">${abnText}</span></strong> The systemic triage profile (Score: ${pythonScore.toFixed(1)}) is categorized as <strong>HIGH RISK</strong>. Immediate clinical intervention and specialist referral are strongly recommended. Please download the diagnostic report below and present it to the ER or primary care provider.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--danger)';
        } else if (pythonScore >= 40) {
            overallText = `Based on the comprehensive analysis ${patientRef}, <strong><span style="color:var(--warning)">${abnText}</span></strong> The triage profile (Score: ${pythonScore.toFixed(1)}) is categorized as <strong>MODERATE RISK</strong>. Preventative care measures, lifestyle modifications, and follow-up monitoring within 1-2 weeks are advised.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--warning)';
        } else {
            overallText = `All 8 physiological markers analyzed ${patientRef} are perfectly aligned within optimal biological ranges. The systemic triage profile (Score: ${pythonScore.toFixed(1)}) is categorized as <strong>NORMAL RISK</strong>. The AI recommends continuing current lifestyle and nutritional habits. No clinical intervention is required at this time.`;
            document.getElementById('overall-report-text').style.borderLeftColor = 'var(--safe)';
        }'''

content = content.replace(old_logic, new_logic)

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("SUCCESS")
