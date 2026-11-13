# Cheminformatics Virtual Laboratory

An advanced, interactive educational virtual laboratory and scientific workstation for molecular representation, chemical structure visualization, computational descriptor calculations, functional group identification, structure–property analysis, academic assessment, and publication-quality report generation.

**Architectural Modernization:** Streamlit has been completely eliminated and replaced with a modern, decoupled scientific web application:
- **Frontend:** React 18 + Vite + TypeScript + Custom Scientific CSS + Lucide Icons + 3Dmol.js + Plotly.js
- **Backend:** Python 3.11 + FastAPI + RDKit + NumPy + Pandas + ReportLab

---

## 1. Project Overview & Architectural Enhancement

This application modernizes the original Python educational Cheminformatics Virtual Laboratory. The enhancement preserves 100% of the original scientific calculations and educational workflows while introducing a professional workstation UI and a modern decoupled architecture:

- **Decoupled Client-Server Architecture:** High-speed FastAPI REST backend serving scientific computations, pure SVG vector depictions, and ReportLab PDF dossiers to a responsive React/TypeScript client.
- **Restrained Scientific Workstation Design:** Professional dark/light-balanced scientific aesthetic using neutral charcoal (`#0e1117`, `#161b22`, `#21262d`), off-white typography (`#e6edf3`), muted forest green / olive accents (`#2ea043`, `#3fb950`), and subtle amber highlights (`#d29922`). Free of generic SaaS templates, neon glowing effects, and random emojis.
- **RDKit-Driven Chemistry Engine:** Pure, validated scientific calculations using RDKit's C++ bindings for 2D coordinate generation, distance geometry 3D conformers (ETKDGv3), force field energy minimization (MMFF94/UFF), SMARTS functional group queries, and 35+ physicochemical descriptors.
- **No Heavy External Databases:** Runs completely stateless and lightweight without requiring complex external database servers.

---

## 2. Preserved Application Modules

All 7 core modules from the original application are retained, enhanced, and redesigned:

| Module | Core Functionality Preserved & Upgraded |
| :--- | :--- |
| **🏠 Dashboard** | Academic workstation landing hub with learning goals, workflow guides, quick-access action tiles, and 1-click curated benchmark molecules (Ethanol, Benzene, Phenol, Acetic Acid, Aspirin, Caffeine, Glucose). |
| **📖 Theory** | Educational reference covering cheminformatics principles, SMILES grammar, valence bond theory (sigma and pi bonds, delocalized π-electrons), aromaticity, molecular descriptors, and 3D force fields. |
| **🧬 Molecular Visualization** | High-DPI 2D vector SVG rendering with atom index numbering toggle and SMARTS substructure highlighting; interactive 3D WebGL conformer viewer supporting 6 display representations (Ball & Stick, Stick, Space-Filling / CPK, Wireframe, Cartoon, and van der Waals surface) with zoom/rotate controls and element legend. |
| **📊 Molecular Properties Report** | RDKit descriptor calculation suite displaying stoichiometric formula, molecular weights, Canonical & Isomeric SMILES, LogP, TPSA, HBD, HBA, rotatable bonds, ring counts, fraction Csp3, valence bond counts (sigma, pi, total covalent bonds), SMARTS functional group summary table, downloadable CSV report, and single-molecule PDF export. |
| **📈 Structure–Property Analysis** | Multi-molecule candidate comparison studio with batch SMILES parsing, automated property extreme detection (highest MW, highest LogP, highest TPSA, highest Fsp3), interactive Plotly bar charts and bivariate scatter plots, and CSV export. |
| **📝 Assessment** | 12-question academic examination covering SMILES notation, molecular descriptors, bonding rules, and 3D modeling. Real-time scoring, percentage calculation, performance feedback, and detailed question-by-question scientific rationales revealed upon submission. |
| **📄 Final Project Report** | Student Name and Academic Registration ID integration, batch SMILES input validation, and automated publication-quality ReportLab PDF generation featuring 2D vector graphs, 3D ball-and-stick projections, complete descriptor tables with student-friendly interpretation columns, point-wise conclusions, and methodology notes. |

