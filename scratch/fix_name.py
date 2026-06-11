with open('kiosk_component/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the label and input HTML
old_input = '''                                <label style="display: block; color: var(--text-muted); font-size: 20px; margin-bottom: 10px;">Full Name (Optional)</label>
                                <input type="text" class="name-input" id="name" placeholder="e.g. John Doe" style="width: 100%; border: 1px solid rgba(255,255,255,0.2); background: rgba(0,0,0,0.4);">'''

new_input = '''                                <label style="display: block; color: #ef4444; font-size: 20px; margin-bottom: 10px;">Preferred Name (Required)</label>
                                <input type="text" class="name-input" id="name" placeholder="e.g. John Doe" style="width: 100%; border: 1px solid #ef4444; background: rgba(0,0,0,0.4);" oninput="this.style.borderColor = this.value.trim() ? 'rgba(255,255,255,0.2)' : '#ef4444';">'''

if old_input in content:
    content = content.replace(old_input, new_input)
else:
    print("WARNING: Could not find old input HTML")

# 2. Update the changeStep function to block progression from step 1
old_change = '''    function changeStep(dir) {
        if (currentStep === 3 && dir === 1) {
            generateReport();
            return;
        }'''

new_change = '''    function changeStep(dir) {
        if (currentStep === 1 && dir === 1) {
            if (!document.getElementById('name').value.trim()) {
                alert("Please enter a Preferred Name before beginning the assessment.");
                return;
            }
        }
        if (currentStep === 3 && dir === 1) {
            generateReport();
            return;
        }'''

if old_change in content:
    content = content.replace(old_change, new_change)
else:
    print("WARNING: Could not find old changeStep function")

with open('kiosk_component/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
