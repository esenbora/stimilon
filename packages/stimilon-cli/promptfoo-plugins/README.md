# Stimilon Plugins for Promptfoo

Use Stimilon's unique security tests directly in your [Promptfoo](https://promptfoo.dev) red teaming setup.

## Installation

```bash
# Clone the plugins
git clone https://github.com/esenbora/stimilon.git
cd stimilon/promptfoo-plugins
```

## Available Plugins

| Plugin | Description | Unique? |
|--------|-------------|---------|
| `turkish-injection.yaml` | Turkish language prompt injection | ✅ |
| `multilingual-confusion.yaml` | Mixed language attacks | ✅ |
| `agent-tool-abuse.yaml` | AI agent tool exploitation | ✅ |
| `rag-poisoning.yaml` | RAG context injection | ✅ |
| `cot-manipulation.yaml` | Chain-of-thought exploitation | ✅ |

## Usage

### Option 1: Reference individual plugins

```yaml
# promptfooconfig.yaml
redteam:
  plugins:
    - file://./stimilon/promptfoo-plugins/turkish-injection.yaml
    - file://./stimilon/promptfoo-plugins/agent-tool-abuse.yaml
```

### Option 2: Use all Stimilon plugins

```yaml
# promptfooconfig.yaml
redteam:
  plugins:
    - file://./stimilon/promptfoo-plugins/turkish-injection.yaml
    - file://./stimilon/promptfoo-plugins/multilingual-confusion.yaml
    - file://./stimilon/promptfoo-plugins/agent-tool-abuse.yaml
    - file://./stimilon/promptfoo-plugins/rag-poisoning.yaml
    - file://./stimilon/promptfoo-plugins/cot-manipulation.yaml
```

### Option 3: Combine with built-in plugins

```yaml
# promptfooconfig.yaml
redteam:
  plugins:
    # Built-in promptfoo plugins
    - harmful
    - pii
    - jailbreak

    # Stimilon unique plugins
    - file://./stimilon/promptfoo-plugins/turkish-injection.yaml
    - file://./stimilon/promptfoo-plugins/agent-tool-abuse.yaml
```

## Example Configuration

```yaml
# promptfooconfig.yaml
description: 'Security scan with Stimilon plugins'

providers:
  - openai:gpt-4o-mini

prompts:
  - 'You are a helpful assistant. User: {{prompt}}'

redteam:
  numTests: 5
  plugins:
    # Stimilon multilingual attacks
    - file://./promptfoo-plugins/turkish-injection.yaml
    - file://./promptfoo-plugins/multilingual-confusion.yaml

    # Stimilon advanced attacks
    - file://./promptfoo-plugins/agent-tool-abuse.yaml
    - file://./promptfoo-plugins/rag-poisoning.yaml
    - file://./promptfoo-plugins/cot-manipulation.yaml
```

## Running

```bash
npx promptfoo eval
npx promptfoo view
```

## Why Stimilon Plugins?

These plugins test vulnerabilities that **aren't covered** by Promptfoo's built-in tests:

1. **Non-English attacks** - Most tools focus on English
2. **Agent-specific threats** - Tool abuse, function injection
3. **RAG vulnerabilities** - Context poisoning, document injection
4. **Advanced manipulation** - CoT exploitation, reasoning attacks

## Links

- [Stimilon CLI](https://github.com/esenbora/stimilon)
- [Promptfoo Docs](https://promptfoo.dev/docs/red-team/)
- [Report Issues](https://github.com/esenbora/stimilon/issues)
