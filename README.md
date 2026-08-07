# mcp-youtube-transcript

An MCP server that takes a YouTube video URL and returns the transcript text to
your agent.

## Tools

- `list_transcript_languages(url)` — which subtitle tracks the video has
- `get_transcript(url, language)` — the transcript text in the given language

`language` is required. If the requested language is unavailable, English is used
as a fallback; if neither exists, the tool returns the list of languages the video
does have so the agent can retry.

URLs are accepted in every common form: `watch?v=`, `youtu.be/`, `/shorts/`,
`/embed/`, `/live/`, or a bare 11-character video ID.

## Installation

No Python needed. The only requirement is [uv](https://docs.astral.sh/uv/) — a
single binary that installs without administrator rights and downloads a suitable
Python for you.

**Windows (PowerShell):**

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then add the server to **Claude Code** with a single command:

```
claude mcp add youtube-transcript -- uvx --from git+https://github.com/gridivit/mcp-youtube-transcript mcp-youtube-transcript
```

For **Claude Desktop**, add this to `claude_desktop_config.json`
(`%APPDATA%\Claude\` on Windows, `~/Library/Application Support/Claude/` on macOS):

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/gridivit/mcp-youtube-transcript",
        "mcp-youtube-transcript"
      ]
    }
  }
}
```

For **Antigravity**, use the same JSON in `~/.gemini/config/mcp_config.json`
(global) or `.agents/mcp_config.json` (per project).

The first launch takes about a minute while uv downloads Python and the
dependencies. Every launch after that is instant.

### Windows notes

- Escape backslashes in JSON paths: `C:\\Users\\...`, or just use forward slashes.
  A single backslash silently breaks config parsing.
- If the client cannot find `uv`, restart the application completely so it picks
  up the updated `PATH`. If that does not help, use the full path to the binary:
  `C:\\Users\\<name>\\.local\\bin\\uvx.exe`.

## Updating

`uvx` caches the cloned repository and will not pick up new commits on its own.
To pull the latest version:

```
uvx --refresh --from git+https://github.com/gridivit/mcp-youtube-transcript mcp-youtube-transcript
```

## Development

Do not install your own checkout through `uvx` — it pulls the code from git, so
you would not see local changes. Point the client at the working copy instead:

```
claude mcp add youtube-transcript-dev -- uv --directory <path-to-clone> run mcp-youtube-transcript
```

Run the test client to inspect the protocol directly:

```
npx @modelcontextprotocol/inspector uv run mcp-youtube-transcript
```
