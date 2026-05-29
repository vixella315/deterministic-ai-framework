# Deterministic AI Framework

![Status](https://img.shields.io/badge/status-active-success)
![Architecture](https://img.shields.io/badge/architecture-deterministic-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> Stop guessing. Start building reliable AI systems.

---

## 🧠 What is Deterministic AI?

Most AI systems are built as black-box chatbots.

**Deterministic AI** is an engineering framework for building:

* Schema-first pipelines
* Self-healing AI outputs
* Production-grade validation systems

This transforms AI from **probabilistic guessing** into **reliable infrastructure**.

---

## 🔧 Core Principles

* **Schema First** → Define structure before generation
* **Validation Always** → Never trust raw AI output
* **Self-Healing** → Automatically repair broken outputs
* **Auditability** → Every asset is traceable

---

## ⚙️ What This Framework Does

* Generates structured AI outputs
* Validates against defined schemas
* Automatically fixes missing or broken fields
* Provides production-ready logging and asset tracking

---

## 🔥 Golden Pipeline (Proof)

Failure → Detection → Healing → Success

### Run the pipeline:

```bash
python examples/golden_pipeline.py
```

### Example Output:

```
STEP 1 — RAW OUTPUT (FAILURE):
{'title': 'AI Product'}

STEP 2 — VALIDATION RESULT:
Valid: False | Error: missing description

STEP 3 — HEALING TRIGGERED

STEP 4 — HEALED OUTPUT:
{'title': 'AI Product', 'description': '...'}

STEP 5 — FINAL VALIDATION:
Valid: True | Error: None
```

---

## 🧱 Why This Matters

Most AI pipelines:

* Fail silently
* Require manual fixes
* Break at scale

This framework:

* Detects failure instantly
* Repairs automatically
* Guarantees valid output

This is the difference between:

**AI demos vs AI infrastructure**

---

## 🚫 What This Framework Does NOT Include

This repository does NOT include:

* Demand prediction systems
* Pricing logic
* Revenue optimization engines

This framework focuses purely on **deterministic AI production infrastructure**.

The economic layer operates separately.

---

## 🚀 Installation

```bash
pip install -e .
```

---

## ⚡ Quick Start

```python
from deterministic.contractual_prompt_factory import ContractualPromptFactory
```

Run:

```bash
python examples/golden_pipeline.py
```

---

## 🏛️ Philosophy

We don’t just generate content.

We build **AI supply chains**.
