import streamlit as st
import streamlit.components.v1 as components
import fuzzy_engine
import urllib.parse
import json
import re
from groq import Groq
from agentic_tools import check_symptoms, check_drug_safety

# 1. Page Config
st.set_page_config(page_title="HealthAgent Pro", layout="wide", initial_sidebar_state="collapsed")

# Setup Groq Agent
try:
    groq_api_key = st.secrets.get("GROQ_API_KEY", "")
except Exception:
    groq_api_key = ""

if not groq_api_key:
    st.warning("GROQ_API_KEY is missing from st.secrets. Agent will not work.")
    groq_client = None
else:
    try:
        groq_client = Groq(api_key=groq_api_key)
    except Exception as e:
        groq_client = None
        st.warning(f"Failed to initialize Groq client: {e}")

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
        top: 20px !important;
        right: 20px !important;
        z-index: 999999 !important;
        background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4) !important;
        border-radius: 30px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        width: auto !important;
    }
    
    .stApp .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
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
        padding: 10px;
        margin-bottom: 10px;
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

# 5. Render Component
# This renders the Kiosk UI. If we have a computed score, we pass it back into the Javascript args.score
component_value = kiosk_ui(score=st.session_state.score, key="kiosk")

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
        else:
            # Process the 8 parameters through the mathematical Fuzzy Engine
            try:
                # filter out 'action' key
                lab_data = {k: v for k, v in component_value.items() if k != "action"}
                new_score = fuzzy_engine.assess_patient(lab_data)
                st.session_state.score = new_score
            except Exception as e:
                st.session_state.score = -1
                print(f"Error calculating score: {e}")
                
                
            st.session_state.last_data = component_value
            st.rerun()

# Floating Native Chat Button
if st.button("🤖 AI Nurse"):
    st.session_state.show_chat = True
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
    }
]

@st.dialog("🩺 AI Triage Nurse", width="large")
def chat_popup():
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("❌ Close", use_container_width=True):
            st.session_state.show_chat = False
            st.rerun()
            
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "groq_chat_history" not in st.session_state:
        st.session_state.groq_chat_history = [
            {"role": "system", "content": "You are a proactive educational triage nurse. You must use the tools provided to check symptoms and drug safety."}
        ]
        
    messages_container = st.container(height=600)
    
    for message in st.session_state.messages:
        with messages_container.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your symptoms or medications..."):
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
            
        full_lab_report = ", ".join([f"{k.upper()}: {v}" for k, v in st.session_state.last_data.items() if k != "action"]) if st.session_state.last_data else "No lab data provided."
            
        system_context = f"System Context: You are a highly professional, empathetic triage nurse. The patient's complete 8-parameter laboratory report is as follows: [{full_lab_report}]. Their overall calculated Risk Score is {score} ({current_tier}). Rule 1: If the user just says hello, politely greet them back and ask how you can help them understand their report today. DO NOT call any tools for simple greetings. Rule 2: ONLY use your tools if the user asks a medical question, mentions medications, or complains of symptoms. Rule 3: Base all of your advice on the full lab report provided above. If a value is critically high or low, prioritize discussing it. Rule 4: Always provide your final answer in natural, warm English. NEVER output raw JSON or tool names.\nCRITICAL RULE: You must NEVER output XML tags, <function>, or JSON blocks in your normal text responses. If you need to use a tool, use the native tool calling API. Your text response must ONLY be natural, conversational English.\n\nUser Question: "
        
        full_prompt = system_context + prompt
        st.session_state.groq_chat_history.append({"role": "user", "content": full_prompt})
        
        with messages_container.chat_message("assistant"):
            if groq_client is not None:
                try:
                    response = groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=st.session_state.groq_chat_history,
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
                        
                    st.session_state.groq_chat_history.append(assistant_msg)
                    
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
                            else:
                                function_response = "Unknown tool"
                                
                            st.session_state.groq_chat_history.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": str(function_response),
                            })
                        
                        # Second request with tool results
                        second_response = groq_client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=st.session_state.groq_chat_history
                        )
                        final_message = second_response.choices[0].message
                        
                        # Scrub any <function=...> tags from the display text
                        clean_content = re.sub(r'<function=.*?</function>', '', final_message.content or '', flags=re.DOTALL)
                        clean_content = clean_content.strip()
                        
                        st.session_state.groq_chat_history.append({"role": "assistant", "content": final_message.content})
                        
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
                st.warning("Groq client is not configured.")

if st.session_state.get("show_chat", False):
    chat_popup()
