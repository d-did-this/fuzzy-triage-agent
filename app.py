import streamlit as st
import plotly.graph_objects as go
import fuzzy_engine
import json
import re
import os
import datetime
from openai import OpenAI
from agentic_tools import check_symptoms, check_drug_safety

# --- MEMORY LOG HELPERS ---
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

# --- PAGE CONFIG & CSS ---
st.set_page_config(page_title="HealthAgent Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Premium Dark Theme Variables */
    :root {
        --bg-color: #0b0f19;
        --card-bg: rgba(30, 41, 59, 0.7);
        --border-color: rgba(255, 255, 255, 0.1);
        --primary: #3b82f6;
        --primary-glow: rgba(59, 130, 246, 0.5);
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e293b 0%, var(--bg-color) 100%);
        color: #f8fafc;
    }

    /* Glassmorphism Containers */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 3rem !important;
        font-weight: 900 !important;
        color: #fff !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.2rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Sliders */
    .stSlider > div > div > div > div {
        background-color: var(--primary) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Chat Bubbles */
    [data-testid="stChatMessage"] {
        background-color: rgba(15, 23, 42, 0.6);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(51, 65, 85, 0.5);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 700 !important;
        background: linear-gradient(to right, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "score" not in st.session_state:
    st.session_state.score = -1.0
if "tier" not in st.session_state:
    st.session_state.tier = "Unknown"
if "lab_data" not in st.session_state:
    st.session_state.lab_data = {
        "hb": 15.0, "wbc": 7.0, "plt": 250.0, "neu": 55.0, 
        "mcv": 88.0, "rdw": 13.0, "egfr": 110.0, "creat": 85.0
    }
if "patient_name" not in st.session_state:
    st.session_state.patient_name = "Patient"
if "agent_chat_history" not in st.session_state:
    st.session_state.agent_chat_history = [
        {"role": "system", "content": "You are a proactive educational triage nurse and Hospital System Manager. You have the ability to adjust clinical thresholds based on external health alerts using your tools."}
    ]
if "messages" not in st.session_state:
    st.session_state.messages = []
if "health_alert" not in st.session_state:
    st.session_state.health_alert = "None"
if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None

# --- DEEPSEEK CLIENT ---
try:
    deepseek_api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
except:
    deepseek_api_key = ""

deepseek_client = None
if deepseek_api_key:
    try:
        deepseek_client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
    except Exception as e:
        st.sidebar.error(f"Failed to load DeepSeek: {e}")
else:
    st.sidebar.warning("Missing DEEPSEEK_API_KEY in secrets.")

# --- ADMIN SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛡️ System Admin")
    admin_pass = st.text_input("Admin Password", type="password")
    
    if admin_pass == "admin123":
        st.success("Admin Mode Active")
        st.session_state.health_alert = st.text_area("Simulate Health Alert (e.g. Dengue Outbreak)", value=st.session_state.health_alert)
        
        st.markdown("#### Reflection Trigger")
        if st.button("Simulate Rule Failure"):
            st.session_state.agent_chat_history.append({
                "role": "user",
                "content": "SYSTEM ALERT: The hospital reports that your recent fuzzy threshold adjustments have resulted in a spike in false positives. Please reflect on this failure and explain how you will reduce your threshold shift aggressiveness moving forward."
            })
            st.warning("Failure injected.")
            
        st.markdown("#### Experience Log")
        log_data = get_memory_log()
        if log_data:
            st.dataframe(log_data)
        else:
            st.info("No logs yet.")
    elif admin_pass:
        st.error("Invalid credentials.")

# --- MAIN LAYOUT ---
st.title("HealthAgent Pro")
st.markdown("Real-time Agentic Fuzzy Logic Triage System")

col_input, col_dash, col_chat = st.columns([1.2, 1.5, 1.5], gap="large")

# === COLUMN 1: INPUTS ===
with col_input:
    st.subheader("Patient Profile")
    st.session_state.patient_name = st.text_input("Full Name", value=st.session_state.patient_name)
    
    with st.expander("🤔 What makes this AI Special?", expanded=False):
        st.markdown("""
        **Fuzzy vs Crisp Logic:** Standard hospital systems use strict "crisp" cutoffs (e.g., if Temp > 38.0 = High Risk). Our Agentic system uses mathematical **Fuzzy Inference**, mapping values to a smooth gradient. A borderline lab value won't trigger a false alarm, but combined with other borderline values, the Fuzzy Engine calculates a holistic, highly accurate risk score.
        """)
    
    st.subheader("🧪 Haematology")
    hb = st.slider("Haemoglobin (g/dL)", 5.0, 25.0, st.session_state.lab_data["hb"], 0.1)
    wbc = st.slider("WBC (x10^9/L)", 1.0, 30.0, st.session_state.lab_data["wbc"], 0.1)
    plt = st.slider("Platelets (x10^9/L)", 10.0, 600.0, st.session_state.lab_data["plt"], 1.0)
    neu = st.slider("Neutrophils (%)", 10.0, 95.0, st.session_state.lab_data["neu"], 0.1)
    mcv = st.slider("MCV (fL)", 50.0, 130.0, st.session_state.lab_data["mcv"], 1.0)
    rdw = st.slider("RDW (%)", 10.0, 25.0, st.session_state.lab_data["rdw"], 0.1)
    
    st.subheader("💧 Renal Panel")
    egfr = st.slider("eGFR (mL/min)", 5.0, 150.0, st.session_state.lab_data["egfr"], 1.0)
    creat = st.slider("Creatinine (umol/L)", 30.0, 400.0, st.session_state.lab_data["creat"], 1.0)
    
    if st.button("Calculate Risk", use_container_width=True):
        st.session_state.lab_data = {"hb": hb, "wbc": wbc, "plt": plt, "neu": neu, "mcv": mcv, "rdw": rdw, "egfr": egfr, "creat": creat}
        try:
            score = fuzzy_engine.assess_patient(st.session_state.lab_data)
            st.session_state.score = score
            if score < 40: st.session_state.tier = "Normal"
            elif score < 60: st.session_state.tier = "Mild"
            elif score < 80: st.session_state.tier = "Moderate"
            else: st.session_state.tier = "Severe"
        except Exception as e:
            st.session_state.score = -1.0
            st.error(f"Fuzzy Engine Error: {e}")

# === COLUMN 2: DASHBOARD ===
with col_dash:
    st.subheader("📊 Clinical Dashboard")
    
    if st.session_state.score >= 0:
        # Score Metric
        metric_color = "#10b981" if st.session_state.tier == "Normal" else "#f59e0b" if st.session_state.tier in ["Mild", "Moderate"] else "#ef4444"
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border: 1px solid {metric_color}; border-radius: 16px; background: rgba(0,0,0,0.2);">
            <div style="font-size: 20px; color: #94a3b8; text-transform: uppercase;">Overall Risk Score</div>
            <div style="font-size: 80px; font-weight: 900; color: {metric_color}; line-height: 1;">{int(st.session_state.score)}</div>
            <div style="font-size: 24px; font-weight: bold; color: {metric_color};">{st.session_state.tier} Risk</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Radar Chart
        categories = ['Hb', 'WBC', 'PLT', 'NEU', 'MCV', 'RDW', 'eGFR', 'Creat']
        
        # Normalize values roughly for radar chart scale 0-100 to make it look good
        # This is purely visual normalization relative to normal ranges
        d = st.session_state.lab_data
        norm_vals = [
            (d['hb']/25)*100, (d['wbc']/30)*100, (d['plt']/600)*100, (d['neu']/95)*100, 
            (d['mcv']/130)*100, (d['rdw']/25)*100, (d['egfr']/150)*100, (d['creat']/400)*100
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=norm_vals, theta=categories, fill='toself',
            name='Patient', line_color=metric_color, fillcolor=metric_color.replace(')', ', 0.3)').replace('rgb', 'rgba') if 'rgb' in metric_color else metric_color + '40'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], showticklabels=False), bgcolor="rgba(0,0,0,0)"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("The AI Nurse will provide detailed findings based on these results. Ask a question to the right!")
        
    else:
        st.markdown("<div style='text-align:center; color:#94a3b8; padding:50px 0;'>Adjust sliders and click 'Calculate Risk' to generate report.</div>", unsafe_allow_html=True)

# === COLUMN 3: AI NURSE CHAT ===
# Tool Schema
GROQ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_symptoms",
            "description": "Returns common symptoms based on eGFR thresholds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "egfr_value": {"type": "number"}
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
                    "medication_name": {"type": "string"},
                    "egfr_value": {"type": "number"}
                },
                "required": ["medication_name", "egfr_value"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_fis_thresholds",
            "description": "Dynamically update a fuzzy logic threshold for a specific variable. Used to react to outbreaks or health alerts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "variable_name": {"type": "string"},
                    "category": {"type": "string"},
                    "new_range": {
                        "type": "array",
                        "items": {"type": "number"}
                    },
                    "reasoning": {"type": "string"}
                },
                "required": ["variable_name", "category", "new_range", "reasoning"]
            }
        }
    }
]

