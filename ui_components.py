import streamlit as st
from typing import Dict, Any, Tuple
from constants import INDUSTRIES, REVENUE_RANGES, TIMELINES


def render_sidebar() -> Tuple[str, str]:
    """Render sidebar with configuration and navigation"""
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("OpenAI API Key", type="password")

        st.header("Navigation")
        page = st.radio("Select Page", ["New Lead Analysis", "Lead History"])

        return api_key, page


def render_lead_form() -> Dict[str, Any]:
    """Render the lead information form"""
    st.subheader("Lead Information")

    lead_data = {
        "company_name": st.text_input("Company Name"),
        "industry": st.selectbox("Industry", INDUSTRIES),
        "annual_revenue": st.selectbox("Annual Revenue", REVENUE_RANGES),
        "pain_points": st.text_area("Pain Points"),
        "contact_name": st.text_input("Contact Name"),
        "contact_position": st.text_input("Contact Position"),
        "budget": st.text_input("Budget Range"),
        "timeline": st.selectbox("Timeline", TIMELINES)
    }

    return lead_data


def render_analysis_results(analysis: Dict[str, Any]) -> None:
    """Render the analysis results"""
    st.subheader("Analysis Results")

    # Lead Qualification
    st.markdown("### Lead Qualification")
    qual = analysis['lead_qualification']
    st.info(f"Lead Score: {qual.get('score', 'N/A')}")
    st.info(f"Deal Size: {qual.get('deal_size', 'N/A')}")
    with st.expander("View Reasoning"):
        st.write(qual.get('reasoning', 'N/A'))

    # Development Strategy
    st.markdown("### Development Strategy")
    dev = analysis['development_strategy']
    with st.expander("View Strategy"):
        st.write(dev.get('strategy', 'N/A'))
    with st.expander("Key Requirements"):
        st.write(dev.get('requirements', 'N/A'))

    # Closing Strategy
    st.markdown("### Closing Strategy")
    close = analysis['closing_strategy']
    st.success(f"Success Probability: {close.get('probability', 'N/A')}")
    with st.expander("View Strategy"):
        st.write(close.get('strategy', 'N/A'))