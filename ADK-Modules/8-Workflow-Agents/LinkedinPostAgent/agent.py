from google.adk.agents import SequentialAgent
from .sub_agents import writer_agent,seo_optimizing_agent


root_agent = SequentialAgent(
    name="LinkedIn_Master_Agent",
    description="It's linkedin post root agent, Only asked to user about topics",
    sub_agents=[writer_agent,seo_optimizing_agent]
)