# Seafile MCP Server

[![Author](https://img.shields.io/badge/author-Setu%20Kathawate-blue)](https://github.com/setugk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that connects Claude to your Seafile file storage. This lets you ask Claude to browse, search, read, and manage files on your self-hosted Seafile server using natural language.

---

## What is Seafile?

[Seafile](https://www.seafile.com/) is an open-source, self-hosted file sync and share platform - similar to Dropbox or Google Drive, but you control your own data. It's popular for personal use, teams, and enterprises who want privacy and control over their files.

**Why Seafile?**
- **Self-hosted**: Your files stay on your own server
- **Privacy-focused**: No third-party access to your data
- **Fast sync**: Efficient file synchronization across devices
- **Libraries**: Organize files into encrypted or unencrypted libraries
- **Cross-platform**: Apps for Windows, Mac, Linux, iOS, Android

**Don't have Seafile yet?** Here's how to get started:

| Option | Description | Link |
|--------|-------------|------|
| **Seafile Cloud** | Hosted by Seafile (easiest) | [cloud.seafile.com](https://cloud.seafile.com/) |
| **Docker Install** | Self-host with Docker (recommended) | [Docker Guide](https://manual.seafile.com/docker/deploy_seafile_with_docker/) |
| **Manual Install** | Self-host on Linux server | [Manual Guide](https://manual.seafile.com/deploy/) |
| **Synology NAS** | Run on Synology NAS | [Synology Package](https://www.seafile.com/en/download/) |
| **UGREEN NAS** | Run on UGREEN NAS via Docker | [Docker Guide](https://manual.seafile.com/docker/deploy_seafile_with_docker/) |
| **Raspberry Pi** | Self-host on a Pi | [Pi Guide](https://manual.seafile.com/deploy/deploy_with_raspberrypi/) |

### Why This MCP Server?

- **Direct connection** - Connects straight to your Seafile server, no middleman
- **Privacy-first** - Your data never leaves your infrastructure
- **Free & open source** - No subscriptions, no vendor lock-in
- **Full control** - Inspect, modify, and extend the code as needed
- **Self-hosted** - Runs locally alongside your self-hosted Seafile

---

## What Can You Do With This?

Once set up, you can ask Claude things like:

- "List all my libraries"
- "Show me what's in my Documents folder"
- "Read the contents of notes.txt"
- "Create a new folder called 'Projects'"
- "Move report.pdf to the Archive folder"
- "Search for files containing 'invoice'"

## Features

| Feature | Description |
|---------|-------------|
| **Browse Libraries** | List all libraries, view library details |
| **Navigate Folders** | List directory contents at any path |
| **Read Files** | Read text file contents directly |
| **File Operations** | Create, rename, move, copy, delete files and folders |
| **Download Links** | Generate download links for any file |
| **Upload Links** | Get upload links for directories |
| **Search** | Search for files across libraries (if enabled on your server) |

---

## Prerequisites

Before you start, make sure you have:

- **Python 3.10 or higher** - Check with `python3 --version`
- **A Seafile server** - Either self-hosted or a Seafile cloud account
- **Claude Desktop app** or **Claude Code CLI** - Where you'll use this MCP server

---

## Installation

### Step 1: Clone or Download This Repository

```bash
# Option A: Clone with git
git clone https://github.com/setugk/seafile-mcp.git
cd seafile-mcp

# Option B: Or download and extract the ZIP, then cd into it
```

### Step 2: Create a Virtual Environment

A virtual environment keeps this project's dependencies isolated from your system Python.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal prompt. This means the virtual environment is active.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `mcp` - The Model Context Protocol library
- `httpx` - For making HTTP requests to Seafile
- `python-dotenv` - For loading configuration from `.env`

### Step 4: Get Your Seafile API Token

You need an API token to authenticate with your Seafile server.

#### Option A: Using the Seafile Web Interface

1. Log into your Seafile web interface
2. Click your avatar/profile icon in the top right
3. Go to **Settings** → **Web API Auth Token**
4. Click **Generate Token** or copy your existing token

#### Option B: Using curl (Command Line)

```bash
curl -d "username=YOUR_EMAIL&password=YOUR_PASSWORD" \
     https://YOUR_SEAFILE_SERVER/api2/auth-token/
```

Replace:
- `YOUR_EMAIL` - Your Seafile login email
- `YOUR_PASSWORD` - Your Seafile password
- `YOUR_SEAFILE_SERVER` - Your Seafile server URL (e.g., `cloud.seafile.com`)

The response will look like:
```json
{"token": "a]1b2c3d4e5f6g7h8i9j0..."}
```

Copy the token value (without quotes).

### Step 5: Configure Your Credentials

```bash
# Copy the example config
cp .env.example .env

# Edit .env with your favorite editor
nano .env   # or vim, code, etc.
```

Fill in your values:

```
SEAFILE_URL=https://your-seafile-server.com
SEAFILE_TOKEN=your-api-token-here
```

**Important:**
- No trailing slash on the URL
- No quotes around values
- Keep this file secret (it's already in `.gitignore`)

### Step 6: Test the Server

```bash
python src/server.py
```

If everything is set up correctly, the server will start without errors. Press `Ctrl+C` to stop it.

---

## Connecting to Claude

Choose the method that matches how you use Claude:

### Option A: Claude Desktop App

1. **Find your Claude Desktop config file:**

   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

   Or in Claude Desktop: `Claude` menu → `Settings` → `Developer` → `Edit Config`

2. **Add the MCP server configuration:**

   If the file is empty or doesn't exist, create it with:

   ```json
   {
     "mcpServers": {
       "seafile": {
         "command": "/FULL/PATH/TO/seafile-mcp/venv/bin/python",
         "args": ["/FULL/PATH/TO/seafile-mcp/src/server.py"]
       }
     }
   }
   ```

   If you already have other MCP servers, add `seafile` inside the existing `mcpServers` object.

   **Important:** Replace `/FULL/PATH/TO/` with the actual absolute path to where you cloned this repo.

   Example paths:
   - macOS: `/Users/yourname/projects/seafile-mcp/venv/bin/python`
   - Windows: `C:\\Users\\yourname\\projects\\seafile-mcp\\venv\\Scripts\\python.exe`

3. **Restart Claude Desktop completely:**
   - Quit Claude Desktop (Cmd+Q on Mac, Alt+F4 on Windows)
   - Reopen Claude Desktop

4. **Verify it works:**
   - Start a new conversation
   - Look for the hammer/tools icon - "seafile" should be listed
   - Ask: "Use the hello tool" or "List my Seafile libraries"

### Option B: Claude Code (CLI)

1. **Create a `.mcp.json` file** in your project directory:

   ```json
   {
     "mcpServers": {
       "seafile": {
         "command": "/FULL/PATH/TO/seafile-mcp/venv/bin/python",
         "args": ["/FULL/PATH/TO/seafile-mcp/src/server.py"]
       }
     }
   }
   ```

2. **Start Claude Code** in that directory - it will automatically load the MCP server.

3. **Test with:** "List my Seafile libraries"

---

## Available Tools

Once connected, Claude has access to these tools:

| Tool | Description |
|------|-------------|
| `hello` | Test that the MCP server is working |
| `ping_server` | Test connection to your Seafile server |
| `get_account_info` | Get your Seafile account information |
| `list_libraries` | List all your libraries/repos |
| `get_library` | Get details of a specific library |
| `list_directory` | List contents of a folder |
| `create_library` | Create a new library |
| `delete_library` | Delete a library (permanent!) |
| `create_directory` | Create a new folder |
| `delete_item` | Delete a file or folder |
| `rename_item` | Rename a file or folder |
| `move_item` | Move a file or folder |
| `copy_item` | Copy a file or folder |
| `get_file_content` | Read a text file's contents |
| `get_file_download_link` | Get a download URL for a file |
| `get_upload_link` | Get an upload URL for a folder |
| `search_files` | Search for files (requires search enabled on server) |

---

## Troubleshooting

### "Server not appearing in Claude Desktop"

- Double-check the paths in your config are absolute paths (start with `/` on Mac/Linux or `C:\` on Windows)
- Make sure you fully restarted Claude Desktop (not just closed the window)
- Check for JSON syntax errors in your config file (missing commas, brackets)

### "SEAFILE_URL or SEAFILE_TOKEN not configured"

- Make sure you created the `.env` file (not just `.env.example`)
- Make sure the `.env` file is in the project root directory (same folder as `src/`)
- Check there are no extra spaces or quotes in your `.env` values

### "Connection error: Could not reach server"

- Verify your Seafile server URL is correct and accessible
- Try opening the URL in a browser
- Check if your server requires VPN access

### "Authentication failed" or "401 Unauthorized"

- Your API token may have expired - generate a new one
- Make sure you copied the full token with no extra spaces

### "Module not found" errors

- Make sure you're using the Python from the virtual environment in your config
- Run `venv/bin/pip list` to verify `mcp` and `httpx` are installed

### Check server logs

Run the server manually to see any errors:

```bash
source venv/bin/activate
python src/server.py
```

---

## Roadmap

Features planned for future releases:

| Feature | Status | Description |
|---------|--------|-------------|
| **PDF reading** | Planned | Extract text from PDF files so Claude can answer questions about receipts, contracts, etc. |
| **Image OCR** | Idea | Extract text from images using OCR |
| **File upload** | Idea | Upload files to Seafile via Claude |

Have a feature request? [Open an issue](https://github.com/setugk/seafile-mcp/issues)!

---

## Security

> **Important:** Please read [SECURITY.md](SECURITY.md) for full security considerations.

**Key points:**

- **Never commit your `.env` file** - It contains your API token
- **API tokens grant full access** to your Seafile account - treat them like passwords
- **Review the code** before running - inspect `src/server.py` to understand what it does
- **Secure file permissions** - Run `chmod 600 .env` to restrict access to your credentials
- **Consider token scope** - Some Seafile deployments support scoped tokens with limited permissions

**Reporting vulnerabilities:** See [SECURITY.md](SECURITY.md) for responsible disclosure guidelines.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## License

MIT License - See LICENSE file for details.

---

## Author

**Setu Kathawate**

- GitHub: [@setugk](https://github.com/setugk)

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) for easy MCP server development
- Uses the [Seafile Web API](https://download.seafile.com/published/web-api/home.md)
