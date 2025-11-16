import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	ScrapeWebsiteTool,
	FileReadTool
)





@CrewBase
class SocialMediaContentSchedulingAutomationCrew:
    """SocialMediaContentSchedulingAutomation crew"""

    
    @agent
    def social_media_content_creator(self) -> Agent:
        
        return Agent(
            config=self.agents_config["social_media_content_creator"],
            
            
            tools=[				SerperDevTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def social_media_analytics_specialist(self) -> Agent:
        
        return Agent(
            config=self.agents_config["social_media_analytics_specialist"],
            
            
            tools=[				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def social_media_scheduler(self) -> Agent:
        
        return Agent(
            config=self.agents_config["social_media_scheduler"],
            
            
            tools=[				FileReadTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def discover_trending_topics(self) -> Task:
        return Task(
            config=self.tasks_config["discover_trending_topics"],
            markdown=False,
            
            
        )
    
    @task
    def analyze_industry_engagement_patterns(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_industry_engagement_patterns"],
            markdown=False,
            
            
        )
    
    @task
    def generate_content_ideas(self) -> Task:
        return Task(
            config=self.tasks_config["generate_content_ideas"],
            markdown=False,
            
            
        )
    
    @task
    def create_publishing_schedule(self) -> Task:
        return Task(
            config=self.tasks_config["create_publishing_schedule"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the SocialMediaContentSchedulingAutomation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
