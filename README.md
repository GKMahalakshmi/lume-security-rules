
# Lume Security Rules

A security rules repository for identifying and documenting risks in Large Language Model (LLM) applications.

## Objectives

- Identify prompt injection attacks.
- Detect attempts to expose system prompts and hidden instructions.
- Document attack patterns, detection rules, and mitigation strategies.
- Support testing and validation of AI application security controls.

## Security Rules

| Rule ID | Vulnerability | Purpose |
|---|---|---|
| LLM01 | Prompt Injection | Identify attempts to override instructions or manipulate an AI model. |
| LLM07 | System Prompt Leakage | Identify attempts to reveal hidden system instructions or confidential prompt content. |

These IDs follow the OWASP LLM Top 10 2023 classification.

## Repository Structure

```text
lume-security-rules/
├── README.md
└── rules/
    ├── LLM01_prompt_injection.md
    └── LLM07_system_prompt_leakage.md
```

## Testing Approach

Each rule documents:
- Rule ID and name
- Threat description
- Example attack inputs
- Detection indicators
- Expected secure behavior
- Mitigation recommendations

## Security Note

Detection rules are intended to support security testing. They do not guarantee detection of every attack. Validate rules against representative test cases before production use.

## References

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)

## Project Status

Initial security rule development and validation.
