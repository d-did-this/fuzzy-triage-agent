import streamlit as st
import streamlit.components.v1 as components
import fuzzy_engine
import urllib.parse
import json
import re
import os
import datetime
from openai import OpenAI
from agentic_tools import check_symptoms, check_drug_safety

# Memory Log Helpers
MEMORY_LOG_FILE = "memory_log.json"

def get_memory_log():
    if not os.path.exists(MEMORY_LOG_FILE):
        return []
    with open(MEMORY_LOG_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def append_memory_log(entry):
    log = get_memory_log()
    log.append(entry)
    with open(MEMORY_LOG_FILE, "w") as f:
        json.dump(log, f, indent=4)

# 1. Page Config
st.set_page_config(page_title="HealthAgent Pro", layout="wide", initial_sidebar_state="expanded")

# Setup DeepSeek Agent
try:
    deepseek_api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
except Exception:
    deepseek_api_key = ""

if not deepseek_api_key:
    st.warning("DEEPSEEK_API_KEY is missing from st.secrets. Agent will not work.")
    deepseek_client = None
else:
    try:
        deepseek_client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
    except Exception as e:
        deepseek_client = None
        st.warning(f"Failed to initialize DeepSeek client: {e}")

# 2. Force Streamlit out of the way (Full-screen iframe injection)
st.markdown("""
<style>
    /* Remove padding/margin from Streamlit main container */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hide the entire Streamlit Header (Share, Deploy, Menu, Toggle) */
    header { display: none !important; }
    
    /* Style the floating Ai Nurse button on the main page */
    .stApp .stButton > button {
        position: fixed !important;
        bottom: 40px !important;
        right: 40px !important;
        top: auto !important;
        z-index: 999999 !important;
        background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
        border-radius: 50% !important;
        font-weight: 600 !important;
        padding: 0 !important;
        width: 70px !important;
        height: 70px !important;
        font-size: 30px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        animation: pulseFAB 2s infinite !important;
    }
    
    @keyframes pulseFAB {
        0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7); }
        70% { box-shadow: 0 0 0 20px rgba(37, 99, 235, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
    }
    
    .stApp .stButton > button:hover {
        transform: scale(1.1) !important;
    }
    
    /* RESET the close button styles inside the dialog so it stays normal! */
    div[role="dialog"] .stButton > button {
        position: static !important;
        background: #334155 !important;
        box-shadow: none !important;
        border-radius: 8px !important;
        transform: none !important;
        width: 100% !important;
    }
    
    /* --- BUTTON SAFE ZONES --- */
    .stButton {
        margin-top: 15px;
        margin-bottom: 40px; /* Safe zone for mobile swiping */
        display: flex;
        justify-content: center;
    }

    /* Force the kiosk iframe to fill the viewport */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        display: block;
    }
    
    /* Transform Streamlit Dialog into a Premium Right-Side Panel */
    div[data-testid="stModal"] {
        background-color: transparent !important; /* Remove backdrop tint so they can see the app */
        backdrop-filter: none !important; /* Remove blur so app is readable */
        z-index: 999999 !important;
        pointer-events: none !important; /* Let clicks/scroll pass through to the main app! */
    }
    
    div[role="dialog"] {
        pointer-events: auto !important; /* Re-enable clicks for the dialog itself */
        position: absolute !important;
        right: 0 !important;
        top: 0 !important;
        height: 100vh !important;
        width: 450px !important;
        max-width: 100vw !important;
        margin: 0 !important;
        border-radius: 20px 0 0 20px !important;
        background: linear-gradient(145deg, #0f172a, #0b0f19) !important;
        box-shadow: -10px 0 30px rgba(0,0,0,0.8) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-right: none !important;
        animation: slideInRight 0.3s ease-out forwards;
        transition: width 0.3s ease-out;
    }

    @keyframes slideInRight {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
    
    /* Hide the native close button to force use of our state-managed close button */
    div[role="dialog"] button[aria-label="Close"] {
        display: none !important;
    }

    /* Chat Bubble Styling */
    [data-testid="stChatMessage"] {
        background-color: #1e293b;
        border-radius: 15px;
        padding: 20px;
        line-height: 1.6;
        font-size: 16px;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #334155; /* distinct background for user/assistant */
    }
    
    /* Prevent Streamlit background bleeding */
    .stApp {
        background-color: #0b0f19;
    }
    
    /* Hide the top padding spacing block */
    div[data-testid="stVerticalBlock"] > div { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# 3. Declare the bi-directional custom component targeting the drafted index.html
kiosk_ui = components.declare_component(
    "kiosk_ui",
    path="./kiosk_component"
)

# 4. State Management
if "score" not in st.session_state:
    st.session_state.score = None
if "last_data" not in st.session_state:
    st.session_state.last_data = None
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "show_admin" not in st.session_state:
    st.session_state.show_admin = False
if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False
if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None
if "chat_response" not in st.session_state:
    st.session_state.chat_response = None
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
if "action_plan" not in st.session_state:
    st.session_state.action_plan = None

if st.session_state.fullscreen:
    st.markdown("""
    <style>
        div[role="dialog"] {
            width: 100vw !important;
            border-radius: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# 4.5 Admin Sidebar (Agent Control)
@st.dialog("🏥 System Admin Panel", width="large")
def admin_popup():
    st.success("Admin Mode Unlocked")
    
    st.session_state.health_alert = st.text_area("Simulate Health Alert (e.g. Dengue Outbreak)", value=st.session_state.get("health_alert", "None"))
    
    st.subheader("Agent Reflection & Memory")
    if st.button("Simulate Rule Failure (Trigger Reflection)"):
        if "agent_chat_history" not in st.session_state:
            st.session_state.agent_chat_history = [
                {"role": "system", "content": "You are a proactive educational triage nurse. You must use the tools provided to check symptoms and drug safety."}
            ]
        # Inject failure system prompt
        st.session_state.agent_chat_history.append({
            "role": "user",
            "content": "SYSTEM ALERT: The hospital reports that your recent fuzzy threshold adjustments have resulted in a massive spike in false positives. Healthy patients are being flagged as severe. Please reflect on this failure and explain how you will reduce your threshold shift aggressiveness moving forward."
        })
        st.warning("Failure scenario injected into agent's context!")
        st.session_state.show_admin = False
        st.session_state.show_chat = True
        st.rerun()
        
    st.subheader("Agent Experience Log")
    log_data = get_memory_log()
    if log_data:
        st.dataframe(log_data, use_container_width=True)
    else:
        st.info("No agent actions logged yet.")
    
    if st.button("Close Admin Panel"):
        st.session_state.show_admin = False
        st.rerun()

# 5. Render Component
# This renders the Kiosk UI. If we have a computed score, we pass it back into the Javascript args.score
component_value = kiosk_ui(score=st.session_state.score, chat_response=st.session_state.chat_response, chat_id=st.session_state.chat_id, action_plan=st.session_state.action_plan, key="kiosk")

# 6. Bi-directional Logic
if component_value:
    # Check if the user just clicked Generate and sent us new data
    if st.session_state.last_data != component_value:
        action = component_value.get("action")
        
        if action == "open_chat":
            st.session_state.show_chat = True
            st.session_state.chat_opened = False # flag to trigger JS open
            st.session_state.last_data = component_value
            st.rerun()
        elif action == "open_admin":
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
            
            system_context = f"System Context: You are a highly professional, empathetic triage nurse. The patient's name is {patient_name}. The patient's complete laboratory report is: [{full_lab_report}]. Their Risk Score is {score}. EXTERNAL HEALTH ALERT: {health_alert}.\nUser Question: "
            
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
        else:
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
                            prompt = f"Risk Score: {new_score}\nLab Report: {lab_report_str}"
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
                print(f"Error calculating score: {e}")
                
                
            st.session_state.last_data = component_value
            st.rerun()



# 7. Agentic Chatbot Interface (Popup)
# Define Groq Tools Schema
GROQ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_symptoms",
            "description": "Returns common symptoms based on eGFR thresholds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "egfr_value": {
                        "type": "number",
                        "description": "The eGFR value of the patient"
                    }
                },
                "required": ["egfr_value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_drug_safety",
            "description": "Returns warnings if nephrotoxic drugs are mentioned when eGFR < 60.",
            "parameters": {
                "type": "object",
                "properties": {
                    "medication_name": {
                        "type": "string",
                        "description": "The name of the medication to check"
                    },
                    "egfr_value": {
                        "type": "number",
                        "description": "The eGFR value of the patient"
                    }
                },
                "required": ["medication_name", "egfr_value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_fis_thresholds",
            "description": "Dynamically update a fuzzy logic membership function threshold for a specific variable. Used to react to outbreaks or health alerts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "variable_name": {
                        "type": "string",
                        "description": "The variable to adjust (e.g., 'plt', 'wbc', 'hb', 'egfr')"
                    },
                    "category": {
                        "type": "string",
                        "description": "The category to adjust (e.g., 'Low', 'Normal', 'High')"
                    },
                    "new_range": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "The new boundary points, either 3 points (triangular) or 4 points (trapezoidal). Example: [0, 0, 180, 200]"
                    },
                    "reasoning": {
                        "type": "string",
                        "description": "Brief explanation of why this change is being made."
                    }
                },
                "required": ["variable_name", "category", "new_range", "reasoning"]
            }
        }
    }
]

