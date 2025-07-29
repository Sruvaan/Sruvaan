# Sruvaan MCP Pipeline Setup Guide

This guide explains how to set up the Sruvaan MCP Pipeline with GitHub Secrets integration and YAML templates.

## Prerequisites

- Python 3.11 or higher
- GitHub account with repository access
- OpenAI API key (optional, for LLM functionality)
- Anthropic API key (optional, for LLM functionality)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Sruvaan.git
cd Sruvaan
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# LLM API Keys (required for LLM functionality)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# GitHub Secrets (optional, for GitHub Actions)
GITHUB_TOKEN=your_github_token_here
GITHUB_REPOSITORY=your_username/your_repo_name

# Additional Configuration (optional)
LOG_LEVEL=INFO
ENABLE_LLM_FALLBACK=true
```

### 5. Run Tests

```bash
python -m pytest tests/ -v
```

### 6. Run Demo

```bash
python demo.py
```

## GitHub Secrets Configuration

### Setting Up GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

#### Required Secrets

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key

#### Optional Secrets

- `GITHUB_TOKEN`: GitHub token (usually auto-provided)
- `GITHUB_REPOSITORY`: Repository name (usually auto-provided)

### Accessing Secrets in Code

The pipeline automatically loads secrets from environment variables:

```python
from src.config import config

# Get a secret
api_key = config.get_secret("openai_api_key")
```

## YAML Templates

### Template Structure

Templates are stored in the `templates/` directory as YAML files:

```yaml
# templates/prompter.yaml
system_prompt: "You are a semantic parser..."
user_prompt: |
  INSTRUCTIONS:
  1. Parse the user instruction...
  2. Extract all relevant entities...

  Parse the following instruction: {instruction}
model: "gpt-4"
temperature: 0.1
max_tokens: 500
```

### Available Templates

- `prompter.yaml`: For intent and entity extraction
- `cryptor.yaml`: For HKP encryption
- `mimicus.yaml`: For adversarial mimicry
- `probator.yaml`: For leakage analysis
- `praeceptor.yaml`: For parameter calibration

### Customizing Templates

1. Edit the YAML files in `templates/` directory
2. Templates support variable substitution using `{variable_name}`
3. Available parameters:
   - `system_prompt`: System-level instructions
   - `user_prompt`: User-level instructions with variables
   - `model`: LLM model name (gpt-4, claude-3, etc.)
   - `temperature`: Response randomness (0.0-1.0)
   - `max_tokens`: Maximum response length

## LLM Integration

### Supported Providers

- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude-3, Claude-2

### Fallback Mechanism

If LLM calls fail, the pipeline automatically falls back to rule-based processing:

```python
# Try LLM first
llm_response = llm_client.call_llm("prompter", instruction=instruction)

if llm_response:
    # Use LLM response
    result = parse_llm_response(llm_response)
else:
    # Fallback to rule-based processing
    result = rule_based_processing(instruction)
```

### Configuration Validation

The pipeline validates configuration on startup:

```python
from src.config import config

if config.validate_config():
    print("Configuration is valid")
else:
    print("Configuration validation failed")
```

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure your `.env` file contains valid API keys
2. **Template Loading**: Check that `templates/` directory exists and contains YAML files
3. **LLM Failures**: The pipeline will automatically fall back to rule-based processing
4. **Import Errors**: Ensure you're running from the project root directory

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python demo.py
```

### Testing Configuration

Test your configuration:

```bash
python -c "
import sys
sys.path.insert(0, 'src')
from config import config
print('Secrets loaded:', list(config.secrets.keys()))
print('Templates loaded:', list(config.templates.keys()))
"
```

## Security Notes

- Never commit API keys to version control
- Use GitHub Secrets for production deployments
- The pipeline includes fallback mechanisms for security
- All sensitive data is handled through environment variables

## Next Steps

1. Set up your API keys in GitHub Secrets
2. Customize YAML templates for your use case
3. Run the demo to test the pipeline
4. Extend the pipeline with additional agents as needed