---

## 3. Added Scientific & Technical Upgrades

1. **Enhanced Molecular Information Panel:**
   - Displays stoichiometric Molecular Formula, Molecular Weight, Exact Molecular Weight, **Canonical SMILES**, **Isomeric SMILES**, LogP, TPSA, H-Bond Donors, H-Bond Acceptors, Rotatable Bonds, Ring Count, Aromatic Rings, and Fraction Csp3.
2. **SMARTS-Based Functional Group Identification:**
   - Automatically detects 16 common organic groups via RDKit SMARTS patterns: Alcohols, Phenols, Aldehydes, Ketones, Carboxylic Acids, Esters, Ethers, Primary Amines, Secondary Amines, Tertiary Amines, Amides, Nitriles, Nitro groups, Alkenes, Alkynes, Aromatic Rings, and Halides.
   - Highlights detected functional group substructures directly on the 2D diagram.
3. **Improved Molecule Comparison Studio:**
   - Allows comparing multiple molecules side by side with automated highlight of property extremes.
   - Generates interactive Plotly comparative bar charts and bivariate scatter plots with CSV download.
4. **Enhanced 2D and 3D Molecular Visualization:**
   - Crisp vector SVG rendering without pixelation.
   - Toggle atom index overlays directly on atoms.
   - 3Dmol.js WebGL rendering with conformer generation via ETKDGv3 and MMFF94/UFF energy minimization.
5. **Robust Error Handling:**
   - Clear, user-friendly validation messages for invalid SMILES, empty inputs, unparseable entries, and conformer generation warnings.

---

## 4. Repository Structure

```
Vetri chemtool/
├── backend/
│   ├── app.py                     # FastAPI application with REST endpoints
│   ├── requirements.txt           # Python dependencies (FastAPI, RDKit, ReportLab, etc.)
│   ├── core/
│   │   ├── chemistry.py           # RDKit engine (descriptors, bonding, SMARTS, 3D conformers)
│   │   ├── visualization.py       # RDKit 2D vector SVG rendering
│   │   └── reporting.py           # Publication-quality ReportLab PDF generation
│   └── tests/
│       └── test_api.py            # Automated FastAPI test suite (all 7 benchmark molecules)
│
├── frontend/
│   ├── index.html                 # Single-page HTML shell with 3Dmol.js and Plotly.js CDNs
│   ├── package.json               # Frontend dependencies (React, Vite, TypeScript, Lucide)
│   ├── vite.config.ts             # Vite build & local API proxy configuration
│   ├── tsconfig.json              # TypeScript strict configuration
│   ├── vercel.json                # Vercel deployment routing configuration
│   ├── .env.example               # Frontend environment variable configuration template
│   └── src/
│       ├── main.tsx               # React root entrypoint
│       ├── App.tsx                # Main layout and view routing
│       ├── api.ts                 # Type-safe API client for FastAPI backend
│       ├── types.ts               # Chemistry and API TypeScript interfaces
│       ├── index.css              # Global scientific workstation theme & CSS reset
│       ├── App.css                # Component-specific workstation styles
│       ├── components/
│       │   ├── Sidebar.tsx        # Workstation navigation and student info panel
│       │   ├── MoleculeViewer2D.tsx # Vector SVG diagram viewer with highlight toggles
│       │   └── MoleculeViewer3D.tsx # 3Dmol.js WebGL viewer with 6 representation styles
│       └── pages/
│           ├── DashboardPage.tsx  # Workstation landing dashboard & example loader
│           ├── TheoryPage.tsx     # Cheminformatics curriculum & bonding theory
│           ├── VisualizationPage.tsx # 2D/3D dual-viewport visualization studio
│           ├── PropertiesPage.tsx # Full descriptor table, valence accounting & PDF export
│           ├── ComparisonPage.tsx # Multi-molecule candidate comparison & Plotly charts
│           ├── AssessmentPage.tsx # 12-question quiz with score tracking & rationales
│           └── ReportPage.tsx     # Final project dossier PDF compiler
│
├── requirements.txt               # Root Python dependencies
├── reference_app.py               # Original reference code preserved for archival
└── README.md                      # Comprehensive project documentation
```

