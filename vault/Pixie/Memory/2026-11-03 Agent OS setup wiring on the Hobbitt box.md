---
title: Agent OS setup wiring on the Hobbitt box
kind: project
source: Claude Memory/Agent OS setup (Claude)/Agent os setup wiring.md
created: 2026-11-03
reviewed: true
---
- Agent OS dashboard runs as systemd `agent-os.service` on port 3737 and reads keys from `~/.config/agent-os/environment`; restart it by killing the `next-server` process (systemd brings it back in about 10s).
- Hermes 0.22.5 lives at `~/.hermes/hermes-agent`, with keys in `~/.hermes/.env` and model config in `~/.hermes/config.yaml`; the user has chosen free models only (no OpenRouter credit).
- Local builder model (`ollama/qwen2.5-coder:7b`) is served from the Windows PC RydenStudio over Tailscale through an nginx relay on 127.0.0.1:11434. If the relay returns 502 after `sudo agent-model` is re-run, the `proxy_ssl_verify_depth 3;` line was wiped and must be re-added with sudo.
- Phone agent chain: Twilio → ElevenLabs agent → cloudflared tunnel (`agentos-tunnel.service`) → Hermes API on 127.0.0.1:8642. The tunnel's URL is relinked automatically to the dashboard on each start.
- Apollo persona is "Pixie" (default voice Juniper, with Sasha as an ElevenLabs option); Codex CLI uses file-based auth because the dashboard cannot read the desktop keyring.
- Pixie caller (`pixie-caller.service`) phones the user at 08:30 and when plans await approval, with Telegram as fallback. Calls to the user's number fail with Twilio error 21216 and need a Twilio Support ticket.
- Claude-to-vault sync (`claude-vault-sync.py`) writes Claude project memories into `Pixie/Claude Memory/<project>/`; this project's Agent OS id is 7689fb44-8cc2-4f2d-a376-218ec1c47e28.

Learned from [[Claude Memory/Agent OS setup (Claude)/Agent os setup wiring]].