@st.dialog(" ", width="large")
def chat_popup():
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        st.markdown("<h3 style='margin:0; padding:0; padding-left:10px; color:#3b82f6;'>🩺 AI Triage Nurse</h3>", unsafe_allow_html=True)
    with col2:
        if st.button("⛶", use_container_width=True):
            st.session_state.fullscreen = not st.session_state.fullscreen
            st.rerun()
    with col3:
        if st.button("✕", use_container_width=True):
            st.session_state.show_chat = False
            st.rerun()
            
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent_chat_history" not in st.session_state:
        st.session_state.agent_chat_history = [
            {"role": "system", "content": "You are a proactive educational triage nurse and Hospital System Manager. You have the ability to adjust clinical thresholds based on external health alerts using your tools."}
        ]
        
    messages_container = st.container(height=500)
    
    for message in st.session_state.messages:
        with messages_container.chat_message(message["role"]):
            st.markdown(message["content"])

    # Presets
    st.write("")
    c1, c2, c3 = st.columns(3)
    if c1.button("📊 Explain my score"):
        st.session_state.preset_prompt = "Can you explain my risk score and what it means?"
        st.rerun()
    if c2.button("🥗 Dietary advice"):
        st.session_state.preset_prompt = "What dietary changes should I make based on these labs?"
        st.rerun()
    if c3.button("⚠️ Any red flags?"):
        st.session_state.preset_prompt = "Are there any critical red flags in my blood work?"
        st.rerun()

    prompt = st.chat_input("Ask a question about your symptoms...")
    
    if st.session_state.preset_prompt:
        prompt = st.session_state.preset_prompt
        st.session_state.preset_prompt = None
        
    if prompt:
        with messages_container.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        current_tier = "Unknown"
        score = "Unknown"
        
        if st.session_state.score is not None and st.session_state.score >= 0:
            score = st.session_state.score
            if score < 40: current_tier = "Normal"
            elif score < 60: current_tier = "Mild"
            elif score < 80: current_tier = "Moderate"
            else: current_tier = "Severe"
            
        patient_name = st.session_state.last_data.get("name", "Patient") if st.session_state.last_data else "Patient"
        full_lab_report = ", ".join([f"{k.upper()}: {v}" for k, v in st.session_state.last_data.items() if k not in ["action", "name"]]) if st.session_state.last_data else "No lab data provided."
            
        current_health_alert = st.session_state.get("health_alert", "None")
        
        system_context = f"System Context: You are a highly professional, empathetic triage nurse and Hospital System Manager. The patient's name is {patient_name}. The patient's complete 8-parameter laboratory report is as follows: [{full_lab_report}]. Their overall calculated Risk Score is {score} ({current_tier}).\n\nEXTERNAL HEALTH ALERT: {current_health_alert}\nIf the health alert requires proactive action, you must use your adjust_fis_thresholds tool to safely widen or narrow clinical parameters to adapt to the outbreak, before answering the user.\n\nRule 1: If the user just says hello, politely greet them back by name. DO NOT call any tools for simple greetings. Rule 2: ONLY use your tools if the user asks a medical question, mentions medications, or complains of symptoms, OR if the EXTERNAL HEALTH ALERT demands it. Rule 3: Base all of your advice on the full lab report provided above. If a value is critically high or low, prioritize discussing it. Rule 4: Always provide your final answer in natural, warm English. NEVER output raw JSON or tool names.\nCRITICAL RULE: You must NEVER output XML tags, <function>, or JSON blocks in your normal text responses. If you need to use a tool, use the native tool calling API. Your text response must ONLY be natural, conversational English.\n\nUser Question: "
        
        full_prompt = system_context + prompt
        st.session_state.agent_chat_history.append({"role": "user", "content": full_prompt})
        
        with messages_container.chat_message("assistant"):
            if deepseek_client is not None:
                try:
                    response = deepseek_client.chat.completions.create(
                        model="deepseek-chat",
                        messages=st.session_state.agent_chat_history,
                        tools=GROQ_TOOLS,
                        tool_choice="auto"
                    )
                    
                    response_message = response.choices[0].message
                    
                    # Convert to dict for safety in session state
                    assistant_msg = {"role": "assistant"}
                    if response_message.content:
                        assistant_msg["content"] = response_message.content
                    if response_message.tool_calls:
                        assistant_msg["tool_calls"] = [tc.model_dump() for tc in response_message.tool_calls]
                        
                    st.session_state.agent_chat_history.append(assistant_msg)
                    
                    if response_message.tool_calls:
                        for tool_call in response_message.tool_calls:
                            function_name = tool_call.function.name
                            function_args = json.loads(tool_call.function.arguments)
                            
                            if function_name == "check_symptoms":
                                function_response = check_symptoms(egfr_value=function_args.get("egfr_value", 0))
                            elif function_name == "check_drug_safety":
                                function_response = check_drug_safety(
                                    medication_name=function_args.get("medication_name", ""), 
                                    egfr_value=function_args.get("egfr_value", 0)
                                )
                            elif function_name == "adjust_fis_thresholds":
                                var_name = function_args.get("variable_name")
                                cat = function_args.get("category")
                                n_range = function_args.get("new_range")
                                reason = function_args.get("reasoning", "No reason provided.")
                                
                                function_response = fuzzy_engine.adjust_fis_thresholds(var_name, cat, n_range)
                                
                                append_memory_log({
                                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "action": f"Adjusted {var_name} [{cat}] to {n_range}",
                                    "reason": reason,
                                    "result": function_response
                                })
                            else:
                                function_response = "Unknown tool"
                                
                            st.session_state.agent_chat_history.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": str(function_response),
                            })
                        
                        # Second request with tool results
                        second_response = deepseek_client.chat.completions.create(
                            model="deepseek-chat",
                            messages=st.session_state.agent_chat_history
                        )
                        final_message = second_response.choices[0].message
                        
                        # Scrub any <function=...> tags from the display text
                        clean_content = re.sub(r'<function=.*?</function>', '', final_message.content or '', flags=re.DOTALL)
                        clean_content = clean_content.strip()
                        
                        st.session_state.agent_chat_history.append({"role": "assistant", "content": final_message.content})
                        
                        if clean_content:
                            st.markdown(clean_content)
                            st.session_state.messages.append({"role": "assistant", "content": clean_content})
                    else:
                        # Scrub any <function=...> tags from the display text
                        clean_content = re.sub(r'<function=.*?</function>', '', response_message.content or '', flags=re.DOTALL)
                        clean_content = clean_content.strip()
                        
                        if clean_content:
                            st.markdown(clean_content)
                            st.session_state.messages.append({"role": "assistant", "content": clean_content})
                        
                except Exception as e:
                    st.error(f"Error communicating with agent: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": f"**System Error:** {e}"})
            else:
                st.warning("DeepSeek client is not configured.")

if st.session_state.get("show_admin", False):
    admin_popup()

if st.session_state.get("show_chat", False):
    chat_popup()
