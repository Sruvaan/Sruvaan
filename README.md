# Sruvaan MCP Pipeline

A modular, Python-centric implementation of the 6-agent MCP (Model Context Protocol) cipher calibration pipeline with Hierarchical Keyed Protocol (HKP) integration.

## 🏗️ Architecture Overview

The Sruvaan MCP pipeline implements a 6-agent architecture for secure, role-based encryption with adversarial testing and parameter calibration:

```
Raw Instruction → Prompter → Cryptor(HKP) → Decryptor → Mimicus → Probator → Praeceptor
                                                                    ↓
                                                              Feedback Loop
```

### Agent Roles

1. **Prompter**: Parses raw user instructions into structured semantic fields
2. **Cryptor**: Applies Hierarchical Keyed Protocol (HKP) encryption with role-scoped keys
3. **Decryptor**: Reverses HKP encryption using role-based keys and validates PoP signatures
4. **Mimicus**: Simulates adversarial mimicry to probe for leakage vulnerabilities
5. **Probator**: Assesses semantic leakage and decipherability of encrypted messages
6. **Praeceptor**: Calibrates encryption parameters based on leakage assessment

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip
- OpenAI API key (optional, for LLM integration)
- Anthropic API key (optional, for LLM integration)

### Quick Reference

| Command                                                                                                         | Purpose                         | Notes                        |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------- | ---------------------------- |
| `python demo.py`                                                                                                | Run basic pipeline demo         | Uses fallback if no API keys |
| `python demo.py --llm-only`                                                                                     | Force LLM-only mode             | No fallbacks allowed         |
| `python demo.py --openai-only`                                                                                  | Use only OpenAI API             | Converts Claude to GPT-4     |
| `python github_secrets_demo.py`                                                                                 | Test GitHub Secrets integration | Shows setup guide            |
| `python -m pytest tests/ -v`                                                                                    | Run all tests                   | 23 tests total               |
| `python -m pytest tests/test_prompter.py -v`                                                                    | Test specific agent             | Unit tests                   |
| `python -c "import sys; sys.path.insert(0, 'src'); from config import config; print(config.validate_config())"` | Validate configuration          | Check setup                  |
| `ls templates/`                                                                                                 | List YAML templates             | 5 agent templates            |
| `cat templates/prompter.yaml`                                                                                   | View template content           | Customize prompts            |

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Sruvaan

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

#### Option 1: Environment Variables (Recommended)

```bash
# Set up environment variables for LLM integration
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# For GitHub Secrets integration
export GITHUB_TOKEN="your_github_token"
export GITHUB_REPOSITORY="your-username/your-repo"
```

#### Option 2: .env File

```bash
# Create a .env file in the project root
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GITHUB_TOKEN=your_github_token
GITHUB_REPOSITORY=your-username/your-repo
EOF
```

### Running the Pipeline

#### Basic Demo

```bash
# Run the complete pipeline demo (uses fallback if no API keys)
python demo.py
```

#### GitHub Secrets Demo

```bash
# Run the GitHub Secrets integration demo
python github_secrets_demo.py
```

#### Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_prompter.py -v

# Run with coverage
python -m pytest --cov=src tests/

# Type checking
mypy src/
```

#### Configuration Validation

```bash
# Validate configuration and templates
python -c "
import sys
sys.path.insert(0, 'src')
from config import config
print('Configuration valid:', config.validate_config())
print('Templates loaded:', list(config.templates.keys()))
"
```

## 📋 Features

### Hierarchical Keyed Protocol (HKP)

- **Role-scoped keys**: Each field encrypted with role-specific keys
- **Time-based constraints**: Epoch-based access control with `Time=∆τ`
- **Proof-of-Protocol**: PoP signatures for integrity verification
- **Field-wise encryption**: Hierarchical key derivation per field

### Adversarial Testing

- **Mimicry simulation**: Mimicus agent generates spoof outputs
- **Leakage assessment**: Probator quantifies semantic leakage
- **Parameter calibration**: Praeceptor optimizes encryption parameters
- **Feedback loops**: Continuous improvement of security vs. usability

### Modular Design

- **Stateless agents**: Each agent is a pure function
- **Strong data contracts**: Pydantic schemas for all I/O
- **Testable components**: Unit and integration tests
- **Extensible architecture**: Easy to add new agents or protocol phases

### LLM Integration with GitHub Secrets

- **Secure API key management**: Uses GitHub Secrets for production deployments
- **YAML templates**: Externalized prompt templates for each agent
- **Fallback mechanisms**: Automatic fallback to rule-based processing if LLM fails
- **Multi-provider support**: OpenAI and Anthropic API integration

## 🔧 Usage Examples

### Basic Pipeline Execution

```python
from src.schemas import RawInstructionInput
from src.main_pipeline import run_pipeline_demo

