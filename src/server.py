"""
Seafile MCP Server
A Model Context Protocol server for Seafile file operations.

Author: Setu Kathawate
License: MIT
Repository: https://github.com/setugk/seafile-mcp
"""

import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

SEAFILE_URL = os.getenv("SEAFILE_URL", "").rstrip("/")
SEAFILE_TOKEN = os.getenv("SEAFILE_TOKEN", "")

# Create the MCP server
mcp = FastMCP("Seafile MCP")


def get_headers() -> dict:
    """Get authorization headers for Seafile API requests."""
    return {
        "Authorization": f"Token {SEAFILE_TOKEN}",
        "Accept": "application/json",
    }


@mcp.tool()
def hello() -> str:
    """A simple test tool to verify MCP is working."""
    return "Hello from MCP! Your server is working correctly."


@mcp.tool()
async def ping_server() -> str:
    """Test connection to the Seafile server and verify authentication."""
    if not SEAFILE_URL or not SEAFILE_TOKEN:
        return "Error: SEAFILE_URL or SEAFILE_TOKEN not configured in .env"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{SEAFILE_URL}/api2/auth/ping/",
                headers=get_headers(),
                timeout=10.0,
            )
            if response.status_code == 200:
                return f"Connected to {SEAFILE_URL} - Authentication successful!"
            else:
                return f"Error: Server returned status {response.status_code}: {response.text}"
        except httpx.ConnectError as e:
            return f"Connection error: Could not reach {SEAFILE_URL} - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool()
async def get_account_info() -> dict:
    """Get information about the authenticated Seafile account."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SEAFILE_URL}/api2/account/info/",
            headers=get_headers(),
            timeout=10.0,
        )
        if response.status_code == 200:
            return response.json()
        return {"error": f"Status {response.status_code}: {response.text}"}


@mcp.tool()
async def list_libraries() -> list:
    """List all libraries (repos) accessible to the authenticated user."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SEAFILE_URL}/api2/repos/",
            headers=get_headers(),
            timeout=10.0,
        )
        if response.status_code == 200:
            libraries = response.json()
            # Return simplified info for each library
            return [
                {
                    "id": lib.get("id"),
                    "name": lib.get("name"),
                    "size": lib.get("size"),
                    "owner": lib.get("owner"),
                    "encrypted": lib.get("encrypted"),
                }
                for lib in libraries
            ]
        return [{"error": f"Status {response.status_code}: {response.text}"}]


@mcp.tool()
async def get_library(library_id: str) -> dict:
    """Get details of a specific library by ID.

    Args:
        library_id: The ID of the library to retrieve
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SEAFILE_URL}/api2/repos/{library_id}/",
            headers=get_headers(),
            timeout=10.0,
        )
        if response.status_code == 200:
            return response.json()
        return {"error": f"Status {response.status_code}: {response.text}"}


@mcp.tool()
async def list_directory(library_id: str, path: str = "/") -> list:
    """List contents of a directory in a library.

    Args:
        library_id: The ID of the library
        path: Path within the library (default: root "/")
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SEAFILE_URL}/api2/repos/{library_id}/dir/",
            headers=get_headers(),
            params={"p": path},
            timeout=10.0,
        )
        if response.status_code == 200:
            items = response.json()
            return [
                {
                    "name": item.get("name"),
                    "type": item.get("type"),
                    "size": item.get("size") if item.get("type") == "file" else None,
                    "modified": item.get("mtime"),
                }
                for item in items
            ]
        return [{"error": f"Status {response.status_code}: {response.text}"}]


@mcp.tool()
async def create_library(name: str, description: str = "", password: str = "") -> dict:
    """Create a new library.

    Args:
        name: Name for the new library
        description: Optional description
        password: Optional password to encrypt the library
    """
    async with httpx.AsyncClient() as client:
        data = {"name": name}
        if description:
            data["desc"] = description
        if password:
            data["passwd"] = password

        response = await client.post(
            f"{SEAFILE_URL}/api2/repos/",
            headers=get_headers(),
            data=data,
            timeout=10.0,
        )
        if response.status_code in (200, 201):
            return response.json()
        return {"error": f"Status {response.status_code}: {response.text}"}


@mcp.tool()
async def delete_library(library_id: str) -> str:
    """Delete a library. WARNING: This permanently deletes all contents.

    Args:
        library_id: The ID of the library to delete
    """
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{SEAFILE_URL}/api2/repos/{library_id}/",
            headers=get_headers(),
            timeout=10.0,
        )
        if response.status_code in (200, 204):
            return f"Library {library_id} deleted successfully"
        return f"Error: Status {response.status_code}: {response.text}"


