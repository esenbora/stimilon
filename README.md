# Stimilon

**Penetration testing for LLM applications.**

Stimilon is an automated security testing platform that identifies vulnerabilities in LLM-powered applications. It simulates adversarial attacks—prompt injections, jailbreaks, and data extraction attempts—against any LLM API.

## Features

- **23 Attack Tests**: 10 prompt injections, 8 jailbreaks, 5 data extraction probes
- **Multi-Provider Support**: OpenAI and Anthropic APIs
- **Severity Scoring**: Critical, High, Medium, Low classifications
- **Remediation Guidance**: Specific fixes for each vulnerability
- **PDF Reports**: Export comprehensive security reports

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.9+
- pnpm

### Installation

```bash
# Clone and install dependencies
pnpm install

# Install Python dependencies
cd apps/api
pip install -r requirements.txt
cd ../..
```

### Development

Start both frontend and backend:

```bash
# Terminal 1: Start frontend
pnpm dev

# Terminal 2: Start backend
cd apps/api
uvicorn main:app --reload --port 8000
```

Open http://localhost:3000 in your browser.

## Project Structure

```
stimilon/
├── apps/
│   ├── web/                 # Next.js 16 frontend
│   │   ├── app/
│   │   │   ├── page.tsx           # Landing page
│   │   │   └── dashboard/         # Dashboard pages
│   │   └── components/ui/         # UI components
│   │
│   └── api/                 # FastAPI backend
│       ├── main.py
│       ├── routers/              # API endpoints
│       └── engine/
│           ├── attacks/          # Attack library
│           ├── connectors/       # LLM API connectors
│           └── executor.py       # Scan executor
│
├── packages/
│   └── ui/                  # Shared UI package
│
└── turbo.json
```

## Attack Library

### Prompt Injection (10 tests)
- Basic instruction override
- System prompt extraction
- Delimiter injection
- Context switching
- Markdown/code block escape
- Multi-language injection
- Unicode manipulation
- Payload in metadata
- Recursive injection
- XML tag injection

### Jailbreaks (8 tests)
- DAN (Do Anything Now)
- Roleplay exploits
- Hypothetical framing
- Academic pretense
- Base64 encoding bypass
- Leetspeak bypass
- Multi-turn escalation
- Emotional manipulation

### Data Extraction (5 tests)
- System prompt repetition
- First message probe
- Training data memorization
- PII extraction
- RAG content exposure

## Tech Stack

- **Frontend**: Next.js 16, TailwindCSS, TypeScript
- **Backend**: Python, FastAPI, httpx
- **Build**: Turborepo, pnpm

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/scans` | Create new security scan |
| GET | `/api/scans/{id}` | Get scan details |
| GET | `/api/scans` | List all scans |
| GET | `/api/reports/{scan_id}/pdf` | Download PDF report |

## License

MIT
