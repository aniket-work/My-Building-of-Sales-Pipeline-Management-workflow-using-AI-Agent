from crewai import Task
from .agents import SalesAgents

class SalesTasks:
    def __init__(self, agents: SalesAgents):
        self.agents = agents
        self.qualification_task = None
        self.development_task = None
        self.closing_task = None

    def create_tasks(self, lead_data: str) -> None:
        self.qualification_task = Task(
            description=f"""
            Analyze this lead data and provide a detailed qualification assessment. 
            Lead data: {lead_data}

            IMPORTANT: Format your response EXACTLY as shown below:
            Lead Score: [cold/warm/hot]
            Deal Size: [small/medium/large]
            Reasoning: [Your detailed analysis]
            Next Steps: [Your recommended actions]
            """,
            expected_output="A structured lead qualification assessment with score, size, reasoning, and next steps",
            agent=self.agents.lead_qualifier_agent
        )

        self.development_task = Task(
            description=f"""
            Based on the initial qualification, develop an engagement strategy.
            Lead data: {lead_data}

            IMPORTANT: Format your response EXACTLY as shown below:
            Engagement Strategy: [Your detailed approach]
            Key Requirements: [List of requirements]
            Risk Factors: [List of risks]
            Timeline: [Proposed timeline]
            """,
            expected_output="A detailed engagement strategy with requirements, risks, and timeline",
            agent=self.agents.sales_agent
        )

        self.closing_task = Task(
            description=f"""
            Review the opportunity and prepare a closing strategy.
            Lead data: {lead_data}

            IMPORTANT: Format your response EXACTLY as shown below:
            Proposed Terms: [List of terms]
            Potential Objections: [List of objections]
            Closing Strategy: [Your detailed approach]
            Success Probability: [Percentage]
            """,
            expected_output="A comprehensive closing strategy with terms, objections, and success probability",
            agent=self.agents.closing_agent
        )