# Lume Security Rules (`lume-security-rules`)

Detection rules and validation tests for LLM and AI agent security, focusing on OWASP Top 10 for LLMs and agentic AI vulnerability patterns.

---

## 1. Project Purpose and Scope

**Lume Security Rules** provides modular, vendor-agnostic detection rules designed for integration into the **Lume Security Toolkit** and other Python-based scanning and monitoring pipelines.

### Purpose
- Define declarative, auditable detection rules for AI security threats.
- Provide a rigorous testing standard that prevents false positives on harmless educational, conceptual, or defensive discussions.
- Establish a transparent lifecycle to mature rules from initial experimental proposals to validated production signatures.

### Supported Security Categories
1. **LLM01: Prompt Injection**
   - Direct instruction overrides (`ignore previous instructions`, `bypass rules`).
   - Structural delimiter forgery and persona spoofing (`[SYSTEM]`, `<<SYS>>`, Developer Mode switches).
2. **LLM07: System Prompt Leakage**
   - System prompt exfiltration requests (demands for verbatim instructions or pre-prompt text).
   - Response-side internal directive disclosure (leakage of hidden developer directives or internal guardrails).

### Out of Scope
- Attack weaponization scripts or exploitation tooling.
- Production credentials, actual private system prompts, or real-world confidential data.
- Unfiltered keyword-only matching engines.

---

## 2. Experimental Status Notice

> **IMPORTANT NOTICE:**  
> All rules in this repository are currently designated as **`experimental / unvalidated`**.  
> They are undergoing active research and validation. Do **not** rely on these rules as production guarantees without empirical testing against your specific application domains and traffic distributions.

---

## 3. Repository Structure

```text
lume-security-rules/
├── README.md                                  # Repository overview and guide
├── .gitignore                                 # Git ignore configurations
├── docs/
│   └── rule_specification.md                  # Rule schema and lifecycle specification
├── rules/
│   ├── llm01_prompt_injection/
│   │   ├── direct_instruction_override.yaml   # Rule LUME-LLM01-001
│   │   └── role_override_delimiter_hijack.yaml# Rule LUME-LLM01-002
│   └── llm07_system_prompt_leakage/
│       ├── system_prompt_exfiltration_request.yaml # Rule LUME-LLM07-001
│       └── response_instruction_leakage.yaml       # Rule LUME-LLM07-002
└── tests/
    ├── test_rules.py                          # Rule schema & detection test suite
    └── fixtures/
        ├── llm01_prompt_injection/
        │   ├── positive/                      # Synthetic injection payloads
        │   └── negative/                      # Benign discussions & research queries
        └── llm07_system_prompt_leakage/
            ├── positive/                      # Synthetic exfiltration & leakage samples
            └── negative/                      # Benign architectural & educational queries
```

---

## 4. Rule Validation Methodology

Rules must strictly avoid classifying benign discussions as security attacks. For instance, a query such as:
> *"What is prompt injection and why do attackers use 'ignore previous instructions'?"*

must **never** be flagged as an attack merely because it contains the phrase "ignore previous instructions".

Validation involves:
1. **Paired Test Fixtures:** Every rule must be tested against both synthetic positive samples (attacks) and synthetic negative samples (benign conceptual discussions).
2. **Exclusion / Negative Logic:** Rules incorporate negative pattern filtering to discount questions, educational queries, and security research discussions.
3. **Automated Schema & Logic Testing:** All rules are verified using an automated test suite.

---

## 5. How to Run Tests

The test suite validates both rule schemas and detection efficacy using standard Python (no external dependencies required):

```bash
# Run the test suite using standard Python unittest
python tests/test_rules.py

# Or run discovery across all tests
python -m unittest discover tests
```

### Expected Output
```text
..
Rule Validation Results: 4 positive attacks caught, 4 benign fixtures correctly cleared (0 false positives).
----------------------------------------------------------------------
Ran 4 tests in 0.015s

OK
```

---

## 6. Current Limitations and Future Integration

### Current Limitations
- **Obfuscation Sensitivity:** Static regex heuristics can be bypassed by Base64 encoding, ciphers, leetspeak, or prompt translation into low-resource languages.
- **Multilingual Scope:** Current experimental rules focus primarily on English language attack constructs.
- **Context Boundaries:** Multi-turn jailbreaks and indirect prompt injections embedded in retrieved documents (RAG) require runtime state tracking beyond static single-turn pattern matching.

### Future Integration Plans
- **Lume Security Toolkit Engine:** Direct ingestion into the Lume Security Toolkit scanner for real-time inference guardrails and batch log auditing.
- **Semantic Embeddings & Canaries:** Augmenting static regex with embedding distance checks and canary token verification for LLM07 leakage detection.
- **Benchmark Datasets:** Continuous evaluation against benchmark datasets (e.g. JailbreakBench, BeaverTails) to quantify precision and recall before promoting rules to `validated`.

---

## 7. Contributing

See [`docs/rule_specification.md`](docs/rule_specification.md) for detailed guidelines on the rule lifecycle, authoring standards, and how to submit new rules.
