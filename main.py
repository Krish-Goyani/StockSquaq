from crewai import Crew
from textwrap import dedent
import streamlit as st
from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks
import os

class FinancialCrew:
  def __init__(self, company):
    self.company = company

  def run(self):
    agents = StockAnalysisAgents()
    tasks = StockAnalysisTasks()

    research_analyst_agent = agents.research_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_advisor_agent = agents.investment_advisor()

    research_task = tasks.research(research_analyst_agent, self.company)
    financial_task = tasks.financial_analysis(financial_analyst_agent)
    filings_task = tasks.filings_analysis(financial_analyst_agent)
    recommend_task = tasks.recommend(investment_advisor_agent)

    crew = Crew(
      agents=[
        research_analyst_agent,
        financial_analyst_agent,
        investment_advisor_agent
      ],
      tasks=[
        research_task,
        financial_task,
        filings_task,
        recommend_task
      ],
      verbose=True
    )

    result = crew.kickoff()
    return result


def main():
    st.set_page_config(page_title="Stock Market Analyzer", page_icon="📈")
    
    st.title("Stock Market Analyzer")
    
    # Project details
    st.markdown("""
    This Stock Market Analyzer uses CrewAI to generate detailed reports on companies.
    It leverages multiple AI agents to perform comprehensive analysis:
    - Research Analyst: Gathers general information about the company
    - Financial Analyst: Analyzes financial data and SEC filings
    - Investment Advisor: Provides investment recommendations
    """)
    
    # API Key inputs
    gemini_api = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
    serper_api = st.sidebar.text_input("Enter your Serper API Key:", type="password")
    sec_api = st.sidebar.text_input("Enter your SEC API Key:", type="password")
    
    # Set environment variables
    os.environ['GEMINI_API_KEY'] = gemini_api
    os.environ['SERPER_API_KEY'] = serper_api
    os.environ['SEC_API_KEY'] = sec_api
    
    # Company input
    company = st.text_input("Enter the company name you want to analyze:")
    
    if st.button("Analyze"):
        if company and gemini_api and serper_api and sec_api:
            with st.spinner("Analyzing... This may take a few minutes."):
                financial_crew = FinancialCrew(company)
                result = financial_crew.run()
                
                st.success("Analysis complete!")
                st.subheader("Analysis Report")
                st.markdown(result)
        else:
            st.warning("Please enter all required information (API keys and company name).")

if __name__ == "__main__":
    main()