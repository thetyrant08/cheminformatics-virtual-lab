"""
Cheminformatics Virtual Laboratory - FastAPI Backend Application
High-performance computational chemistry API powered by RDKit, NumPy, Pandas, and ReportLab.
"""

import sys
import os
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from io import BytesIO
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from rdkit import Chem

from core.chemistry import (
    EXAMPLE_MOLECULES,
    get_molecule,
    calculate_bond_information,
    calculate_properties,
    generate_3d_molecule,
    identify_functional_groups,
    get_property_interpretation,
    build_key_interpretation_points
)
from core.visualization import generate_2d_svg
from core.reporting import generate_molecule_pdf, generate_multi_final_report

app = FastAPI(
    title="Cheminformatics Virtual Laboratory API",
    description="Scientific API for molecular properties, 2D/3D visualization, and academic reporting",
    version="2.0.0"
)

# Enable CORS for Vite frontend and local/production deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()


# ==============================================================================
# PYDANTIC DATA MODELS
# ==============================================================================

class MoleculeRequest(BaseModel):
    smiles: str
    show_atom_numbers: bool = False
    highlight_atoms: Optional[List[int]] = None
    highlight_fg: bool = False


class MoleculeItem(BaseModel):
    name: str
    smiles: str


class CompareRequest(BaseModel):
    molecules: List[MoleculeItem]


class SingleReportRequest(BaseModel):
    smiles: str
    student_name: str = ""
    registration_number: str = ""


class MultiReportRequest(BaseModel):
    student_name: str = ""
    registration_number: str = ""
    smiles_list: List[str]


class AssessmentSubmitRequest(BaseModel):
    answers: List[Optional[str]]
    student_name: str = ""
    registration_number: str = ""


# ==============================================================================
# API ENDPOINTS (ROUTER)
# ==============================================================================

@router.get("/health")
def health_check():
    """Health check endpoint and library versions."""
    import rdkit
    return {
        "status": "healthy",
        "service": "Cheminformatics Virtual Laboratory Backend",
        "rdkit_version": rdkit.__version__
    }


@router.get("/examples")
def get_example_molecules():
    """Return dictionary of reference example molecules."""
    return {"examples": EXAMPLE_MOLECULES}


@router.post("/molecule/info")
def get_molecule_info(req: MoleculeRequest):
    """
    Complete structural characterization endpoint:
    Parses SMILES, calculates 35+ descriptors, identifies functional groups,
    generates 2D vector SVG, and creates 3D conformer coordinates in MDL Molblock format.
    """
    mol, err = get_molecule(req.smiles)
    if err or mol is None:
        raise HTTPException(status_code=400, detail=err or "Invalid SMILES notation.")

    # 1. Properties
    properties = calculate_properties(mol)
    bond_info = calculate_bond_information(mol)

    # 2. Functional groups
    functional_groups = identify_functional_groups(mol)
    fg_atom_indices = list(set(idx for g in functional_groups for idx in g["matched_atom_indices"]))

    # Determine highlight atoms
    highlight_list = []
    if req.highlight_atoms is not None:
        highlight_list = req.highlight_atoms
    elif req.highlight_fg:
        highlight_list = fg_atom_indices

    # 3. 2D Vector SVG
    svg_2d = generate_2d_svg(
        mol,
        size=(650, 420),
        show_atom_numbers=req.show_atom_numbers,
        highlight_atoms=highlight_list
    )

    # 4. 3D Conformer coordinates
    mol3d, conf_err = generate_3d_molecule(mol)
    mol_block_3d = Chem.MolToMolBlock(mol3d) if mol3d is not None else ""

    # 5. Point-wise pedagogical interpretations
    interpretations = {
        key: get_property_interpretation(key, val, properties)
        for key, val in properties.items()
    }
    key_points = build_key_interpretation_points(properties)

    return {
        "smiles": req.smiles,
        "valid": True,
        "properties": properties,
        "bond_info": bond_info,
        "functional_groups": functional_groups,
        "fg_atom_indices": fg_atom_indices,
        "svg_2d": svg_2d,
        "mol_block_3d": mol_block_3d,
        "conformer_error": conf_err,
        "interpretations": interpretations,
        "key_interpretation_points": key_points
    }


@router.post("/molecule/2d-svg")
def get_molecule_svg(req: MoleculeRequest):
    """Generate 2D SVG with customizable atom numbering and highlight atoms."""
    mol, err = get_molecule(req.smiles)
    if err or mol is None:
        raise HTTPException(status_code=400, detail=err or "Invalid SMILES notation.")

    svg_2d = generate_2d_svg(
        mol,
        size=(650, 420),
        show_atom_numbers=req.show_atom_numbers,
        highlight_atoms=req.highlight_atoms
    )
    return Response(content=svg_2d, media_type="image/svg+xml")


