from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# dfine the class for our crew
@CrewBase
class ResearchAndBlogCrew():
    """ResearchAndBlogCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # define the paths of conif files
    agents_config = "src/research_and_blog_crew/config/agents.yaml"
    tasks_config = "src/research_and_blog_crew/config/tasks.yaml"
    
    # ====== Define Agents ======
    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config = self.agents_config["report_generator"]
        )
        
    @agent
    def blog_writer(self) -> Agent:
        return Agent(
            config = self.agents_config["blog_writer"]
        )
        
    # ====== Define Tasks ======
    # order of task definition matters
    @task
    def research_task(self) -> Task:
        return Task(
            config = self.tasks_config["report_task"]   
        )
        
    def blog_writing_task(self) -> Task:
        return Task(
            config = self.tasks_config["blog_writing_task"],
            outut_file = "blogs/blogs.md"
        )         
        
    # ====== Define Crew ======
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            Process=Process.sequential,
            verbsose=True
        )    