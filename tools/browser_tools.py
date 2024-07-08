import requests
from bs4 import BeautifulSoup
from crewai import Agent, Task
from langchain.tools import tool
import os
from langchain_google_genai import ChatGoogleGenerativeAI

class BrowserTools:
    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content"""
        # Fetch the webpage content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print("=====================used===================")
        response = requests.get(website, headers=headers)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text content
        for script in soup(["script", "style"]):
            script.decompose()
        content = soup.get_text(separator="\n")

        # Clean up the text
        lines = (line.strip() for line in content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        content = '\n'.join(chunk for chunk in chunks if chunk)
        print(content)
        # Split content into chunks
        content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]

        summaries = []
        for chunk in content_chunks:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing research and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
                llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key = os.getenv("GOOGLE_API_KEY")),
                allow_delegation=False
            )
            task = Task(
                agent=agent,
                description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}',


            )
            summary = task.execute()
            summaries.append(summary)

        return "\n\n".join(summaries)