---

## 5. Vercel Deployment Configuration (Vercel Services)

The project is configured for deployment entirely on Vercel under a single deployment and domain using **Vercel Services**:

- **Unified Root `vercel.json`:** Defines multi-service orchestration with independent builds for `frontend` (Vite) and `backend` (FastAPI).
- **Internal Routing:** Incoming requests to `/api/(.*)` are transparently routed to the FastAPI backend service; all other routes fallback to the Vite React frontend.
- **Single Domain:** No CORS configuration or external backend URLs are required because frontend and backend share the same deployment origin.

### Deploying on Vercel:
1. Go to **[vercel.com/new](https://vercel.com/new)** and import `cheminformatics-virtual-lab`.
2. Vercel will detect the root `vercel.json` and select the **Services** preset.
3. Keep the Root Directory as the repository root (`./`).
4. Click **Deploy**. Both the Vite frontend and Python FastAPI backend will build and deploy under one single domain.

---

## 6. Installation & Local Execution

### Prerequisites
- Python 3.10+ (with pip)
- Node.js 18+ (with npm)

### 1. Setup and Start Backend (FastAPI + RDKit)

```bash
# From the project root, create and activate a virtual environment
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
# source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Start the FastAPI server on port 8000
python -m uvicorn app:app --app-dir backend --reload --port 8000
```
Backend API interactive documentation is available at `http://localhost:8000/docs`.

### 2. Setup and Start Frontend (React + Vite + TypeScript)

In a new terminal window:
```bash
cd frontend

# Install npm packages
npm install

# Start Vite development server
npm run dev
```
Open your browser to `http://localhost:5173`. The Vite dev server automatically proxies `/api/*` requests to `http://localhost:8000`.

### 3. Production Frontend Build

```bash
cd frontend
npm run build
```
The compiled production bundle is generated into `frontend/dist/`.

---

## 7. Automated Testing & Benchmark Verification

The backend includes a comprehensive automated test suite verifying all 7 benchmark molecules:

| Molecule | SMILES | Key Verified Properties |
| :--- | :--- | :--- |
| **Ethanol** | `CCO` | MW: 46.07 g/mol, Formula: C2H6O, LogP: -0.0014, Alcohol detected |
| **Benzene** | `c1ccccc1` | MW: 78.11 g/mol, Formula: C6H6, LogP: 1.6866, 6 Delocalized π-electrons |
| **Phenol** | `Oc1ccccc1` | MW: 94.11 g/mol, Formula: C6H6O, LogP: 1.3932, Phenol detected |
| **Acetic Acid** | `CC(=O)O` | MW: 60.05 g/mol, Formula: C2H4O2, LogP: 0.0909, Carboxylic acid detected |
| **Aspirin** | `CC(=O)Oc1ccccc1C(=O)O` | MW: 180.16 g/mol, Formula: C9H8O4, Carboxylic acid + Ester detected |
| **Caffeine** | `CN1C=NC2=C1C(=O)N(C(=O)N2C)C` | MW: 194.19 g/mol, Formula: C8H10N4O2, Purine xanthine core |
| **Glucose** | `OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O` | MW: 180.16 g/mol, Formula: C6H12O6, HBD: 5, HBA: 6, 5 chiral centers |

To run the automated tests:
```bash
python -m unittest backend/tests/test_api.py
```
**Test Results:** 7/7 tests passed in 0.78s covering molecule parsing, 2D vector SVG generation, 3D conformers, comparison analytics, academic assessment scoring, and ReportLab PDF compilation.
