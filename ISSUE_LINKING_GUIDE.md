# Linking Commits to GitHub Issues

## 🔗 **Methods to Link Commits to Issues**

### **1. Automatic Linking (Recommended)**

When you commit and push, GitHub automatically links commits to issues if you include issue numbers in your commit message:

```bash
# Method 1: Include issue number in commit message
git commit -m "feat: implement LLM-only mode and OpenAI-only runtime flags

Add comprehensive runtime control for LLM processing with fallback prevention
and provider-specific restrictions. Includes detailed pipeline stage analysis
and enhanced error handling for production deployments.

Closes #123
Fixes #124
Related to #125

- Add --llm-only flag to force LLM usage without fallbacks
- Add --openai-only flag to restrict API usage to OpenAI only
- Implement environment variable checks across all 6 agents
- Add detailed pipeline stage documentation with inputs/outputs
- Enhance error messages with setup instructions
- Create comprehensive testing and validation framework
- Add visual data flow documentation for each pipeline stage
- Implement backward compatibility with existing fallback behavior
- Add security metrics analysis and recommendations
- Create production-ready deployment documentation

Breaking Changes: None (backward compatible)
Security: Enhanced with LLM-only mode for production deployments
Testing: Comprehensive validation with multiple scenarios
Documentation: Complete pipeline stage analysis and visual summaries"
```

### **2. Manual Linking in Pull Request**

When creating a pull request, you can link issues in the description:

````markdown
## 🚀 LLM-Only Mode Implementation

This PR implements comprehensive runtime control for the Sruvaan MCP Pipeline.

### 🔧 **Core Features**

- Add `--llm-only` flag to force LLM usage without fallbacks
- Add `--openai-only` flag to restrict API usage to OpenAI only
- Implement environment variable checks across all 6 agents
- Add detailed pipeline stage documentation with inputs/outputs

### 📊 **Testing Results**

- ✅ LLM-Only Mode: Forces LLM usage, fails gracefully without API keys
- ✅ OpenAI-Only Mode: Restricts to OpenAI API, converts Claude models
- ✅ Normal Mode: Maintains existing fallback behavior
- ✅ Error Handling: Comprehensive error scenarios tested

### 🔗 **Related Issues**

Closes #123
Fixes #124
Related to #125

### 📁 **Files Modified**

- `demo.py`: Added argument parsing and environment variable setting
- `src/prompter.py`: Added LLM-only mode checks and error handling
- `src/cryptor.py`: Added LLM-only mode checks and error handling
- `src/mimicus.py`: Added LLM-only mode checks and error handling
- `src/probator.py`: Added LLM-only mode checks and error handling
- `src/praeceptor.py`: Added LLM-only mode checks and error handling
- `src/llm_client.py`: Added OpenAI-only mode support and provider conversion
- `README.md`: Updated with new runtime flags and usage examples
- `LLM_ONLY_MODE_SUMMARY.md`: Comprehensive implementation summary
- `PIPELINE_STAGES_DETAILED.md`: Detailed stage-by-stage analysis
- `PIPELINE_VISUAL_SUMMARY.md`: Visual data flow documentation

### 🧪 **Testing**

```bash
# Test LLM-only mode
python demo.py --llm-only

# Test OpenAI-only mode
python demo.py --openai-only

# Test normal mode
python demo.py
```
````

### ✅ **Success Criteria Met**

- ✅ Runtime flag implementation
- ✅ LLM-only mode (no fallbacks)
- ✅ OpenAI-only mode
- ✅ Clear error messages
- ✅ Backward compatibility
- ✅ Environment variable support
- ✅ All agents modified
- ✅ Comprehensive testing
- ✅ Detailed documentation
- ✅ Production readiness

````

### **3. GitHub Keywords for Automatic Linking**

Use these keywords in your commit message or PR description:

| Keyword | Action |
|---------|--------|
| `Closes #123` | Closes the issue when merged |
| `Fixes #123` | Closes the issue when merged |
| `Resolves #123` | Closes the issue when merged |
| `Related to #123` | Links to issue without closing |
| `Addresses #123` | Links to issue without closing |
| `Refs #123` | Links to issue without closing |

### **4. Command Line Examples**

