# Shiranui
Shiranui is [the Model Context Protocol](https://modelcontextprotocol.io/introduction)(MCP) Server for retreiving the clinical standard contents in [the CDISC Library](https://library.cdisc.org/browser/#/).  
This MCP server is built with [Python FastMCP](https://github.com/jlowin/fastmcp).

https://github.com/user-attachments/assets/9cd7e1a6-2750-4910-bb03-763c323b9f22

## Support CDISC Library API
- v2 Biomedical Concept Endpoints
- v2 Dataset Specialization Endpoints
- Controlled Terminology Codelist Endpoints
- ADaM Variable Metadata Endpoints
- SDTM Metadata Endpoints (Dataset and Variable Metadata)

## Requirements
- Python v3.13 and [UV](https://docs.astral.sh/uv/getting-started/installation/) were installed on your device.
- You have the [CDISC Library API Key](https://api.developer.library.cdisc.org/signin?returnUrl=%2Fapi-details).
  
## Installation
Download Shiranui from the [Releases Page](https://github.com/i-akiya/Shiranui/releases).
### Mac and Linux
```bash
cd /your/shiranui/dir
uv venv -p 3.13
source .venv/bin/activate
uv sync
```
Set your API key as an environment variable named CDISC_LIBRARY_API_KEY.   
### Windows
```

```
Set your API key as an environment variable named CDISC_LIBRARY_API_KEY.   
  
## Configure mcp client
### LM Studio
```
{
  "mcpServers": {
    "Shiranui": {
      "command": "uv",
      "args": [
        "run",
        "/full/path/to/shiranui/dir/.venv/bin/shiranui"
      ]
    }
  }
}
```
You need to replace "/full/path/to/shiranui/dir" to match your own environment.  
In addition to LM Studio, it may also work with Claude Desktop, Codename Goose, and other MCP Clients.

  
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
