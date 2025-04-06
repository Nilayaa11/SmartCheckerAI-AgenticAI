import streamlit as st
from agents.rfp_extracter_agent import run_rfp_extraction
from agents.compliance_checker import run_compliance_decision
import tempfile
import json

st.set_page_config(page_title="RFP Eligibility Validator", layout="wide")
st.title("📄 RFP Eligibility & Compliance Validator")

st.markdown("Upload both the RFP and Company Profile PDFs to analyze eligibility based on the project requirements.")

# -------------------- Upload PDFs --------------------
rfp_file = st.file_uploader("📎 Upload RFP Document", type=["pdf"])
company_file = st.file_uploader("🏢 Upload Company Profile", type=["pdf"])

# -------------------- Process --------------------
if rfp_file and company_file:
    with st.spinner("🔍 Extracting information from RFP..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_rfp:
            tmp_rfp.write(rfp_file.read())
            rfp_path = tmp_rfp.name

        rfp_summary = run_rfp_extraction(rfp_path)

    st.success("✅ RFP Summary Extracted!")
    st.subheader("📋 RFP Summary")
    st.markdown(rfp_summary)



    with st.spinner("⚖️ Validating Company Compliance..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_company:
            tmp_company.write(company_file.read())
            company_path = tmp_company.name

        compliance_result = run_compliance_decision(rfp_summary, company_path)

    st.success("🎯 Compliance Validation Done!")

    st.subheader("✅ Final Compliance Decision")
    st.json(compliance_result)

else:
    st.info("📂 Please upload both the RFP and Company Profile PDFs.")
