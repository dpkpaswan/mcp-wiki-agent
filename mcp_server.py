from mcp.server.fastmcp import FastMCP
import wikipediaapi

mcp = FastMCP("wikipedia-server")

@mcp.tool()
def search_wikipedia(topic: str) -> str:
    """Search Wikipedia for information about a topic."""
    wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='mcp-wiki-agent/1.0'
    )
    page = wiki.page(topic)
    if not page.exists():
        return f"No Wikipedia article found for '{topic}'"
    
    summary = page.summary[:1000]
    return f"Wikipedia article on '{topic}':\n\n{summary}"

if __name__ == "__main__":
    mcp.run(transport="stdio")