# Run complete pipeline
result = run_pipeline_demo()
print(f"Final Theta Update: {result.dict()}")
```

### Feedback Loop Demo

```python
from src.main_pipeline import run_pipeline_with_feedback

# Run pipeline with parameter calibration
```

### GitHub Secrets Configuration

For production deployments, configure GitHub Secrets:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ANTHROPIC_API_KEY`: Your Anthropic API key

The pipeline automatically loads these secrets in GitHub Actions workflows.

### YAML Templates

LLM prompts are managed as YAML templates in the `templates/` directory:

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

Available templates:

- `prompter.yaml`: Intent and entity extraction
- `cryptor.yaml`: HKP encryption
- `mimicus.yaml`: Adversarial mimicry
- `probator.yaml`: Leakage analysis
- `praeceptor.yaml`: Parameter calibration
  result = run_pipeline_with_feedback()
  print(f"Calibrated Parameters: {result.theta_update}")

````

### Individual Agent Usage

```python
from src.schemas import RawInstructionInput
from src.prompter import run_prompter
from src.cryptor import run_cryptor

# Use individual agents
raw_input = RawInstructionInput(
    instruction="Transfer $75,000 to account 7395-8845-2291",
    language="EN"
)

# Prompter
semantic_output = run_prompter(raw_input)
print(f"Parsed intent: {semantic_output.intent}")

# Cryptor with HKP
encrypted_output = run_cryptor(semantic_output)
print(f"Encrypted with role: {encrypted_output.role_tag}")
````

## 📊 Data Flow

### Sample Data Mutation

| Agent          | Input                   | Output                                                 |
| -------------- | ----------------------- | ------------------------------------------------------ |
| **Prompter**   | `"Transfer $75,000..."` | `{intent: "transfer", entities: {...}}`                |
| **Cryptor**    | `SemanticPromptOut`     | `{Ωα: "DYNX_Ω47", Role=Γ5: "HKP-derived", ...}`        |
| **Decryptor**  | `EncryptedOutput`       | `{intent: "transfer", entities: {...}}`                |
| **Mimicus**    | `DecryptedFieldsOut`    | `{mimic_fields: {...}, spoof_status: "mimic_attempt"}` |
| **Probator**   | `MimicOutput`           | `{leakage_score: 0.32, hk_protection: "active"}`       |
| **Praeceptor** | `LeakageVectorOut`      | `{theta_update: {...}, mode: "recalibrate"}`           |

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_prompter.py

# Run with coverage
pytest --cov=src tests/

# Run integration tests
pytest tests/test_pipeline_integration.py
```

### Test Structure

- **Unit tests**: Individual agent functionality
- **Integration tests**: Complete pipeline flow
- **HKP tests**: Hierarchical Keyed Protocol validation
- **Feedback loop tests**: Parameter calibration

## 🔒 Security Features

### HKP Protection

- **Role-based access**: Γ5 role tag for high-privilege operations
- **Time constraints**: Epoch-based key expiration
- **PoP signatures**: Integrity verification for all encrypted fields
- **Field isolation**: Each field encrypted with unique derived key

### Adversarial Resistance

- **Mimicry detection**: Identifies spoof attempts
- **Leakage quantification**: Measures semantic information exposure
- **Parameter adaptation**: Dynamic encryption strength adjustment
- **Continuous monitoring**: Real-time security assessment

## 📁 Project Structure & File Descriptions

### Core Pipeline Files

