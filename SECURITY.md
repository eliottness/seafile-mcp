# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities
2. Email the maintainer directly (or open a private security advisory on GitHub)
3. Include a detailed description of the vulnerability and steps to reproduce

We will respond within 48 hours and work with you to understand and address the issue.

## Security Considerations

### API Token Security

This MCP server requires a Seafile API token for authentication. Please be aware:

- **API tokens grant full access** to your Seafile account
- **Never commit your `.env` file** - it contains your API token
- **Never share your API token** in logs, screenshots, or public forums
- **Rotate tokens periodically** - generate new tokens and revoke old ones
- **Use scoped tokens** if your Seafile server supports them (limits access to specific libraries)

### Local Execution Risks

This MCP server runs locally on your machine. Be aware that:

- The server has access to whatever the Seafile API token allows
- MCP clients (like Claude Desktop) can invoke any tool exposed by this server
- Review tool descriptions to understand what operations are possible

### Network Security

- All communication with your Seafile server uses HTTPS
- The server does not expose any network ports (uses stdio transport)
- Credentials are loaded from environment variables, not passed via command line

### Best Practices

1. **Minimal permissions**: If your Seafile server supports library-specific tokens, use them
2. **Secure your `.env` file**: Ensure it has restrictive file permissions (`chmod 600 .env`)
3. **Review before running**: Inspect the `src/server.py` code before running
4. **Keep updated**: Pull updates to get security fixes
5. **Monitor access**: Check your Seafile server's access logs periodically

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |

## Dependencies

This project depends on:
- `mcp` - Model Context Protocol library
- `httpx` - HTTP client
- `python-dotenv` - Environment variable loading

Keep dependencies updated to receive security patches:

```bash
pip install --upgrade -r requirements.txt
```