@router.post("/compare")
def compare_molecules(req: CompareRequest):
    """
    Compare multiple molecules side by side:
    Computes descriptors, highlights property extremes, and formats data for charts.
    """
    if not req.molecules:
        raise HTTPException(status_code=400, detail="No candidate molecules provided.")

    records = []
    skipped = []

    for item in req.molecules:
        m, err = get_molecule(item.smiles)
        if m:
            props = calculate_properties(m)
            records.append({
                "name": item.name,
                "smiles": item.smiles,
                "formula": props["Molecular Formula"],
                "mw": props["Molecular Weight"],
                "logp": props["LogP"],
                "tpsa": props["TPSA"],
                "hbd": props["Hydrogen Bond Donors"],
                "hba": props["Hydrogen Bond Acceptors"],
                "rotatable_bonds": props["Rotatable Bonds"],
                "ring_count": props["Ring Count"],
                "aromatic_rings": props["Aromatic Rings"],
                "fraction_csp3": props["Fraction Csp3"],
                "heavy_atoms": props["Heavy Atoms"]
            })
        else:
            skipped.append({"name": item.name, "smiles": item.smiles, "error": err})

    if not records:
        raise HTTPException(status_code=400, detail="All submitted SMILES were invalid.")

    # Calculate extremes
    highest_mw = max(records, key=lambda x: x["mw"])
    highest_logp = max(records, key=lambda x: x["logp"])
    highest_tpsa = max(records, key=lambda x: x["tpsa"])
    highest_fsp3 = max(records, key=lambda x: x["fraction_csp3"])

    return {
        "records": records,
        "skipped": skipped,
        "extremes": {
            "highest_mw": {"name": highest_mw["name"], "value": highest_mw["mw"]},
            "highest_logp": {"name": highest_logp["name"], "value": highest_logp["logp"]},
            "highest_tpsa": {"name": highest_tpsa["name"], "value": highest_tpsa["tpsa"]},
            "highest_fsp3": {"name": highest_fsp3["name"], "value": highest_fsp3["fraction_csp3"]}
        }
    }


@router.post("/export/pdf/single")
def export_single_pdf(req: SingleReportRequest):
    """Generate and return single-molecule ReportLab PDF report."""
    mol, err = get_molecule(req.smiles)
    if err or mol is None:
        raise HTTPException(status_code=400, detail=err or "Invalid SMILES notation.")

    properties = calculate_properties(mol)
    pdf_bytes = generate_molecule_pdf(req.smiles, mol, properties)

    formula = properties.get("Molecular Formula", "Molecule")
    filename = f"{formula}_Properties_Report.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.post("/export/pdf/multi")
def export_multi_pdf(req: MultiReportRequest):
    """Generate and return multi-molecule ReportLab student analysis PDF report."""
    if not req.smiles_list:
        raise HTTPException(status_code=400, detail="Empty SMILES list provided.")

    records = []
    for smi in req.smiles_list:
        smi_clean = smi.strip()
        if not smi_clean:
            continue
        mol, _ = get_molecule(smi_clean)
        if mol:
            props = calculate_properties(mol)
            records.append((smi_clean, mol, props))

    if not records:
        raise HTTPException(status_code=400, detail="No valid molecules found in the list.")

    pdf_bytes = generate_multi_final_report(
        req.student_name,
        req.registration_number,
        records
    )

    filename = "Cheminformatics_Final_Student_Report.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# ==============================================================================
# ASSESSMENT MODULE
# ==============================================================================