```
Sruvaan/
├── src/                           # Main source code
│   ├── __init__.py               # Package initialization
│   ├── schemas.py                # Pydantic data contracts for all agents
│   ├── config.py                 # GitHub Secrets & YAML template management
│   ├── llm_client.py             # LLM API integration (OpenAI/Anthropic)
│   ├── prompter.py               # Agent 1: Semantic parsing & intent extraction
│   ├── cryptor.py                # Agent 2: HKP encryption with role-based keys
│   ├── decryptor.py              # Agent 3: Role-based decryption & validation
│   ├── mimicus.py                # Agent 4: Adversarial mimicry simulation
│   ├── probator.py               # Agent 5: Leakage assessment & analysis
│   ├── praeceptor.py             # Agent 6: Parameter calibration & feedback
│   └── main_pipeline.py          # Pipeline orchestration & coordination
├── templates/                     # YAML prompt templates for LLM agents
│   ├── prompter.yaml             # Intent extraction prompts
│   ├── cryptor.yaml              # HKP encryption prompts
│   ├── mimicus.yaml              # Adversarial mimicry prompts
│   ├── probator.yaml             # Leakage analysis prompts
│   └── praeceptor.yaml           # Parameter calibration prompts
├── tests/                        # Test suite
│   ├── __init__.py               # Test package initialization
│   ├── test_prompter.py          # Unit tests for Prompter agent
│   ├── test_cryptor.py           # Unit tests for Cryptor agent
│   └── test_pipeline_integration.py  # Integration tests for full pipeline
├── .github/workflows/            # GitHub Actions CI/CD
│   └── test-pipeline.yml         # Automated testing workflow
├── requirements.txt              # Python dependencies
├── demo.py                       # Basic pipeline demonstration
├── github_secrets_demo.py        # GitHub Secrets integration demo
├── SETUP.md                      # Detailed setup guide
└── README.md                     # This file
```

### Detailed File Descriptions

#### Core Agent Files

**`src/schemas.py`**

- **Purpose**: Defines all data contracts between agents using Pydantic
- **Key Classes**: `RawInstructionInput`, `SemanticPromptOut`, `EncryptedOutput`, `MimicOutput`, `LeakageVectorOut`, `ThetaUpdate`
- **Usage**: Imported by all agents for type safety and data validation

**`src/config.py`**

- **Purpose**: Manages GitHub Secrets, environment variables, and YAML templates
- **Features**: Automatic template loading, secret validation, fallback creation
- **Methods**: `get_secret()`, `get_template()`, `validate_config()`

**`src/llm_client.py`**

- **Purpose**: Abstracts LLM API calls (OpenAI/Anthropic) with fallback mechanisms
- **Features**: Template-based prompting, JSON response parsing, error handling
- **Methods**: `call_llm()`, `parse_json_response()`, `_call_openai()`, `_call_anthropic()`

**`src/prompter.py`**

- **Purpose**: Parses raw user instructions into structured semantic fields
- **Input**: `RawInstructionInput` (instruction, language)
- **Output**: `SemanticPromptOut` (intent, entities, auth_level)
- **Features**: LLM integration with fallback to rule-based parsing

**`src/cryptor.py`**

- **Purpose**: Applies Hierarchical Keyed Protocol (HKP) encryption
- **Input**: `SemanticPromptOut`
- **Output**: `EncryptedOutput` (encrypted_fields, role_tag, pop_signature)
- **Features**: Role-based key derivation, PoP signatures, time constraints

**`src/decryptor.py`**

- **Purpose**: Reverses HKP encryption using role-based keys
- **Input**: `EncryptedOutput`
- **Output**: `DecryptedFieldsOut` (intent, entities, auth_grade)
- **Features**: PoP signature validation, role-based access control

**`src/mimicus.py`**

- **Purpose**: Simulates adversarial mimicry to probe for vulnerabilities
- **Input**: `DecryptedFieldsOut`
- **Output**: `MimicOutput` (mimic_fields, spoof_status)
- **Features**: Adversarial pattern generation, spoof detection

**`src/probator.py`**

- **Purpose**: Assesses semantic leakage and decipherability
- **Input**: `MimicOutput`
- **Output**: `LeakageVectorOut` (leakage_score, details, hk_protection)
- **Features**: Multi-metric leakage analysis, HKP protection assessment

**`src/praeceptor.py`**

- **Purpose**: Calibrates encryption parameters based on leakage assessment
- **Input**: `LeakageVectorOut`
- **Output**: `ThetaUpdate` (theta_update, mode, hk_feedback)
- **Features**: Parameter optimization, feedback loop integration