with col_chat:
    st.subheader("🩺 AI Triage Nurse")
    
    chat_container = st.container(height=500)
    
    for msg in st.session_state.messages:
        with chat_container.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    c1, c2, c3 = st.columns(3)
    if c1.button("📊 Explain Score", use_container_width=True): st.session_state.preset_prompt = "Can you explain my risk score?"
    if c2.button("🥗 Dietary Advice", use_container_width=True): st.session_state.preset_prompt = "What dietary changes should I make?"
    if c3.button("⚠️ Red Flags?", use_container_width=True): st.session_state.preset_prompt = "Are there any critical red flags?"

    prompt = st.chat_input("Ask about symptoms or meds...")
    if st.session_state.preset_prompt:
        prompt = st.session_state.preset_prompt
        st.session_state.preset_prompt = None

    if prompt:
        with chat_container.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        full_lab_report = ", ".join([f"{k.upper()}: {v}" for k, v in st.session_state.lab_data.items()])
        sys_context = f"System Context: You are an empathetic triage nurse. Patient Name: {st.session_state.patient_name}. Labs: [{full_lab_report}]. Risk Score: {st.session_state.score} ({st.session_state.tier}).\n\nEXTERNAL HEALTH ALERT: {st.session_state.health_alert}\nIf the health alert requires proactive action, use adjust_fis_thresholds to safely widen or narrow clinical parameters to adapt to the outbreak.\n\nRule 1: Greet the user by name if they say hello. Rule 2: ONLY use tools if asked a medical question, meds, symptoms, or if the HEALTH ALERT demands it. Rule 3: Base advice on the lab report. Rule 4: Always provide final answer in warm English. NEVER output raw JSON/XML tags in normal text.\n\nUser: "
        
        full_prompt = sys_context + prompt
        st.session_state.agent_chat_history.append({"role": "user", "content": full_prompt})
        
        with chat_container.chat_message("assistant"):
            if deepseek_client:
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
                            f_name = tool_call.function.name
                            f_args = json.loads(tool_call.function.arguments)
                            
                            if f_name == "check_symptoms":
                                f_res = check_symptoms(egfr_value=f_args.get("egfr_value", 0))
                            elif f_name == "check_drug_safety":
                                f_res = check_drug_safety(f_args.get("medication_name", ""), f_args.get("egfr_value", 0))
                            elif f_name == "adjust_fis_thresholds":
                                f_res = fuzzy_engine.adjust_fis_thresholds(
                                    f_args.get("variable_name"), f_args.get("category"), f_args.get("new_range")
                                )
                                append_memory_log({
                                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "action": f"Adjusted {f_args.get('variable_name')} to {f_args.get('new_range')}",
                                    "reason": f_args.get("reasoning", "")
                                })
                            else:
                                f_res = "Unknown tool"
                                
                            st.session_state.agent_chat_history.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": f_name,
                                "content": str(f_res),
                            })
                            
                        second_response = deepseek_client.chat.completions.create(
                            model="deepseek-chat",
                            messages=st.session_state.agent_chat_history
                        )
                        final_message = second_response.choices[0].message
                        clean_content = re.sub(r'<function=.*?</function>', '', final_message.content or '', flags=re.DOTALL).strip()
                        
                        st.session_state.agent_chat_history.append({"role": "assistant", "content": final_message.content})
                        if clean_content:
                            st.markdown(clean_content)
                            st.session_state.messages.append({"role": "assistant", "content": clean_content})
                    else:
                        clean_content = re.sub(r'<function=.*?</function>', '', response_message.content or '', flags=re.DOTALL).strip()
                        if clean_content:
                            st.markdown(clean_content)
                            st.session_state.messages.append({"role": "assistant", "content": clean_content})
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("DeepSeek client not configured.")
