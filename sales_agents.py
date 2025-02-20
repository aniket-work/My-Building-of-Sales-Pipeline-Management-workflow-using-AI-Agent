from crewai import Agent

class SalesAgents:
    def __init__(self):
        self.lead_qualifier_agent = Agent(
            role="Lead Qualification Specialist",
            goal="Analyze and qualify incoming sales leads based on specific criteria",
            backstory="""You are an expert at evaluating potential customers and 
                      determining their likelihood to convert based on various factors.
                      You always provide structured, clear assessments following the exact
                      format requested.""",
            verbose=True,
            allow_delegation=False
        )

        self.sales_agent = Agent(
            role="Sales Development Representative",
            goal="Develop qualified leads into concrete opportunities with clear strategies",
            backstory="""You excel at building relationships with prospects and 
                      identifying their specific needs and pain points. You always
                      provide structured strategies following the exact format requested.""",
            verbose=True,
            allow_delegation=False
        )

        self.closing_agent = Agent(
            role="Senior Sales Closer",
            goal="Convert opportunities into closed deals using proven closing techniques",
            backstory="""You are skilled at negotiating terms, handling objections,
                      and closing high-value sales opportunities. You always provide
                      structured closing plans following the exact format requested.""",
            verbose=True,
            allow_delegation=False
        )