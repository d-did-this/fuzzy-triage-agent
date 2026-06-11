with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the kiosk_ui call
old_kiosk = 'component_value = kiosk_ui(score=st.session_state.score, chat_response=st.session_state.chat_response, chat_id=st.session_state.chat_id, action_plan=st.session_state.action_plan, key="kiosk")'
new_kiosk = 'component_value = kiosk_ui(score=st.session_state.score, chat_response=st.session_state.chat_response, chat_id=st.session_state.chat_id, action_plan=st.session_state.action_plan, logs=get_memory_log(), rules=fuzzy_engine.get_thresholds(), key="kiosk")'

if old_kiosk in content:
    content = content.replace(old_kiosk, new_kiosk)
else:
    print("WARNING: Could not find old_kiosk in app.py")

# 2. Add set_health_alert action handling
old_action = '''        elif action == "open_admin":
            pass # Ignored since Admin is HTML
        elif action == "simulate_failure":'''

new_action = '''        elif action == "open_admin":
            pass # Ignored since Admin is HTML
        elif action == "set_health_alert":
            st.session_state.health_alert = component_value.get("health_alert", "None")
            st.session_state.last_data = component_value
            st.rerun()
        elif action == "simulate_failure":'''

if old_action in content:
    content = content.replace(old_action, new_action)
else:
    print("WARNING: Could not find action routing block in app.py")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
