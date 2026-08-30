# Install Studio V2 in ChatGPT

Studio's default ChatGPT distribution is one skills-first archive:

```text
dist/chatgpt/studio.zip
```

Build it with `python scripts/build_studio.py`. The archive contains the
portable Skills and OpenAI Skill metadata only. It does not declare an MCP
server, require localhost, a tunnel, an API key, or a connected app. Satellite
archives are diagnostic/optional outputs; the default install is the umbrella
archive.

## Supported account route

1. Use Browser use with the owner's existing browser profile.
2. Identify the visible ChatGPT account and workspace before changing anything.
3. Prefer **Workspace settings → Plugins → Add → Import marketplace** when the
   account exposes that route and the GitHub marketplace revision is available.
4. Otherwise use **Plugins → Skills → Create → Upload** and upload
   `dist/chatgpt/studio.zip`.
5. Wait for scanning, inspect any review/block reason, and verify the actual
   invocation surface in a new chat.

Never enter or request a password, MFA/recovery code, cookie, OAuth token, or
API key. OAuth/account selection, permission changes, external writes, and any
custom-instruction change are human gates. Do not claim `@Studio` works unless
the mention is visibly observed; if the personal Skills route exposes only an
explicit Skill invocation, record that exact invocation instead.

## Fresh-chat proof

Use a completely new chat and ask Studio to identify the canonical repository
and Drive workspace, perform read-only probes, and return a project brief with
goals, non-goals, assumptions, requirements, proof levels, and one next action.
Record the visible account, installed version, invocation surface, and result
in `bootstrap/CHATGPT_INSTALL_RECEIPT.md`. Mark iPhone/mobile availability
`USER CHECK` until personally verified.
