from google.adk.agents import LoopAgent
from .sub_agents import writer_agent,seo_optimizing_agent,critic_agent


root_agent = LoopAgent(
    name="LinkedIn_Master_Agent",
    description="It's linkedin post root agent, Only asked to user about topics",
    sub_agents=[writer_agent,seo_optimizing_agent,critic_agent],
    max_iterations=3
)