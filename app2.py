import streamlit as st
from agents.rfp_extracter_agent import run_rfp_extraction
from agents.compliance_checker import run_compliance_decision
from agents.contractrisk_analyzer import run_contract_risk_analysis
import tempfile
import json

st.set_page_config(page_title="ConsultAdd RFP Analyzer", layout="wide")
st.title("📊 ConsultAdd - RFP Analyzer Suite")

st.markdown("A unified dashboard to understand and evaluate RFPs effectively using AI-driven insights.")

# -------------------- File Upload Section --------------------
with st.sidebar:
    st.header("📂 Upload PDFs")
    rfp_file = st.file_uploader("📎 RFP Document", type=["pdf"])
    company_file = st.file_uploader("🏢 Company Profile", type=["pdf"])

    if not rfp_file or not company_file:
        st.warning("Please upload both RFP and Company PDFs to continue.")


# -------------------- Tabs for Modules --------------------
if rfp_file and company_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_rfp:
        tmp_rfp.write(rfp_file.read())
        rfp_path = tmp_rfp.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_company:
        tmp_company.write(company_file.read())
        company_path = tmp_company.name

    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 Know Your RFP (Chatbot)",
        "📌 Key Requirements & Deal Breakers",
        "✅ Compliance Checker",
        "⚠️ Contract Risk Analyzer"
    ])

    # -------------------- Tab 1: Chatbot --------------------
    with tab1:
        with st.container():
            st.subheader("💬 Ask anything about the RFP")
            st.markdown("This is a smart Q&A agent that helps you understand the uploaded RFP.")
            
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            user_question = st.text_input("Type your question about the RFP...")
            if user_question:
                # You would plug in a Q&A chain here using vector store
                response = "🚧 Chatbot coming soon. This will answer: " + user_question  # Replace with real logic
                st.session_state.chat_history.append((user_question, response))

            for q, a in st.session_state.chat_history[::-1]:
                with st.chat_message("user"):
                    st.write(q)
                with st.chat_message("assistant"):
                    st.write(a)

    # -------------------- Tab 2: RFP Extractor --------------------
    with tab2:
        with st.spinner("🔍 Extracting RFP insights..."):
            rfp_summary = run_rfp_extraction(rfp_path)
        
        st.success("✅ Key RFP Requirements Identified")
        st.markdown("Below are the extracted key requirements and potential deal-breakers:")
        st.markdown(rfp_summary)

    # -------------------- Tab 3: Compliance Checker --------------------
    with tab3:
        with st.spinner("⚖️ Checking compliance with company profile..."):
            compliance_result = run_compliance_decision(rfp_summary, company_path)

        st.success("🎯 Compliance Analysis Complete")
        st.subheader("📋 Compliance Report")
        st.json(compliance_result)

    # -------------------- Tab 4: Contract Risk Analyzer --------------------
    with tab4:
        with st.spinner("🔍 Analyzing contract risks and biased clauses..."):
            risk_report = run_contract_risk_analysis(rfp_path)

        st.success("⚠️ Contract Risk Analysis Done")
        st.subheader("📌 Identified Risks & Suggestions")
        st.markdown(risk_report)

else:
    st.info("👈 Upload both RFP and Company profile PDFs to begin.")
