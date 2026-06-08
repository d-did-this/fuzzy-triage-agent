import streamlit as st
import streamlit.components.v1 as components
import fuzzy_engine
import google.generativeai as genai
from agentic_tools import check_symptoms, check_drug_safety

# 1. Page Config
st.set_page_config(page_title="HealthAgent Pro", layout="wide", initial_sidebar_state="collapsed")

# Setup Gemini Agent
try:
    gemini_api_key = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    gemini_api_key = ""

if not gemini_api_key:
    st.warning("GEMINI_API_KEY is missing from st.secrets. Agent will not work.")
else:
    genai.configure(api_key=gemini_api_key)

try:
    agent_model = genai.GenerativeModel('gemini-1.5-flash', tools=[check_symptoms, check_drug_safety])
except Exception as e:
    agent_model = None
    st.warning(f"Failed to initialize Gemini model: {e}")

# 2. Force Streamlit out of the way (Full-screen iframe injection)
st.markdown("""
<style>
    /* Remove padding/margin from Streamlit main container */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hide header/footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Hide Streamlit Cloud 'Manage App' watermark */
    [data-testid="manage-app-button"] {display: none !important;}
    
    /* Target the App Creator Avatar explicitly */
    [data-testid="appCreatorAvatar"] { 
        display: none !important; 
    }
    
    /* Target the obfuscated Streamlit Logo SVG wrapper */
    div[class^="_link_"] { 
        display: none !important; 
    }
    
    /* Target the parent container of the new profile badge */
    div[class^="_profileContainer_"], 
    div[class^="_container_"] { 
        display: none !important; 
    }
    
    /* --- BUTTON SAFE ZONES --- */
    .stButton {
        margin-top: 15px;
        margin-bottom: 40px; /* Safe zone for mobile swiping */
        display: flex;
        justify-content: center;
    }

    /* Force iframe to cover the entire viewport without scrollbars */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        display: block;
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

# 5. Render Component
# This renders the Kiosk UI. If we have a computed score, we pass it back into the Javascript args.score
component_value = kiosk_ui(score=st.session_state.score, key="kiosk")

# 6. Bi-directional Logic
if component_value:
    # Check if the user just clicked Generate and sent us new data
    if st.session_state.last_data != component_value:
        
        # Process the 8 parameters through the mathematical Fuzzy Engine
        try:
            new_score = fuzzy_engine.assess_patient(component_value)
            st.session_state.score = new_score
        except Exception as e:
            st.session_state.score = -1
            print(f"Error calculating score: {e}")
            
        st.session_state.last_data = component_value
        
        # Rerun Streamlit. This forces `kiosk_ui()` to be called again on line 42
        # which instantly drops the newly calculated score right into the Javascript listener!
        st.rerun()

# 7. Agentic Chatbot Interface
st.markdown("### Educational Triage Nurse")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your symptoms or medications..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    current_egfr = "Unknown"
    current_creat = "Unknown"
    current_tier = "Unknown"
    
    if st.session_state.last_data:
        current_egfr = st.session_state.last_data.get('egfr', 'Unknown')
        current_creat = st.session_state.last_data.get('creat', 'Unknown')
    
    if st.session_state.score is not None and st.session_state.score >= 0:
        score = st.session_state.score
        if score < 40: current_tier = "Normal"
        elif score < 60: current_tier = "Mild"
        elif score < 80: current_tier = "Moderate"
        else: current_tier = "Severe"
        
    system_context = f"System Context: The patient currently has an eGFR of {current_egfr} and a Creatinine of {current_creat}. Their Fuzzy Risk Tier is {current_tier}. If they ask a question, you must use your tools to check their symptoms and drug safety based on these numbers, then proactively educate them.\n\nUser Question: "
    
    full_prompt = system_context + prompt
    
    with st.chat_message("assistant"):
        if 'agent_model' in locals() and agent_model is not None:
            try:
                if "gemini_chat" not in st.session_state:
                    st.session_state.gemini_chat = agent_model.start_chat(enable_automatic_function_calling=True)
                
                response = st.session_state.gemini_chat.send_message(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error communicating with agent: {e}")
        else:
            st.warning("Gemini model is not configured.")

