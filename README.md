---
title: Email Triage OpenEnv
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# 📧 Email Triage OpenEnv

OpenEnv-compliant environment for email triage and prioritization tasks.

## Environment Description

The Email Triage Environment simulates real-world email management scenarios where agents must:
- Classify emails by urgency (low/medium/high)
- Draft appropriate responses
- Prioritize emails for optimal workflow

## API Endpoints

- `POST /reset` - Reset environment with task configuration
- `POST /` - Step through environment with actions
- `GET /state` - Get current environment state
- `GET /health` - Health check endpoint
- `WS /ws` - WebSocket interface for interactive sessions

## Tasks

- **Easy**: Classify 5 emails correctly
- **Medium**: Classify 6 emails and draft responses
- **Hard**: Full triage with 10 emails, responses, and priority ordering

## Team Dragon

- Mallarapu Arun Chand - arunchandmallarapu@gmail.com
- T. Someswararao - someshtellakula@gmail.com
