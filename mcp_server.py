from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("messaging-agent")

@mcp.tool()
async def get_current_date() -> str:
    """
    Get the current date.
    Example: Friday September 20, 2025
    """
    return datetime.now().strftime("%A %B %d, %Y")

@mcp.tool()
async def get_current_time() -> str:
    """
    Get the current time.
    Example: 10:00 AM
    """
    return datetime.now().strftime("%I:%M %p")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")