# Preferences

A collection of code examples, templates, and configuration patterns that serve as a reference for AI assistants working on my projects.

## Purpose

This repository helps AI assistants understand my preferred approaches to common development tasks by providing concrete examples of configurations, project structures, and patterns I use across different projects.

## Structure

Examples are organized by topic in separate folders (e.g., `templates/devcontainers/` for development container setups). Each folder may contain multiple alternative implementations - only one would typically be used in any given project.

## Using These Preferences in Your Projects

Access these preferences through the MCP (Model Context Protocol) server. This provides system-wide access to all your preferences without needing per-project configuration.

### Option 1: Local Installation (Claude Desktop)

For system-wide access on your local machine from Claude Desktop or other MCP-compatible AI assistants:

#### Installation

First, ensure you have `uv` installed:
```bash
# macOS
brew install uv

# Linux/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies and the MCP server:
```bash
# Clone this repository
git clone <repo-url> ~/preferences
cd ~/preferences

# Install dependencies
uv sync

# Install to Claude Desktop
fastmcp install claude-desktop mcp_server/server.py --project .
```

Alternatively, manually configure Claude Desktop by editing the config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "preferences": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/preferences",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "mcp_server/server.py"
      ],
      "env": {
        "REPO_PATH": "/absolute/path/to/preferences"
      }
    }
  }
}
```

After configuration, restart Claude Desktop completely.

#### Testing

Test the server locally:
```bash
# Run with stdio transport (default)
python -m mcp_server.server

# Run with HTTP transport for remote access
python -m mcp_server.server --transport http --port 8000
```

### Option 2: Docker Deployment (Remote Access)

For deploying the MCP server to a remote server (e.g., home server) with public access via Cloudflare Tunnel:

#### Prerequisites

- Docker and Docker Compose installed on your server
- A Cloudflare account with Zero Trust access
- A domain configured in Cloudflare (optional, but recommended)

#### Setup Cloudflare Tunnel

1. **Create the tunnel** in [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/):
   - Navigate to **Networks > Tunnels**
   - Click **Create a tunnel**
   - Choose **Cloudflared** as the connector type
   - Give it a name (e.g., "preferences-mcp")
   - Save the tunnel

2. **Download tunnel credentials**:
   - After creating the tunnel, you'll see a tunnel ID (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
   - Cloudflare provides a credentials JSON file - download it
   - Save it as `cloudflared/credentials.json` in this repository

3. **Update the tunnel configuration**:
   - Edit `cloudflared/config.yml`
   - Replace `YOUR_TUNNEL_ID` with your actual tunnel ID
   - The hostname `preferences.lunarlab.co.za` is already configured (change if needed)

4. **Configure public hostname** in Cloudflare dashboard:
   - In your tunnel settings, go to the **Public Hostname** tab
   - Click **Add a public hostname**:
     - **Subdomain**: `preferences` (or your preferred subdomain)
     - **Domain**: Select your domain
     - **Service Type**: HTTP
     - **URL**: `mcp-server:8000`
   - Save the configuration

#### Deploy the Server

```bash
# Clone the repository on your server
git clone <repo-url> ~/preferences
cd ~/preferences

# Ensure cloudflared/credentials.json and cloudflared/config.yml are configured
# (see Setup Cloudflare Tunnel section above)

# Build and start the services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

#### Connect from Claude Code

Once deployed, add the MCP server to Claude Code using the HTTP transport:

```bash
claude mcp add --transport http preferences https://mcp.yourdomain.com/mcp
```

Replace `https://mcp.yourdomain.com/mcp` with your actual Cloudflare Tunnel URL. The `/mcp` path is the MCP endpoint.

#### Management Commands

```bash
# Stop the services
docker-compose down

# Restart the services
docker-compose restart

# Update to latest code
git pull
docker-compose up -d --build

# View MCP server logs
docker-compose logs -f mcp-server

# View Cloudflare tunnel logs
docker-compose logs -f cloudflared
```

#### Available Resources

The MCP server exposes the following resources:

- `preferences://catalog` - List all available preferences
- `preferences://devcontainer/{name}/{file}` - Get devcontainer files (config, dockerfile, compose, caddyfile)
- `preferences://guide/{name}` - Get guides (claude, readme, style)
- `preferences://devcontainer/{name}/list` - List all files in a devcontainer
- `preferences://files/{filepath}` - Access any file in the repository

#### Available Tools

- `search_preferences(query, category)` - Search across preference files
- `list_devcontainer_files(name)` - List files in a specific devcontainer
- `compare_devcontainers(name1, name2)` - Compare two devcontainer configurations
- `list_all_preferences()` - Get organized list of all preferences

#### Available Prompts

The MCP server automatically provides context to AI assistants through prompts. These are **automatically available** without needing to be explicitly requested:

- `coding_style_guidelines` - Comprehensive coding style guidelines.

- `devcontainer_preferences` - Information about available devcontainer templates and when to use them

- `repository_guide` - General guidance on using this preferences repository

**Important**: These prompts provide automatic context to AI assistants. The coding style guidelines will be applied to all code without needing explicit reminders.

## Development

This repository uses `uv` for Python dependency management. The MCP server is implemented with [FastMCP](https://gofastmcp.com/).