@mcp.tool()
async def create_directory(library_id: str, path: str) -> str:
    """Create a new directory in a library.

    Args:
        library_id: The ID of the library
        path: Full path of the directory to create (e.g., "/new-folder")
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SEAFILE_URL}/api2/repos/{library_id}/dir/",
            headers=get_headers(),
            params={"p": path},
            data={"operation": "mkdir"},
            timeout=10.0,
        )
        if response.status_code in (200, 201):
            return f"Directory '{path}' created successfully"
        return f"Error: Status {response.status_code}: {response.text}"


@mcp.tool()
async def delete_item(library_id: str, path: str) -> str:
    """Delete a file or directory from a library.

    Args:
        library_id: The ID of the library
        path: Path to the file or directory to delete
    """
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{SEAFILE_URL}/api2/repos/{library_id}/file/",
            headers=get_headers(),
            params={"p": path},
            timeout=10.0,
        )
        if response.status_code in (200, 204):
            return f"'{path}' deleted successfully"
        return f"Error: Status {response.status_code}: {response.text}"


@mcp.tool()
async def rename_item(library_id: str, path: str, new_name: str) -> str:
    """Rename a file or directory.

    Args:
        library_id: The ID of the library
        path: Current path to the file or directory
        new_name: New name for the item
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SEAFILE_URL}/api2/repos/{library_id}/file/",
            headers=get_headers(),
            params={"p": path},
            data={"operation": "rename", "newname": new_name},
            timeout=10.0,
        )
        if response.status_code == 200:
            return f"Renamed to '{new_name}' successfully"
        return f"Error: Status {response.status_code}: {response.text}"


@mcp.tool()
async def move_item(library_id: str, path: str, dst_library_id: str, dst_path: str) -> str:
    """Move a file or directory to a new location.

    Args:
        library_id: Source library ID
        path: Path to the file or directory to move
        dst_library_id: Destination library ID
        dst_path: Destination directory path
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SEAFILE_URL}/api2/repos/{library_id}/file/",
            headers=get_headers(),
            params={"p": path},
            data={
                "operation": "move",
                "dst_repo": dst_library_id,
                "dst_dir": dst_path,
            },
            timeout=10.0,
        )
        if response.status_code == 200:
            return f"Moved '{path}' to '{dst_path}' successfully"
        return f"Error: Status {response.status_code}: {response.text}"


@mcp.tool()
async def copy_item(library_id: str, path: str, dst_library_id: str, dst_path: str) -> str:
    """Copy a file or directory to a new location.

    Args:
        library_id: Source library ID
        path: Path to the file or directory to copy
        dst_library_id: Destination library ID
        dst_path: Destination directory path
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SEAFILE_URL}/api2/repos/{library_id}/file/",
            headers=get_headers(),
            params={"p": path},
            data={
                "operation": "copy",
                "dst_repo": dst_library_id,
                "dst_dir": dst_path,
            },
            timeout=10.0,
        )
        if response.status_code == 200:
            return f"Copied '{path}' to '{dst_path}' successfully"
        return f"Error: Status {response.status_code}: {response.text}"


@mcp.tool()
async def get_file_download_link(library_id: str, path: str) -> str:
    """Get a download link for a file.

    Args:
        library_id: The ID of the library
        path: Path to the file
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SEAFILE_URL}/api2/repos/{library_id}/file/",
            headers=get_headers(),
            params={"p": path},
            timeout=10.0,
        )
        if response.status_code == 200:
            return response.text.strip('"')
        return f"Error: Status {response.status_code}: {response.text}"


@mcp.tool()
async def get_file_content(library_id: str, path: str) -> str:
    """Get the content of a text file.

    Args:
        library_id: The ID of the library
        path: Path to the file
    """
    async with httpx.AsyncClient() as client:
        # First get the download link
        link_response = await client.get(
            f"{SEAFILE_URL}/api2/repos/{library_id}/file/",
            headers=get_headers(),
            params={"p": path},
            timeout=10.0,
        )
        if link_response.status_code != 200:
            return f"Error getting download link: {link_response.status_code}"

        download_url = link_response.text.strip('"')

        # Download the content
        content_response = await client.get(download_url, timeout=30.0)
        if content_response.status_code == 200:
            return content_response.text
        return f"Error downloading file: {content_response.status_code}"


@mcp.tool()
async def get_upload_link(library_id: str, path: str = "/") -> str:
    """Get an upload link for a directory. Use this to upload files.

    Args:
        library_id: The ID of the library
        path: Directory path where files will be uploaded (default: root)
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SEAFILE_URL}/api2/repos/{library_id}/upload-link/",
            headers=get_headers(),
            params={"p": path},
            timeout=10.0,
        )
        if response.status_code == 200:
            return response.text.strip('"')
        return f"Error: Status {response.status_code}: {response.text}"


@mcp.tool()
async def search_files(query: str, library_id: str = "") -> list:
    """Search for files across libraries.

    Args:
        query: Search query string
        library_id: Optional library ID to limit search scope
    """
    async with httpx.AsyncClient() as client:
        params = {"q": query}
        if library_id:
            params["repo_id"] = library_id

        response = await client.get(
            f"{SEAFILE_URL}/api2/search/",
            headers=get_headers(),
            params=params,
            timeout=30.0,
        )
        if response.status_code == 200:
            results = response.json().get("results", [])
            return [
                {
                    "name": item.get("name"),
                    "path": item.get("fullpath"),
                    "library_id": item.get("repo_id"),
                    "library_name": item.get("repo_name"),
                }
                for item in results
            ]
        return [{"error": f"Status {response.status_code}: {response.text}"}]


if __name__ == "__main__":
    mcp.run()
