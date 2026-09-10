# QuantumShield — Post-Quantum Cryptography Readiness & CBOM Platform

**Smart India Hackathon 2026 — Software Edition**  
**Problem Statement ID:** 26164  
**Title:** Post-Quantum Cryptography readiness / discovery and inventory of Cryptographic Artefacts  
**Project Type:** Working Software Prototype / Functional Product  

---

## 1. Problem Overview

With the imminent advancement of quantum computing, public-key cryptographic algorithms such as **RSA, ECC, ECDSA, ECDH, and DSA** will become completely vulnerable to **Shor’s Algorithm** running on a Cryptographically Relevant Quantum Computer (CRQC). Organizations face severe exposure under **"Harvest Now, Decrypt Later"** attacks, where encrypted sensitive data with long lifetime requirements is recorded today and decrypted when quantum capabilities emerge.

Organizations currently lack visibility into:
1. **What cryptographic assets exist** across legacy and cloud software systems.
2. **Which primitives are vulnerable** to classical vs. quantum threats.
3. **Which assets must be migrated first** based on risk, data sensitivity, and business criticality.
4. **What standardized Post-Quantum Cryptography (PQC)** alternatives should replace legacy primitives.
5. **When migration must happen** according to mathematical models such as the Mosca Theorem.
6. **How cryptographic assets depend on applications and files** across the blast radius.

---

## 2. Solution Overview

**QuantumShield** is an end-to-end, zero-fake-data Quantum-Safe Cryptographic Bill of Materials (CBOM) Intelligence & Migration Platform. It scans software source code static assets (ZIP archives, GitHub URLs, or local demo projects), automatically catalogs cryptographic primitives into a CycloneDX-compatible CBOM, calculates multi-factor risk scores, prioritizes P0–P3 migration candidates, recommends NIST FIPS-standardized PQC targets (**ML-KEM, ML-DSA, SLH-DSA**), models Mosca migration timelines, visualizes interactive dependency graphs, and generates executive PDF security reports.

---

## 3. Technology Stack

### Backend
- **Language & Framework:** Python 3.11+, FastAPI
- **Database & ORM:** SQLite (MVP local DB) / PostgreSQL-compatible schema via SQLAlchemy, Pydantic v2
- **Data & Intelligence Libraries:** scikit-learn, pandas, numpy, NetworkX
- **Reporting & Security:** ReportLab (PDF Generation), GitPython (Static Git Ingestion), ZipSlip-safe extractors

### Frontend
- **Framework & Build Tool:** React 18+, Vite
- **Routing & State:** React Router v6, Axios, React Context API
- **Styling & Icons:** Tailwind CSS (Dark Enterprise Cybersecurity SaaS aesthetic), Lucide React
- **Visualization:** Recharts (Risk/Algorithm Analytics), `@xyflow/react` (Interactive React Flow Dependency Graph)

---

## 4. Platform Architecture

```
quantumshield/
│
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI Application Entrypoint & Middleware
│   │   ├── api/                      # REST API Endpoints (projects, scans, assets, roadmap, graph, reports)
│   │   ├── core/                     # Configuration settings & SQLAlchemy database session setup
│   │   ├── models/                   # ORM Models (Project, Scan, Finding, Asset, Risk, Recommendation, Dependency, Roadmap)
│   │   ├── schemas/                  # Pydantic v2 validation schemas
│   │   ├── services/                 # Business logic orchestration services
│   │   ├── scanners/                 # Multi-language static code & manifest scanners (Java, Python, JS, Library, Container)
│   │   ├── engines/                  # Intelligence Engines (Purpose Classifier, Risk Engine, Priority Engine, PQC Recommender, Mosca Engine)
│   │   ├── graph/                    # NetworkX dependency graph builder
│   │   ├── cbom/                     # CycloneDX 1.5 JSON CBOM Generator
│   │   └── utils/                    # Patterns, file security, Zip-Slip prevention, GitHub validator
│   ├── tests/                        # Pytest suite (engine tests, scanner tests, E2E pipeline tests)
│   ├── generated_reports/            # Output PDF reports
│   ├── tmp_uploads/                  # Isolated temporary extraction directory
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── api/client.js             # Centralized Axios API client
│   │   ├── components/               # Reusable UI (Sidebar, Topbar, MetricCard, RiskBadge, PriorityBadge, CustomNode)
│   │   ├── context/                  # Global Project Context
│   │   ├── pages/                    # 8 SaaS Dashboard Pages
│   │   ├── App.jsx                   # React Router layout
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
│
├── demo-project/                     # Pre-packaged multi-language test suite
│   ├── java/CryptoService.java
│   ├── python/security_module.py
│   ├── javascript/auth_handler.js
│   ├── pom.xml
│   ├── requirements.txt
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## 5. End-to-End Scanning Workflow

```
Source Ingestion (ZIP / GitHub / Demo)
       ↓
Safe Extraction & Isolation (Zip Slip Check, File Limits)
       ↓
Multi-Language Static Analysis (Regex & Abstract AST Token Matching)
       ↓
