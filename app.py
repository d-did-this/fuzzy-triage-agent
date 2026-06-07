import streamlit as st
import streamlit.components.v1 as components
import fuzzy_engine

# 1. Page Config
st.set_page_config(page_title="HealthAgent Pro", layout="wide", initial_sidebar_state="collapsed")

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