**`src/main_pipeline.py`**

- **Purpose**: Orchestrates the complete 6-agent pipeline
- **Functions**: `run_pipeline_demo()`, `run_pipeline_with_feedback()`
- **Features**: Sequential agent execution, error handling, result aggregation

#### Template Files

**`templates/*.yaml`**

- **Purpose**: Externalized LLM prompts for each agent
- **Structure**: `system_prompt`, `user_prompt`, `model`, `temperature`, `max_tokens`
- **Features**: Variable substitution (`{instruction}`, `{semantic_fields}`, etc.)
- **Auto-creation**: Default templates created if directory missing

#### Test Files

**`tests/test_prompter.py`**

- **Purpose**: Unit tests for Prompter agent functionality
- **Coverage**: Intent extraction, entity parsing, LLM integration, fallback mechanisms

**`tests/test_cryptor.py`**

- **Purpose**: Unit tests for Cryptor agent functionality
- **Coverage**: HKP encryption, key derivation, PoP signatures, role-based access

**`tests/test_pipeline_integration.py`**

- **Purpose**: Integration tests for complete pipeline flow
- **Coverage**: End-to-end pipeline execution, feedback loops, error handling

#### Demo Files

**`demo.py`**

- **Purpose**: Basic pipeline demonstration
- **Features**: Complete pipeline execution, individual agent showcase, feedback loop demo
- **Usage**: `python demo.py`

**`github_secrets_demo.py`**

- **Purpose**: GitHub Secrets integration demonstration
- **Features**: API key validation, configuration testing, setup guide
- **Usage**: `python github_secrets_demo.py`

#### CI/CD Files

**`.github/workflows/test-pipeline.yml`**

- **Purpose**: Automated testing in GitHub Actions
- **Features**: Secret injection, dependency installation, test execution, demo validation
- **Triggers**: Push to main/develop, pull requests

#### Configuration Files

**`requirements.txt`**

- **Purpose**: Python dependency specification
- **Key Dependencies**: `pydantic`, `openai`, `anthropic`, `PyYAML`, `pytest`

**`SETUP.md`**

- **Purpose**: Comprehensive setup guide
- **Content**: Prerequisites, installation, configuration, troubleshooting

## 🔄 Feedback Loop

The pipeline implements a continuous feedback loop:

1. **Praeceptor** analyzes leakage assessment from **Probator**
2. **Parameter calibration** adjusts encryption strength and HKP settings
3. **Updated theta parameters** flow back to **Cryptor**
4. **Improved encryption** provides better protection against mimicry
5. **Cycle repeats** for continuous security optimization

## 🚧 Development

### Adding New Agents

1. Create agent module in `src/`
2. Define I/O schemas in `src/schemas.py`
3. Implement `run_*` function with proper typing
4. Add unit tests in `tests/`
5. Update `src/main_pipeline.py` for integration

### Extending HKP

1. Modify `src/cryptor.py` for new key derivation schemes
2. Update `src/decryptor.py` for corresponding decryption
3. Enhance `src/probator.py` for new protection assessment
4. Extend `src/praeceptor.py` for parameter calibration

## 🔐 GitHub Secrets Integration

The pipeline supports secure API key management through GitHub Secrets:

### Setting Up Secrets

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ANTHROPIC_API_KEY`: Your Anthropic API key

### Automatic Loading

The pipeline automatically loads secrets in GitHub Actions:

```yaml
# .github/workflows/test-pipeline.yml
- name: Create environment file
  run: |
    cat > .env << EOF
    OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
    ANTHROPIC_API_KEY=${{ secrets.ANTHROPIC_API_KEY }}
    EOF
```

## 📝 YAML Templates

LLM prompts are externalized as YAML templates for easy customization:

### Template Structure

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

- **prompter.yaml**: Intent and entity extraction
- **cryptor.yaml**: HKP encryption with role-based keys
- **mimicus.yaml**: Adversarial mimicry simulation
- **probator.yaml**: Leakage analysis and assessment
- **praeceptor.yaml**: Parameter calibration and feedback

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

## 📚 References

- **CRYPTA_MCP_BITS.pdf**: Protocol specification (Section 2.2)
- **Hierarchical Keyed Protocols**: Role-scoped encryption schemes
- **Proof-of-Protocol**: Integrity verification mechanisms
- **Adversarial Testing**: Mimicry and leakage assessment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Run full test suite
5. Submit pull request

## 🔧 Troubleshooting & FAQ

### Common Issues

#### 1. **LLM API Key Issues**

**Problem**: `Missing required secrets: ['openai_api_key', 'anthropic_api_key']`

**Solution**:

```bash
# Set environment variables
export OPENAI_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-api-key"

