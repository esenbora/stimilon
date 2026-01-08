# Stimilon

<p align="center">
  <img src="https://img.shields.io/pypi/v/stimilon?color=blue&label=PyPI" alt="PyPI">
  <img src="https://img.shields.io/pypi/pyversions/stimilon" alt="Python">
  <img src="https://img.shields.io/github/license/stimilon/stimilon" alt="License">
</p>

<p align="center">
  <b>LLM Security Scanner</b><br>
  Find prompt injection, jailbreak, and data extraction vulnerabilities in your AI applications.
</p>

---

## Quick Start

```bash
# Install
pip install stimilon

# Scan your endpoint
stimilon scan https://your-chatbot.com/api
```

## Features

- **73 Security Tests** - Comprehensive coverage of LLM vulnerabilities
- **Multiple Formats** - Supports OpenAI, Anthropic, and custom API formats
- **Fast & Parallel** - Async execution with configurable rate limiting
- **CI/CD Ready** - JSON output and exit codes for automation
- **Beautiful CLI** - Rich terminal output with progress tracking

## Installation

```bash
pip install stimilon
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv pip install stimilon
```

## Usage

### Basic Scan

```bash
# Scan a custom chatbot endpoint
stimilon scan https://api.yourcompany.com/chat
```

### With Authentication

```bash
# With API key
stimilon scan https://api.yourcompany.com/chat --api-key "your-token"

# OpenAI-compatible endpoint
stimilon scan https://api.openai.com/v1/chat/completions \
  --api-key "sk-xxx" \
  --format openai
```

### Specific Categories

```bash
# Only run injection tests
stimilon scan https://your-endpoint.com -c injection

# Multiple categories
stimilon scan https://your-endpoint.com -c injection,jailbreak
```

### Output Options

```bash
# Save results to JSON
stimilon scan https://your-endpoint.com -o results.json

# Quiet mode (for CI/CD)
stimilon scan https://your-endpoint.com -q
```

### List Available Tests

```bash
# Show all tests
stimilon list-attacks

# Filter by category
stimilon list-attacks -c jailbreak
```

## Security Tests

| Category | Count | Description |
|----------|-------|-------------|
| **Injection** | 10 | Prompt injection attacks |
| **Jailbreak** | 8 | Restriction bypass techniques |
| **Extraction** | 5 | Data and prompt extraction |
| **Multilingual** | 10 | Non-English & mixed language attacks |
| **Advanced** | 10 | Agent, RAG, and emerging threats |
| **Languages** | 10 | Extended language attacks (Russian, Chinese, Hindi, Japanese, etc.) |
| **Social Engineering** | 10 | Authority impersonation, urgency, flattery, guilt tripping |
| **Encoding** | 10 | Base64, Hex, ROT13, Morse, Unicode obfuscation |

### Injection Tests

- `INJ-001` Basic Instruction Override
- `INJ-002` System Prompt Extraction
- `INJ-003` Delimiter Injection
- `INJ-004` Context Switching
- `INJ-005` Markdown/Code Block Escape
- `INJ-006` Multi-Language Injection
- `INJ-007` Unicode Manipulation
- `INJ-008` Payload in User Metadata
- `INJ-009` Recursive Instruction Injection
- `INJ-010` XML/HTML Tag Injection

### Jailbreak Tests

- `JB-001` DAN (Do Anything Now)
- `JB-002` Roleplay Character Exploit
- `JB-003` Hypothetical Scenario Framing
- `JB-004` Academic Research Pretense
- `JB-005` Base64 Encoding Bypass
- `JB-006` Leetspeak Character Substitution
- `JB-007` Multi-Turn Escalation
- `JB-008` Emotional Manipulation

### Extraction Tests

- `EXT-001` Direct Instruction Repetition
- `EXT-002` First Message Probe
- `EXT-003` Training Data Memorization
- `EXT-004` PII Extraction Attempt
- `EXT-005` RAG Content Exposure

### Multilingual Tests (Unique!)

- `ML-001` Turkish Prompt Injection
- `ML-002` Arabic Prompt Injection
- `ML-003` Mixed Language Confusion
- `ML-004` Cyrillic Homoglyph Attack
- `ML-005` RTL Override Attack
- `ML-006` Cultural Context Exploit
- `ML-007` Formality Level Manipulation
- `ML-008` Translation Request Trick
- `ML-009` Emoji Obfuscation
- `ML-010` Pig Latin / Word Games

### Advanced Tests (Unique!)

