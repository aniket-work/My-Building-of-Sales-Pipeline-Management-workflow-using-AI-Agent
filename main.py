import streamlit as st
import os
import json
import yaml
import logging
from crewai import Crew

from sales_agents import SalesAgents
from sales_tasks import SalesTasks
from response_processor import process_ai_response
from data_manager import save_lead_data, load_lead_history
from ui_components import render_sidebar, render_lead_form, render_analysis_results

# Load configuration
with open('settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(level=getattr(logging, config['logging']['level']))

# Configure Streamlit page
st.set_page_config(**config['page_config'])


# Apply custom CSS
st.markdown(f"<style>{config['styles']['custom_css']}</style>", unsafe_allow_html=True)


def main():
    # Render sidebar and get navigation selection
    api_key, page = render_sidebar()

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    if page == "New Lead Analysis":
        col1, col2 = st.columns([2, 1])

        with col1:
            # Render lead form
            lead_data = render_lead_form()

            if st.button("Analyze Lead"):
                if not api_key:
                    st.error("Please enter your OpenAI API Key in the sidebar.")
                    return

                with st.spinner("Analyzing lead... This may take a few minutes."):
                    try:
                        # Initialize agents and tasks
                        agents = SalesAgents()
                        tasks = SalesTasks(agents)
                        tasks.create_tasks(json.dumps(lead_data, indent=2))

                        # Create and execute crews
                        qual_crew = Crew(
                            agents=[agents.lead_qualifier_agent],
                            tasks=[tasks.qualification_task],
                            verbose=True
                        )

                        dev_crew = Crew(
                            agents=[agents.sales_agent],
                            tasks=[tasks.development_task],
                            verbose=True
                        )

                        close_crew = Crew(
                            agents=[agents.closing_agent],
                            tasks=[tasks.closing_task],
                            verbose=True
                        )

                        # Execute tasks and collect results
                        qual_result = qual_crew.kickoff()
                        dev_result = dev_crew.kickoff()
                        close_result = close_crew.kickoff()

                        # Combine results
                        combined_result = f"""
                        # Lead Qualification
                        {qual_result}

                        # Development Strategy
                        {dev_result}

                        # Closing Strategy
                        {close_result}
                        """

                        # Process and display results
                        analysis = process_ai_response(combined_result)
                        if analysis:
                            save_lead_data(lead_data, str(analysis))
                            with col2:
                                render_analysis_results(analysis)

                    except Exception as e:
                        logging.error(f"Error during execution: {str(e)}")
                        st.error(f"An error occurred: {str(e)}")
                        st.error("Please try again or contact support if the error persists.")

    else:  # Lead History page
        st.subheader("Lead History")
        df = load_lead_history()
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No leads analyzed yet.")


if __name__ == "__main__":
    main()