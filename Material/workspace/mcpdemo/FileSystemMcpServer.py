from mcp.server import MCPServer
from pathlib import Path
from typing import List

# Create an MCP server
mcp = MCPServer("FileSystemServer")

@mcp.tool()
def list_files(directory: str) -> List:
    """List all files in a directory"""
    try:
        return [f.absolute() for f in Path(directory).iterdir() if f.is_file()]
    
    except Exception as e:
        return [f"Error: {str(e)}"]

@mcp.tool()
def read_file(file_path: str) -> str:
    """Read contents of a file"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """Write content to a file"""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
            return f"File written successfully to  {f.name}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def create_directory(directory: str) -> str:
    """Create a new directory"""
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return "Directory created successfully"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def delete_file(file_path: str) -> str:
    """Delete a file"""
    try:
        Path(file_path).unlink()
        return "File deleted successfully"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__": 
    mcp.run()