- `ADV-001` Agent Tool Abuse
- `ADV-002` RAG Context Poisoning
- `ADV-003` Chain-of-Thought Manipulation
- `ADV-004` Function Calling Injection
- `ADV-005` System Prompt Reconstruction
- `ADV-006` Token Smuggling
- `ADV-007` Context Window Exhaustion
- `ADV-008` Virtualization/Simulation Attack
- `ADV-009` Output Format Exploit
- `ADV-010` Time-Based Context Attack

### Extended Language Tests (Unique!)

- `LANG-001` Russian (Cyrillic) Injection
- `LANG-002` Chinese (Simplified) Injection
- `LANG-003` Hindi (Devanagari) Injection
- `LANG-004` Japanese (Kanji/Hiragana/Katakana) Injection
- `LANG-005` Korean (Hangul) Injection
- `LANG-006` Portuguese Injection
- `LANG-007` French Injection
- `LANG-008` German Injection
- `LANG-009` Spanish Injection
- `LANG-010` Thai Injection

### Social Engineering Tests (Unique!)

- `SOC-001` Authority Impersonation
- `SOC-002` Urgency/Emergency Exploit
- `SOC-003` Flattery Manipulation
- `SOC-004` Reciprocation Exploit
- `SOC-005` Social Consensus Manipulation
- `SOC-006` Scarcity Pressure
- `SOC-007` Guilt Tripping
- `SOC-008` Gaslighting Attack
- `SOC-009` Peer Pressure
- `SOC-010` Love Bombing

### Encoding/Obfuscation Tests (Unique!)

- `ENC-001` Base64 Encoded Injection
- `ENC-002` Hexadecimal Encoding
- `ENC-003` ROT13 Cipher Bypass
- `ENC-004` Morse Code Injection
- `ENC-005` Binary Encoding
- `ENC-006` Acronym Hiding (Acrostic)
- `ENC-007` Unicode Normalization Attack
- `ENC-008` Invisible Character Injection
- `ENC-009` Confusable/Lookalike Characters
- `ENC-010` Split Instruction Reassembly

## Request Formats

### Simple (Default)

```json
{"message": "your prompt here"}
```

### OpenAI

```json
{
  "model": "gpt-4o-mini",
  "messages": [{"role": "user", "content": "your prompt here"}]
}
```

### Anthropic

```json
{
  "model": "claude-3-haiku-20240307",
  "messages": [{"role": "user", "content": "your prompt here"}]
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: LLM Security Scan

on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Stimilon
        run: pip install stimilon

      - name: Run Security Scan
        run: stimilon scan ${{ secrets.LLM_ENDPOINT }} -k ${{ secrets.LLM_API_KEY }} -q -o results.json

      - name: Upload Results
        uses: actions/upload-artifact@v4
        with:
          name: security-results
          path: results.json
```

### Exit Codes

- `0` - All tests passed
- `1` - Vulnerabilities found

## API Usage

```python
import asyncio
from stimilon import Scanner, ScanConfig

config = ScanConfig(
    endpoint="https://your-chatbot.com/api",
    api_key="your-token",
    categories=["injection", "jailbreak"],
)

scanner = Scanner(config)
result = asyncio.run(scanner.run())

print(f"Score: {result.score}/100")
print(f"Vulnerabilities: {result.failed}")
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Adding New Attacks

```python
from stimilon.engine.attacks.base import Attack, AttackResult

class MyCustomAttack(Attack):
    name = "CUSTOM-001: My Attack"
    description = "Description of what this attack does"
    category = "injection"
    severity = "high"
    remediation = "How to fix this vulnerability"

    @property
    def prompt(self) -> str:
        return "Your attack prompt here"

    def analyze_response(self, response: str) -> AttackResult:
        success = "indicator" in response.lower()
        return AttackResult(
            success=success,
            response=response,
            severity=self.severity,
            confidence=0.9 if success else 0.1,
            details="Attack result details",
        )
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Promptfoo Integration

Use Stimilon attacks in your Promptfoo red teaming setup:

```yaml
# promptfooconfig.yaml
redteam:
  plugins:
    - file://./stimilon/promptfoo-plugins/turkish-injection.yaml
    - file://./stimilon/promptfoo-plugins/agent-tool-abuse.yaml
    - file://./stimilon/promptfoo-plugins/rag-poisoning.yaml
```

See [promptfoo-plugins/README.md](promptfoo-plugins/README.md) for full documentation.

## Links

- [GitHub](https://github.com/esenbora/stimilon)
- [Promptfoo Plugins](https://github.com/esenbora/stimilon/tree/main/promptfoo-plugins)

---

<p align="center">
  Made with ❤️ by the Stimilon team
</p>