```bash
# Commit with issue linking
git commit -m "feat: implement LLM-only mode and OpenAI-only runtime flags

Add comprehensive runtime control for LLM processing with fallback prevention
and provider-specific restrictions.

Closes #123
Fixes #124
Related to #125

- Add --llm-only flag to force LLM usage without fallbacks
- Add --openai-only flag to restrict API usage to OpenAI only
- Implement environment variable checks across all 6 agents
- Add detailed pipeline stage documentation with inputs/outputs
- Enhance error messages with setup instructions
- Create comprehensive testing and validation framework
- Add visual data flow documentation for each pipeline stage
- Implement backward compatibility with existing fallback behavior
- Add security metrics analysis and recommendations
- Create production-ready deployment documentation

Breaking Changes: None (backward compatible)
Security: Enhanced with LLM-only mode for production deployments
Testing: Comprehensive validation with multiple scenarios
Documentation: Complete pipeline stage analysis and visual summaries"

# Push to trigger automatic linking
git push origin main
````

### **5. Creating an Issue First (Recommended Workflow)**

1. **Create the Issue**:

   ```markdown
   ## 🚀 Implement LLM-Only Mode and Runtime Flags

   ### **Objective**

   Add runtime control for LLM processing with fallback prevention and provider-specific restrictions.

   ### **Requirements**

   - [ ] Add `--llm-only` flag to force LLM usage without fallbacks
   - [ ] Add `--openai-only` flag to restrict API usage to OpenAI only
   - [ ] Implement environment variable checks across all 6 agents
   - [ ] Add detailed pipeline stage documentation with inputs/outputs
   - [ ] Enhance error messages with setup instructions
   - [ ] Create comprehensive testing and validation framework
   - [ ] Add visual data flow documentation for each pipeline stage
   - [ ] Implement backward compatibility with existing fallback behavior
   - [ ] Add security metrics analysis and recommendations
   - [ ] Create production-ready deployment documentation

   ### **Acceptance Criteria**

   - [ ] LLM-only mode forces LLM usage, fails gracefully without API keys
   - [ ] OpenAI-only mode restricts to OpenAI API, converts Claude models
   - [ ] Normal mode maintains existing fallback behavior
   - [ ] Error handling comprehensive error scenarios tested
   - [ ] Backward compatibility with existing functionality
   - [ ] Production-ready deployment capabilities
   - [ ] Comprehensive documentation and testing

   ### **Technical Details**

   - **Files to Modify**: All 6 agents + demo script + documentation
   - **Environment Variables**: `LLM_ONLY_MODE`, `OPENAI_ONLY_MODE`
   - **Testing**: Multiple scenarios with different API key configurations
   - **Documentation**: Pipeline stage analysis and visual summaries

   ### **Priority**

   High - Production readiness feature

   ### **Labels**

   - `enhancement`
   - `production`
   - `security`
   - `documentation`
   ```

2. **Reference the Issue in Your Commit**:

   ```bash
   git commit -m "feat: implement LLM-only mode and OpenAI-only runtime flags

   Closes #123

   Add comprehensive runtime control for LLM processing with fallback prevention
   and provider-specific restrictions. Includes detailed pipeline stage analysis
   and enhanced error handling for production deployments.

   - Add --llm-only flag to force LLM usage without fallbacks
   - Add --openai-only flag to restrict API usage to OpenAI only
   - Implement environment variable checks across all 6 agents
   - Add detailed pipeline stage documentation with inputs/outputs
   - Enhance error messages with setup instructions
   - Create comprehensive testing and validation framework
   - Add visual data flow documentation for each pipeline stage
   - Implement backward compatibility with existing fallback behavior
   - Add security metrics analysis and recommendations
   - Create production-ready deployment documentation

   Breaking Changes: None (backward compatible)
   Security: Enhanced with LLM-only mode for production deployments
   Testing: Comprehensive validation with multiple scenarios
   Documentation: Complete pipeline stage analysis and visual summaries"
   ```

### **6. GitHub Actions Integration**

You can also link issues in GitHub Actions workflows:

```yaml
name: Link to Issue
on:
  push:
    branches: [main]

jobs:
  link-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Link commit to issue
        uses: actions/github-script@v6
        with:
          script: |
            const issue_number = 123;
            const commit_sha = context.sha;

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issue_number,
              body: `🔗 **Commit Linked**: ${commit_sha}\n\nThis commit implements the requested LLM-only mode functionality.`
            });
```

### **7. Best Practices**

1. **Create Issues First**: Always create an issue before implementing features
2. **Use Descriptive Keywords**: Use `Closes`, `Fixes`, or `Related to` appropriately
3. **Include Issue Numbers**: Always include issue numbers in commit messages
4. **Update Issue Status**: Use keywords to automatically close issues when merged
5. **Document Changes**: Include detailed descriptions in PR descriptions
6. **Test Linking**: Verify that issues are properly linked after pushing

### **8. Verification**

After pushing, you can verify the linking worked by:

1. Going to the issue page
2. Checking the "Linked pull requests" section
3. Looking for commit references in the issue timeline
4. Verifying the issue status (closed if using `Closes` keyword)

This ensures proper tracking and documentation of your implementation! 🚀
