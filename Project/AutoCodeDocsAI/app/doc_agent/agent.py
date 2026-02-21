from google.adk.agents import Agent

doc_agent = Agent(
    name="RepoArchitect",
    model="gemini-2.5-flash-lite",
    instruction="""
    You are an expert Technical Writer and Senior Developer.
    1. Analyze the provided source code within the <file> tags.
    2. Determine the project's purpose, installation steps, and core features.
    3. Generate a professional, high-quality README.md in Markdown format.
    4. Focus on clarity and developer experience.
    """
)

