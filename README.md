# 🩺 BioGuard AI — Autonomous Clinical Triage & Drug Verification Platform

> **AgentVerse 2026 Hackathon Project (Supported by OpenAI)**  
> *An autonomous AI agent platform for low-resource rural health clinics, featuring multi-tool execution for emergency triage, counterfeit medication detection, and inventory management.*

---

## 📌 Problem Statement
Rural healthcare clinics frequently suffer from:
1. **Clinical Triage Bottlenecks:** Limited access to emergency physicians leads to delayed identification of critical patient conditions.
2. **Counterfeit & Recalled Drugs:** Sub-standard and counterfeit pharmaceutical batches pose life-threatening risks in underserved regions.
3. **Stockout Vulnerability:** Poor inventory tracking leads to critical shortages of essential medicine.

**BioGuard AI** addresses these challenges by acting as an autonomous clinical co-pilot that executes real-time vital analysis, batch verification, and stock checking.

---

## 🛠️ Key Capabilities & Tools

BioGuard AI uses **LangChain tool binding** to interact with clinical databases:

1. **`evaluate_patient_triage`**: Analyzes SpO₂, heart rate, temperature, and symptoms to return a color-coded priority level (**🔴 RED**, **🟡 YELLOW**, **🟢 GREEN**).
2. **`verify_drug_batch`**: Cross-references pharmaceutical batch numbers against national safety registries to flag expired or counterfeit stock.
3. **`check_clinic_inventory`**: Monitors current drug stock, cabinet storage locations, and automated reorder alerts.

---

## 🏗️ Architecture & Tech Stack

* **LLM Engine:** Groq API (`openai/gpt-oss-20b`) / OpenAI GPT-4o-mini
* **Agent Framework:** LangChain (Tool Calling & Multi-Step Reasoning)
* **Frontend UI:** Streamlit Web Application
* **Database:** Local JSON Clinical Registry (`database.json`)
* **Environment Management:** Python 3.11+, `python-dotenv`

---

## 🚀 Quick Start & Local Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/HackIndiaXYZ/ai-agents-hackathon-agentverse-2026-supported-by-openai-null.git](https://github.com/HackIndiaXYZ/ai-agents-hackathon-agentverse-2026-supported-by-openai-null.git)
cd ai-agents-hackathon-agentverse-2026-supported-by-openai-null