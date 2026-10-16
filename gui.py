import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage

# Import our custom tools from tools.py
from tools import verify_drug_batch, check_clinic_inventory, evaluate_patient_triage

# Page Configuration
st.set_page_config(
    page_title="BioGuard AI | Clinical Assistant",
    page_icon="🩺",
    layout="wide"
)

# Load Environment Variables
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    st.error("⚠️ GROQ_API_KEY is missing from your .env file!")
    st.stop()

# Initialize Tools & Model
tools_list = [verify_drug_batch, check_clinic_inventory, evaluate_patient_triage]
tools_map = {tool.name: tool for tool in tools_list}

llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    groq_api_key=groq_key,
    temperature=0
).bind_tools(tools_list)

# App Title & Header
st.title("🩺 BioGuard AI")
st.caption("Autonomous Emergency Triage & Medication Safety Platform for Rural Clinics")
st.markdown("---")

# Sidebar - Quick Actions
with st.sidebar:
    st.header("📋 Clinic Quick Actions")
    st.markdown("Use these quick templates to test agent capabilities:")
    
    if st.button("🔍 Check Batch BATCH-FAKE-009"):
        st.session_state.user_input = "Please verify medicine batch BATCH-FAKE-009 and check if we have Amoxicillin in stock at the clinic."
        
    if st.button("🚨 Emergency Patient Triage"):
        st.session_state.user_input = "Patient has SpO2 of 88%, heart rate 115 bpm, temperature 101.5 F, and complains of severe chest pain. Evaluate triage priority."

    st.markdown("---")
    st.info("💡 **Tip:** BioGuard AI autonomously decides which internal clinical tools to execute based on your input.")

# Main Input Section
user_query = st.text_area("Enter Patient Vitals, Drug Batch Numbers, or Clinical Inquiries:", 
                          value=st.session_state.get("user_input", ""), 
                          height=100,
                          placeholder="e.g., Check batch BATCH-AMX-2026 and evaluate vitals: SpO2 96%, HR 80 bpm, Temp 98.6 F.")

if st.button("🚀 Run BioGuard Analysis", type="primary"):
    if not user_query.strip():
        st.warning("Please enter a query or select a quick action template from the sidebar.")
    else:
        st.subheader("🤖 Agent Execution Logs")
        
        messages = [
            ("system", "You are BioGuard AI, an expert autonomous assistant for rural clinical triage and drug verification. Always use available tools when factual clinic data, batch verification, or triage analysis is needed."),
            HumanMessage(content=user_query)
        ]

        # Container for live status updates
        with st.status("Analyzing clinical input and calling tools...", expanded=True) as status:
            max_iterations = 5
            iteration = 0

            while iteration < max_iterations:
                iteration += 1
                ai_msg = llm.invoke(messages)
                messages.append(ai_msg)

                if ai_msg.tool_calls:
                    for tool_call in ai_msg.tool_calls:
                        tool_name = tool_call["name"]
                        selected_tool = tools_map.get(tool_name)

                        if selected_tool:
                            st.write(f"⚙️ **Executing Tool:** `{tool_name}` with parameters `{tool_call['args']}`")
                            tool_output = selected_tool.invoke(tool_call['args'])
                            st.write(f"📋 **Result:** {tool_output}")
                            messages.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call["id"]))
                else:
                    status.update(label="Analysis complete!", state="complete", expanded=False)
                    break

        st.subheader("🎉 Clinical Assessment & Recommendations")
        st.markdown(ai_msg.content)