# Or create .env file
echo "OPENAI_API_KEY=your-api-key" > .env
echo "ANTHROPIC_API_KEY=your-api-key" >> .env
```

#### 2. **Template Loading Issues**

**Problem**: `No templates loaded`

**Solution**:

```bash
# Templates are auto-created, but you can verify:
ls templates/
# Should show: prompter.yaml, cryptor.yaml, mimicus.yaml, probator.yaml, praeceptor.yaml
```

#### 3. **Import Errors**

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**:

```bash
# Make sure you're in the project root
cd /path/to/Sruvaan

# Install in development mode
pip install -e .
```

#### 4. **Test Failures**

**Problem**: Tests failing with Pydantic warnings

**Solution**:

```bash
# Update Pydantic to latest version
pip install --upgrade pydantic

# Or suppress warnings in tests
python -m pytest tests/ -v -W ignore::DeprecationWarning
```

#### 5. **GitHub Actions Issues**

**Problem**: Secrets not available in CI/CD

**Solution**:

1. Go to repository → Settings → Secrets and variables → Actions
2. Add secrets: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
3. Ensure workflow file references secrets correctly

### Performance Optimization

#### 1. **LLM Response Time**

**Issue**: Slow LLM responses

**Solutions**:

- Use `gpt-3.5-turbo` instead of `gpt-4` for faster responses
- Reduce `max_tokens` in templates
- Implement caching for repeated requests

#### 2. **Memory Usage**

**Issue**: High memory consumption

**Solutions**:

- Use smaller models in templates
- Implement streaming for large responses
- Monitor with `memory_profiler`

### Debugging

#### 1. **Enable Debug Logging**

```bash
# Set debug level
export LOG_LEVEL=DEBUG
python demo.py
```

#### 2. **Test Individual Components**

```bash
# Test specific agent
python -c "
import sys; sys.path.insert(0, 'src')
from prompter import run_prompter
from schemas import RawInstructionInput
result = run_prompter(RawInstructionInput(instruction='Transfer $100', language='EN'))
print(result)
"
```

#### 3. **Validate Configuration**

```bash
# Check configuration
python -c "
import sys; sys.path.insert(0, 'src')
from config import config
print('Valid:', config.validate_config())
print('Templates:', list(config.templates.keys()))
print('Secrets:', list(config.secrets.keys()))
"
```

### FAQ

#### Q: **Do I need API keys to run the pipeline?**

A: No! The pipeline has robust fallback mechanisms. Without API keys, it uses rule-based processing for all agents.

#### Q: **How do I customize LLM prompts?**

A: Edit files in `templates/` directory. Each agent has its own YAML template with `system_prompt` and `user_prompt`.

#### Q: **Can I add new agents?**

A: Yes! Create a new agent file in `src/`, define schemas in `schemas.py`, add tests, and update `main_pipeline.py`.

#### Q: **How do I deploy to production?**

A: Use GitHub Actions with secrets, or deploy with environment variables. The pipeline is stateless and container-ready.

#### Q: **What's the difference between HKP and regular encryption?**

A: HKP provides role-based access control, time constraints, and field-wise encryption with PoP signatures for integrity.

#### Q: **How do I monitor pipeline performance?**

A: Use the logging output, or add custom metrics in each agent. The feedback loop provides continuous optimization.

### Getting Help

1. **Check logs**: All agents provide detailed logging
2. **Run tests**: `python -m pytest tests/ -v`
3. **Validate config**: Use the configuration validation commands above
4. **Check templates**: Verify YAML files in `templates/` directory
5. **Review SETUP.md**: Comprehensive setup guide

## 📄 License

[License information to be added]

---

**Sruvaan MCP Pipeline** - Secure, role-based encryption with adversarial testing and continuous parameter calibration.