ASSESSMENT_QUESTIONS = [
    {
        "id": 1,
        "question": "1. What is the full expansion of the acronym SMILES?",
        "options": [
            "Simplified Molecular Input Line Entry System",
            "Standard Molecular Information Language Encoding System",
            "Simple Molecular Identification and Labeling System"
        ],
        "answer": "Simplified Molecular Input Line Entry System",
        "explanation": "SMILES stands for Simplified Molecular Input Line Entry System, introduced by Arthur Weininger in 1988."
    },
    {
        "id": 2,
        "question": "2. What does a SMILES string represent?",
        "options": [
            "A molecular structure using a text string",
            "A spectroscopy technique",
            "A laboratory analytical instrument"
        ],
        "answer": "A molecular structure using a text string",
        "explanation": "SMILES uses compact alphanumeric characters to specify molecular connectivity and stereochemistry."
    },
    {
        "id": 3,
        "question": "3. Which SMILES notation represents ethanol?",
        "options": ["CCO", "c1ccccc1", "CC(=O)O"],
        "answer": "CCO",
        "explanation": "CCO denotes two connected carbon atoms followed by a hydroxyl oxygen (CH3-CH2-OH)."
    },
    {
        "id": 4,
        "question": "4. Which SMILES notation represents benzene?",
        "options": ["c1ccccc1", "CCO", "O=C=O"],
        "answer": "c1ccccc1",
        "explanation": "c1ccccc1 denotes a 6-membered aromatic ring with opening and closing ring tag 1."
    },
    {
        "id": 5,
        "question": "5. In SMILES, parentheses '( )' are mainly used to indicate:",
        "options": ["Branches", "Molecular weight", "Atom colour"],
        "answer": "Branches",
        "explanation": "Parentheses enclose side-chain branches attached to the preceding atom, such as in CC(=O)O."
    },
    {
        "id": 6,
        "question": "6. Which descriptor is commonly associated with molecular lipophilicity?",
        "options": ["LogP", "TPSA", "HBD"],
        "answer": "LogP",
        "explanation": "LogP quantifies differential partition between 1-octanol and water, reflecting lipophilicity."
    },
    {
        "id": 7,
        "question": "7. What does TPSA describe?",
        "options": [
            "Topological Polar Surface Area",
            "Total Pi Surface Area",
            "Thermal Property Surface Analysis"
        ],
        "answer": "Topological Polar Surface Area",
        "explanation": "TPSA estimates the surface area contributed by polar atoms (O, N, and attached hydrogens)."
    },
    {
        "id": 8,
        "question": "8. What does HBA stand for in Lipinski's Rule of Five?",
        "options": ["Hydrogen Bond Acceptor", "Heavy Bond Atom", "Hydrogen Bond Analysis"],
        "answer": "Hydrogen Bond Acceptor",
        "explanation": "HBA stands for Hydrogen Bond Acceptor (typically nitrogen and oxygen lone pairs)."
    },
    {
        "id": 9,
        "question": "9. What does HBD stand for in Lipinski's Rule of Five?",
        "options": ["Hydrogen Bond Donor", "Heavy Bond Descriptor", "Hydrogen Bond Distance"],
        "answer": "Hydrogen Bond Donor",
        "explanation": "HBD stands for Hydrogen Bond Donor (typically OH and NH groups)."
    },
    {
        "id": 10,
        "question": "10. In chemical bonding, how many pi (π) bonds exist in a double bond?",
        "options": ["1", "2", "0"],
        "answer": "1",
        "explanation": "A standard covalent double bond consists of 1 sigma (σ) bond and 1 pi (π) bond."
    },
    {
        "id": 11,
        "question": "11. How many pi (π) bonds are present in a triple bond?",
        "options": ["2", "1", "3"],
        "answer": "2",
        "explanation": "A covalent triple bond consists of 1 sigma (σ) bond and 2 orthogonal pi (π) bonds."
    },
    {
        "id": 12,
        "question": "12. Which molecular model is useful for visualizing approximate van der Waals steric volume?",
        "options": ["Space Filling", "Wireframe only", "Text SMILES"],
        "answer": "Space Filling",
        "explanation": "Space Filling (CPK) models scale spheres to van der Waals radii to represent steric volume."
    }
]


@router.get("/assessment/questions")
def get_assessment_questions():
    """Return the assessment questions list (without answers)."""
    public_questions = [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in ASSESSMENT_QUESTIONS
    ]
    return {"questions": public_questions}


@router.post("/assessment/submit")
def submit_assessment(req: AssessmentSubmitRequest):
    """
    Score the assessment submission and return the score, percentage,
    performance feedback, and complete rationales for every question.
    """
    if len(req.answers) != len(ASSESSMENT_QUESTIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Expected {len(ASSESSMENT_QUESTIONS)} answers, received {len(req.answers)}"
        )

    score = 0
    feedback_details = []

    for i, q in enumerate(ASSESSMENT_QUESTIONS):
        student_ans = req.answers[i]
        is_correct = (student_ans == q["answer"])
        if is_correct:
            score += 1

        feedback_details.append({
            "id": q["id"],
            "question": q["question"],
            "student_answer": student_ans,
            "correct_answer": q["answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

    percentage = round((score / len(ASSESSMENT_QUESTIONS)) * 100, 1)

    if percentage >= 80:
        performance = "Excellent performance! Strong understanding of cheminformatics principles."
    elif percentage >= 50:
        performance = "Good performance! Review areas of uncertainty to strengthen concepts."
    else:
        performance = "Review recommended. Please revisit the Theory section."

    return {
        "student_name": req.student_name,
        "registration_number": req.registration_number,
        "score": score,
        "total": len(ASSESSMENT_QUESTIONS),
        "percentage": percentage,
        "performance": performance,
        "details": feedback_details
    }


# Include router with and without /api prefix for universal routing
app.include_router(router, prefix="/api")
app.include_router(router)


@app.get("/")
def root():
    """Service status and discovery endpoint."""
    return {
        "service": "Cheminformatics Virtual Laboratory API",
        "status": "online",
        "version": "2.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
