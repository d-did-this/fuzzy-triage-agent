import os

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We need to add session state for chat response and chat id
state_init = '''if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None'''

state_init_new = '''if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None
if "chat_response" not in st.session_state:
    st.session_state.chat_response = None
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None'''
if 'st.session_state.chat_response' not in content:
    content = content.replace(state_init, state_init_new)

# 2. We need to pass chat_response and chat_id to kiosk_ui
old_kiosk = '''component_value = kiosk_ui(score=st.session_state.score, key="kiosk")'''
new_kiosk = '''component_value = kiosk_ui(score=st.session_state.score, chat_response=st.session_state.chat_response, chat_id=st.session_state.chat_id, key="kiosk")'''
if old_kiosk in content:
    content = content.replace(old_kiosk, new_kiosk)

# 3. Handle new actions
old_logic = '''        elif action == "open_admin":
            st.session_state.show_admin = True
            st.rerun()
        else:'''

import uuid
new_logic = '''        elif action == "open_admin":
            pass # Ignored since Admin is HTML
        elif action == "simulate_failure":
            if "agent_chat_history" not in st.session_state:
                st.session_state.agent_chat_history = [
                    {"role": "system", "content": "You are a proactive educational triage nurse."}
                ]
            st.session_state.agent_chat_history.append({
                "role": "user",
                "content": "SYSTEM ALERT: The hospital reports that your recent fuzzy threshold adjustments have resulted in a massive spike in false positives. Please reflect on this failure."
            })
            st.session_state.chat_response = "I have received a System Alert regarding my recent threshold adjustments. I am currently reflecting on this failure and will prioritize safety."
            import uuid
            st.session_state.chat_id = str(uuid.uuid4())
            st.rerun()
        elif action == "chat_message":
            prompt = component_value.get("prompt", "")
            health_alert = component_value.get("health_alert", "None")
            patient_name = component_value.get("name", "Patient")
            
            score = st.session_state.score if st.session_state.score is not None else -1
            full_lab_report = ", ".join([f"{k.upper()}: {v}" for k, v in st.session_state.last_data.items() if k not in ["action", "name", "prompt", "health_alert"]]) if st.session_state.last_data else "No lab data provided."
            
            system_context = f"System Context: You are a highly professional, empathetic triage nurse. The patient's name is {patient_name}. The patient's complete laboratory report is: [{full_lab_report}]. Their Risk Score is {score}. EXTERNAL HEALTH ALERT: {health_alert}.\\nUser Question: "
            
            full_prompt = system_context + prompt
            st.session_state.agent_chat_history.append({"role": "user", "content": full_prompt})
            
            if deepseek_client is not None:
                try:
                    response = deepseek_client.chat.completions.create(
                        model="deepseek-chat",
                        messages=st.session_state.agent_chat_history,
                        tools=GROQ_TOOLS,
                        tool_choice="auto"
                    )
                    
                    response_message = response.choices[0].message
                    assistant_msg = {"role": "assistant"}
                    if response_message.content: assistant_msg["content"] = response_message.content
                    if response_message.tool_calls: assistant_msg["tool_calls"] = [tc.model_dump() for tc in response_message.tool_calls]
                        
                    st.session_state.agent_chat_history.append(assistant_msg)
                    
                    if response_message.tool_calls:
                        for tool_call in response_message.tool_calls:
                            function_name = tool_call.function.name
                            function_args = json.loads(tool_call.function.arguments)
                            
                            if function_name == "check_symptoms": function_response = check_symptoms(egfr_value=function_args.get("egfr_value", 0))
                            elif function_name == "check_drug_safety": function_response = check_drug_safety(function_args.get("medication_name", ""), function_args.get("egfr_value", 0))
                            elif function_name == "adjust_fis_thresholds":
                                function_response = fuzzy_engine.adjust_fis_thresholds(function_args.get("variable_name"), function_args.get("category"), function_args.get("new_range"))
                                append_memory_log({
                                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "action": f"Adjusted {function_args.get('variable_name')} to {function_args.get('new_range')}",
                                    "reason": function_args.get("reasoning", "")
                                })
                            else: function_response = "Unknown tool"
                                
                            st.session_state.agent_chat_history.append({"tool_call_id": tool_call.id, "role": "tool", "name": function_name, "content": str(function_response)})
                        
                        second_response = deepseek_client.chat.completions.create(model="deepseek-chat", messages=st.session_state.agent_chat_history)
                        final_message = second_response.choices[0].message
                        
                        import re
                        clean_content = re.sub(r'<function=.*?</function>', '', final_message.content or '', flags=re.DOTALL).strip()
                        st.session_state.agent_chat_history.append({"role": "assistant", "content": final_message.content})
                        
                        st.session_state.chat_response = clean_content
                    else:
                        import re
                        clean_content = re.sub(r'<function=.*?</function>', '', response_message.content or '', flags=re.DOTALL).strip()
                        st.session_state.chat_response = clean_content
                        
                except Exception as e:
                    st.session_state.chat_response = f"**System Error:** {e}"
            else:
                st.session_state.chat_response = "DeepSeek client is not configured."
                
            import uuid
            st.session_state.chat_id = str(uuid.uuid4())
            st.rerun()
        else:'''

if old_logic in content:
    content = content.replace(old_logic, new_logic)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS")