Raw Findings Storage (Preserving file path, line number, matched text, surrounding context, detector, confidence)
       ↓
Purpose Classification Engine (Context-aware: Key Establishment, Signature, Encryption, Hashing, TLS, Unknown)
       ↓
Crypto Asset Normalization & Deduplication
       ↓
Quantum & Classical Risk Engine (35% Quantum + 20% Sensitivity + 20% Lifetime + 15% Criticality + 10% Difficulty)
       ↓
Quantum Migration Priority Engine (P0 Immediate, P1 High, P2 Planned, P3 Monitor)
       ↓
PQC Recommendation Engine (NIST FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA)
       ↓
Interactive Dependency Graph (@xyflow/react)
       ↓
Mosca Migration Roadmap & CycloneDX CBOM JSON Export
       ↓
Executive PDF Security Report Generation
```

---

## 6. Key Intelligence Engines & Methodologies

### A. Quantum & Classical Risk Engine
- **Weights:**
  - **Quantum Vulnerability:** 35%
  - **Data Sensitivity:** 20%
  - **Data Protection Lifetime:** 20%
  - **Business Criticality:** 15%
  - **Migration Difficulty:** 10%
- **Risk Bands:** `0–30: LOW`, `31–60: MEDIUM`, `61–80: HIGH`, `81–100: CRITICAL`.
- **Nuance Note:** Modern symmetric encryption (e.g. AES-256) is **not broken** by quantum computing. Grover's algorithm halves key length (AES-128 drops to 64-bit security margin, AES-256 remains 128-bit quantum-safe). AES primitives are categorized as **MONITOR** items rather than replaced with PQC KEMs.

### B. NIST Post-Quantum Cryptography Recommendations
- **Key Establishment / KEM:** `ML-KEM (Module-Lattice-Based Key Encapsulation Mechanism - NIST FIPS 203)`
- **Digital Signatures:** `ML-DSA (Module-Lattice-Based Digital Signature Algorithm - NIST FIPS 204)`
- **Hash-Based Signatures:** `SLH-DSA (Stateless Hash-Based Digital Signature Algorithm - NIST FIPS 205)`
- **Legacy Weak Hashes (MD5, SHA-1):** Migrated to `SHA-256` / `SHA-384`.

### C. Mosca Theorem Migration Analysis
Determines required security window:
$$\text{Required Security Window} = \text{Data Protection Lifetime } (Y) + \text{Estimated Migration Time } (Z)$$
Compares against the user-configured **Planning Threat Horizon** $(X)$:
- If $Y + Z > X \implies$ **URGENT**
- If $Y + Z \ge X - 2 \implies$ **ACCELERATE**
- Otherwise $\implies$ **PLANNED**

---

## 7. Installation & Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- (Optional) Docker & docker-compose

### Local Setup (Student Laptop / Quick Run)

#### Step 1: Start Backend Server
```bash
cd backend
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app/main.py
```
*Backend runs at:* `http://localhost:8000`  
*API Documentation:* `http://localhost:8000/api/docs`

#### Step 2: Start Frontend Application
```bash
cd frontend
npm install
npm run dev
```
*Frontend runs at:* `http://localhost:5173`

---

## 8. Demo Scan Instructions

1. Open `http://localhost:5173` in your browser.
2. Navigate to **Projects** $\to$ Click **Launch & Scan Demo Project**.
3. The platform will clone/read the local `demo-project/` containing vulnerable Java, Python, Node.js code, manifests (`pom.xml`, `requirements.txt`), and `Dockerfile`.
4. Observe real-time discovery of:
   - **RSA-2048** in `CryptoService.java` & `security_module.py` (Quantum Risk, P0 Priority, ML-KEM / ML-DSA guidance).
   - **ECDSA & ECDH** (Quantum Risk, P1 Priority).
   - **AES-256-GCM** (Monitor Item, Key length guidance).
   - **MD5** (Classical Weakness, SHA-256 target).
5. Open **Asset Details** $\to$ Edit data sensitivity from Medium to Critical $\to$ Click **Recalculate Risk & Priority** to observe live dynamic scoring.
6. Open **Dependency Graph** to interactively zoom, pan, and filter nodes.
7. Open **Migration Roadmap** to adjust the Threat Horizon sliders.
8. Click **CBOM JSON** or **PDF Report** in the top bar to download exports.

---

## 9. Automated Testing

Run the comprehensive pytest test suite covering scanners, risk weight scoring, PQC mapping, Mosca theorem, and end-to-end API integration:

```bash
cd backend
.\venv\Scripts\python.exe -m pytest tests/
```

---

## 10. Limitations & Future Enhancements

### Current MVP Limitations
- Scanners run static regex/pattern matching (dynamic binary AST parsing is not executed to preserve system safety).
- Database defaults to local SQLite file `quantumshield.db`.

### Future Enterprise Roadmap
- PostgreSQL production cluster support.
- CI/CD GitHub Action & GitLab Runner integrations.
- Binary artifact scanning (.jar, .dll, ELF executables).
- Automated pull request creation for hybrid PQC code refactoring.
