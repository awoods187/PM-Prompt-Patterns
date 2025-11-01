# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2.0 | :x:                |

## Reporting a Vulnerability

We take the security of PM Prompt Toolkit seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do NOT Create a Public Issue

Please **do not** open a public GitHub issue for security vulnerabilities. Public disclosure could put users at risk.

### 2. Send a Private Report

Email security reports to: **[MAINTAINER_EMAIL]** (Update this before publishing)

Include in your report:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

### 3. Response Timeline

- **Initial Response:** Within 48 hours
- **Severity Assessment:** Within 72 hours
- **Fix Timeline:**
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: 90 days

### 4. Coordinated Disclosure

We follow coordinated disclosure:
- We'll work with you to understand and verify the issue
- We'll develop and test a fix
- We'll coordinate on timing for public disclosure
- We'll credit you in the security advisory (unless you prefer anonymity)

## Security Best Practices

### API Key Management

**CRITICAL:** Never commit API keys to version control

✅ **DO:**
- Store API keys in `.env` file (gitignored)
- Use environment variables
- Rotate keys regularly
- Use different keys for dev/staging/production
- Use secrets managers in production (AWS Secrets Manager, GCP Secret Manager, etc.)

❌ **DON'T:**
- Hardcode API keys in code
- Commit `.env` file to git
- Share API keys in documentation
- Use production keys for testing

### Secure Configuration

1. **Environment Variables**
   ```bash
   # Use .env file (never commit this)
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   OPENAI_API_KEY=sk-your-key-here
   GOOGLE_API_KEY=your-key-here
   ```

2. **Secrets Managers (Production)**
   ```python
   # AWS Secrets Manager
   import boto3
   secret = boto3.client('secretsmanager').get_secret_value(SecretId='api-keys')

   # GCP Secret Manager
   from google.cloud import secretmanager
   secret = secretmanager.SecretManagerServiceClient().access_secret_version(...)
   ```

3. **Key Validation**
   - Settings module validates key format before use
   - Fails fast if keys are missing or invalid
   - Never logs actual key values

### Input Validation

The toolkit includes built-in security controls:

1. **XML Injection Prevention**
   - All user input is escaped before use in XML prompts
   - Uses `xml.sax.saxutils.escape()`
   - See: `pm_prompt_toolkit/providers/claude.py:167`

2. **API Key Validation**
   - Format validation in `pm_prompt_toolkit/config/settings.py`
   - Length checks and placeholder detection
   - Clear error messages without exposing keys

3. **Error Message Sanitization**
   - Customer data truncated in error logs
   - See: `pm_prompt_toolkit/providers/claude.py:215`

### Dependency Security

We use multiple layers of dependency security:

1. **Dependabot**
   - Automated dependency updates
   - Security vulnerability scanning
   - See: `.github/dependabot.yml`

2. **Pre-commit Hooks**
   - Code quality checks before commit
   - See: `.pre-commit-config.yaml`

3. **Recommended: Additional Tools**
   ```bash
   # Python security linters
   pip install bandit safety pip-audit

   # Run security scans
   bandit -r pm_prompt_toolkit/
   safety check
   pip-audit
   ```

### Production Deployment

**Checklist before deploying:**

- [ ] All API keys stored in secrets manager
- [ ] `.env` file NOT deployed to production
- [ ] Logging configured to NOT log API keys
- [ ] Input validation enabled
- [ ] Rate limiting configured
- [ ] Error handling doesn't leak sensitive data
- [ ] Dependencies scanned for vulnerabilities
- [ ] Monitoring and alerting configured

## Known Security Considerations

### LLM-Specific Risks

1. **Prompt Injection**
   - User input should be treated as untrusted
   - Use structured prompts (XML) to separate instructions from data
   - Validate and sanitize all user-provided content

2. **Data Privacy**
   - LLM API calls send data to third parties (Anthropic, OpenAI, Google)
   - Review each provider's data handling policies
   - Consider data residency requirements
   - Avoid sending PII or confidential data when possible

3. **Cost Control**
   - Implement rate limiting to prevent abuse
   - Set budget alerts in provider consoles
   - Monitor usage metrics
   - Use cascading strategies to control costs

### Cloud Provider Security

**AWS Bedrock:**
- Use IAM roles, not long-lived access keys
- Enable CloudTrail logging
- Use VPC endpoints for private access

**Google Vertex AI:**
- Use service accounts with minimal permissions
- Enable audit logging
- Use VPC Service Controls when possible

**OpenAI / Anthropic Direct:**
- Rotate API keys regularly
- Monitor usage dashboards
- Set usage limits

## Security Features

### Built-in Protections

✅ **Environment Variable Management**
- Pydantic Settings with validation
- No hardcoded credentials in code
- Clear error messages for missing keys

✅ **Input Sanitization**
- XML escaping for Claude prompts
- Type validation with Pydantic
- Length and format checks

✅ **Error Handling**
- Sensitive data truncation in logs
- No API keys in error messages
- Clear but safe error reporting

✅ **Testing**
- 80%+ test coverage
- Security-focused test cases
- Mock providers for safe testing

### Compliance Considerations

**GDPR / Data Privacy:**
- Data sent to LLM providers may be subject to their retention policies
- Review each provider's DPA (Data Processing Agreement)
- Consider data anonymization before sending to LLMs

**SOC 2 / ISO 27001:**
- Use secrets managers for credential storage
- Enable audit logging
- Implement access controls
- Regular security reviews

## Security Updates

Subscribe to security updates:
- Watch this repository for security advisories
- Enable Dependabot alerts
- Follow provider security bulletins:
  - [Anthropic Security](https://www.anthropic.com/security)
  - [OpenAI Security](https://platform.openai.com/docs/security)
  - [Google AI Security](https://ai.google.dev/docs/safety)

## Vulnerability Disclosure History

No security vulnerabilities have been reported to date.

---

**Last Updated:** 2025-10-31
**Next Review:** 2026-01-31

For questions about this security policy, contact: **[MAINTAINER_EMAIL]**
