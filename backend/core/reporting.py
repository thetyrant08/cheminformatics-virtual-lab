"""
Cheminformatics Virtual Laboratory - PDF Report Engine
Generates publication-quality single and multi-molecule academic reports via ReportLab.
"""

import os
import tempfile
from io import BytesIO
from typing import Dict, Any, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from rdkit import Chem
from rdkit.Chem import Draw

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
    Preformatted
)
from reportlab.lib.units import inch

from core.chemistry import (
    generate_3d_molecule,
    get_property_interpretation,
    build_key_interpretation_points
)


def save_2d_structure_png(mol: Chem.Mol) -> str:
    """Create a temporary PNG of the 2D structure for PDF reports."""
    img = Draw.MolToImage(mol, size=(700, 500))
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp.close()
    img.save(tmp.name)
    return tmp.name


def save_3d_structure_png(mol: Chem.Mol) -> str:
    """Create a high-clarity ball-and-stick image for the PDF report."""
    mol3d, _ = generate_3d_molecule(mol)
    if mol3d is None:
        return None

    conf = mol3d.GetConformer()
    n_atoms = mol3d.GetNumAtoms()

    coords = np.array([
        [conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y, conf.GetAtomPosition(i).z]
        for i in range(n_atoms)
    ], dtype=float)

    centered = coords - coords.mean(axis=0)
    if n_atoms >= 3 and np.linalg.matrix_rank(centered) >= 2:
        _, _, vh = np.linalg.svd(centered, full_matrices=False)
        projected = centered @ vh[:2].T
    else:
        projected = centered[:, :2]

    cpk = {
        "H": "#FFFFFF", "C": "#3F3F3F", "N": "#2F5BFF",
        "O": "#E53935", "F": "#65C466", "P": "#F39C12",
        "S": "#F4D03F", "Cl": "#27AE60", "Br": "#8E3B2F",
        "I": "#8E44AD"
    }
    sizes = {
        "H": 70, "C": 240, "N": 270, "O": 285, "F": 260,
        "P": 300, "S": 310, "Cl": 310, "Br": 330, "I": 350
    }

    fig, ax = plt.subplots(figsize=(8.5, 6.0), facecolor="white")
    ax.set_facecolor("white")

    for bond in mol3d.GetBonds():
        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()
        x1, y1 = projected[i]
        x2, y2 = projected[j]
        dx, dy = x2 - x1, y2 - y1
        length = float(np.hypot(dx, dy))
        if length == 0:
            continue

        px, py = -dy / length, dx / length
        btype = bond.GetBondType()
        if btype == Chem.BondType.DOUBLE:
            offsets = (-0.035, 0.035)
        elif btype == Chem.BondType.TRIPLE:
            offsets = (-0.055, 0.0, 0.055)
        else:
            offsets = (0.0,)

        for off in offsets:
            ax.plot(
                [x1 + px * off, x2 + px * off],
                [y1 + py * off, y2 + py * off],
                color="#666666", linewidth=2.8,
                solid_capstyle="round", zorder=1
            )

    for i, atom in enumerate(mol3d.GetAtoms()):
        symbol = atom.GetSymbol()
        x, y = projected[i]
        ax.scatter(
            x, y,
            s=sizes.get(symbol, 250),
            c=cpk.get(symbol, "#A0A0A0"),
            edgecolors="#222222",
            linewidths=1.0,
            zorder=3
        )
        if symbol not in ("H", "C"):
            ax.text(
                x, y, symbol,
                ha="center", va="center",
                fontsize=8.5, fontweight="bold",
                color="white" if symbol in ("N", "Br", "I") else "black",
                zorder=4
            )

    xmin, ymin = projected.min(axis=0)
    xmax, ymax = projected.max(axis=0)
    width = max(xmax - xmin, 1.0)
    height = max(ymax - ymin, 1.0)
    pad = 0.22 * max(width, height)

    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title("3D Molecular Structure (Ball-and-Stick)", fontsize=16, fontweight="bold", pad=14, color="#17365D")

    fig.tight_layout(pad=1.0)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp.close()
    fig.savefig(tmp.name, dpi=300, bbox_inches="tight", facecolor="white", pad_inches=0.1)
    plt.close(fig)
    return tmp.name


def generate_molecule_pdf(input_smiles: str, mol: Chem.Mol, properties: Dict[str, Any]) -> bytes:
    """Generate a single-molecule properties report PDF (original format enhanced)."""
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=45, rightMargin=45, topMargin=45, bottomMargin=45
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"], fontSize=20, alignment=TA_CENTER, textColor=HexColor("#17365D")
    )
    heading_style = ParagraphStyle(
        "HeadingStyle", parent=styles["Heading1"], fontSize=13, textColor=HexColor("#17365D"), spaceBefore=8, spaceAfter=6
    )
    body_style = ParagraphStyle(
        "BodyStyle", parent=styles["BodyText"], fontSize=9.5, leading=14, alignment=TA_JUSTIFY
    )
    small_style = ParagraphStyle(
        "SmallText", parent=styles["BodyText"], fontSize=8, leading=10
    )

    story = [
        Paragraph("CHEMINFORMATICS VIRTUAL LABORATORY", title_style),
        Spacer(1, 0.08 * inch),
        Paragraph("MOLECULAR PROPERTIES REPORT", ParagraphStyle("Sub", parent=title_style, fontSize=14, textColor=HexColor("#2EA043"))),
        Spacer(1, 0.25 * inch),
        Paragraph("1. Molecular Information", heading_style)
    ]

    canonical_smiles = Chem.MolToSmiles(mol, canonical=True)
    basic_data = [
        ["Property", "Value"],
        ["Input SMILES", input_smiles],
        ["Canonical SMILES", canonical_smiles],
        ["Molecular Formula", properties.get("Molecular Formula", "N/A")],
        ["Molecular Weight", f"{properties.get('Molecular Weight', 'N/A')} g/mol"]
    ]
    basic_table = Table(basic_data, colWidths=[2.2 * inch, 4.4 * inch])
    basic_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 6)
    ]))
    story += [basic_table, Spacer(1, 0.25 * inch)]

    story.append(Paragraph("2. Molecular Properties Table", heading_style))
    property_data = [["Property", "Value"]]
    for key, value in properties.items():
        property_data.append([str(key), str(value)])

    property_table = Table(property_data, colWidths=[3.3 * inch, 3.3 * inch], repeatRows=1)
    property_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2F5597")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 4)
    ]))
    story += [property_table, Spacer(1, 0.25 * inch)]

    story.append(Paragraph("3. Interpretation & Methodology", heading_style))
    interpretation = """
    This report was generated using the Cheminformatics Virtual Laboratory. 
    The molecular properties were calculated from the chemical structure represented by the 
    submitted SMILES notation using the RDKit cheminformatics toolkit. Calculated descriptors are 
    computational estimates useful for comparative cheminformatics analysis and structure-property relationships.
    """
    story.append(Paragraph(interpretation, body_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def generate_multi_final_report(
    student_name: str,
    registration_number: str,
    molecule_records: List[Tuple[str, Chem.Mol, Dict[str, Any]]]
) -> bytes:
    """Generate the complete student molecular analysis report (single or multiple molecules)."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=38, rightMargin=38, topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ProjectTitle", parent=styles["Title"], fontSize=18, leading=22, alignment=TA_CENTER, textColor=HexColor("#17365D")
    )
    heading_style = ParagraphStyle(
        "ProjectHeading", parent=styles["Heading1"], fontSize=12, leading=16, textColor=HexColor("#17365D"), spaceBefore=8, spaceAfter=6
    )
    body_style = ParagraphStyle(
        "ProjectBody", parent=styles["BodyText"], fontSize=9, leading=13, alignment=TA_JUSTIFY
    )
    small_style = ParagraphStyle(
        "SmallTableText", parent=styles["BodyText"], fontSize=7.5, leading=9.5
    )
    header_style = ParagraphStyle(
        "HeaderTableText", parent=styles["BodyText"], fontSize=8, leading=9.5, textColor=colors.white, alignment=TA_CENTER
    )

    story = [
        Paragraph("CHEMINFORMATICS VIRTUAL LABORATORY", title_style),
        Spacer(1, 0.05 * inch),
        Paragraph("STUDENT MOLECULAR ANALYSIS REPORT", ParagraphStyle("Sub", parent=title_style, fontSize=13, textColor=HexColor("#2EA043"))),
        Spacer(1, 0.12 * inch),
        Paragraph(
            f"<b>Student Name:</b> {student_name or 'Not provided'} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Registration Number:</b> {registration_number or 'Not provided'} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b>Molecules Analyzed:</b> {len(molecule_records)}",
            body_style
        ),
        Spacer(1, 0.15 * inch)
    ]

    temp_images = []

    for index, record in enumerate(molecule_records, start=1):
        input_smiles, mol, properties = record
        if index > 1:
            story.append(PageBreak())

        story.append(Paragraph(f"Molecule {index} of {len(molecule_records)}: Molecular Information", heading_style))

        basic_data = [
            ["Input SMILES", input_smiles],
            ["Canonical SMILES", Chem.MolToSmiles(mol, canonical=True)],
            ["Molecular Formula", properties.get("Molecular Formula", "N/A")],
            ["Molecular Weight", f"{properties.get('Molecular Weight', 'N/A')} g/mol"]
        ]
        basic_table = Table(basic_data, colWidths=[1.8 * inch, 4.9 * inch])
        basic_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, HexColor("#CBD5E1")),
            ("BACKGROUND", (0, 0), (0, -1), HexColor("#F1F5F9")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 4)
        ]))
        story += [basic_table, Spacer(1, 0.12 * inch)]

        # Molecular Structures (2D and 3D)
        story.append(Paragraph("Molecular Structures", heading_style))
        img2d = save_2d_structure_png(mol)
        img3d = save_3d_structure_png(mol)
        if img2d: temp_images.append(img2d)
        if img3d: temp_images.append(img3d)

        if img2d and img3d:
            structure_table = Table([[
                Image(img2d, width=3.15 * inch, height=2.15 * inch),
                Image(img3d, width=3.15 * inch, height=2.15 * inch)
            ]], colWidths=[3.35 * inch, 3.35 * inch])
            structure_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#CBD5E1"))
            ]))
            story += [
                structure_table,
                Spacer(1, 0.05 * inch),
                Paragraph(
                    "<b>Figure 1.</b> Left: 2D molecular connectivity. "
                    "Right: Generated 3D ball-and-stick geometry showing the spatial arrangement of atoms.",
                    body_style
                ),
                Spacer(1, 0.12 * inch)
            ]
        elif img2d:
            story += [Image(img2d, width=5.0 * inch, height=3.5 * inch), Spacer(1, 0.12 * inch)]

        # Complete Properties with Interpretation Column
        story.append(Paragraph("Complete Molecular Properties and Interpretation", heading_style))
        prop_data = [[
            Paragraph("<b>Property</b>", header_style),
            Paragraph("<b>Value</b>", header_style),
            Paragraph("<b>Interpretation</b>", header_style)
        ]]

        for key, value in properties.items():
            interp = get_property_interpretation(key, value, properties)
            prop_data.append([
                Paragraph(str(key), small_style),
                Paragraph(str(value), small_style),
                Paragraph(interp, small_style)
            ])

        property_table = Table(prop_data, colWidths=[1.8 * inch, 1.0 * inch, 3.9 * inch], repeatRows=1)
        property_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2F5597")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#CBD5E1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 3.5)
        ]))
        story += [property_table, Spacer(1, 0.12 * inch)]

        # Point-wise Interpretation
        story.append(Paragraph("Point-wise Molecular Interpretation", heading_style))
        for point in build_key_interpretation_points(properties):
            story.append(Paragraph(point, body_style))
            story.append(Spacer(1, 0.04 * inch))

    # Educational notes and library section
    story.append(PageBreak())
    story += [
        Paragraph("Python Libraries Used and Their Importance", heading_style),
        Paragraph(
            "The virtual laboratory uses the following libraries to process "
            "molecular structures, calculate descriptors, display results and create this report:",
            body_style
        ),
        Spacer(1, 0.06 * inch)
    ]

    library_rows = [
        [Paragraph("<b>Library</b>", header_style), Paragraph("<b>Role in Project</b>", header_style)],
        [Paragraph("Streamlit", small_style), Paragraph("Interactive web application framework, navigation, inputs, and controls.", small_style)],
        [Paragraph("RDKit", small_style), Paragraph("SMILES parsing, 2D/3D structure generation, valence analysis, SMARTS, and descriptor calculation.", small_style)],
        [Paragraph("py3Dmol", small_style), Paragraph("Interactive WebGL 3D molecular visualization in the web browser.", small_style)],
        [Paragraph("Pandas", small_style), Paragraph("Data organization and CSV export.", small_style)],
        [Paragraph("ReportLab", small_style), Paragraph("Publication-quality PDF report generation with tables and figures.", small_style)],
        [Paragraph("Matplotlib & NumPy", small_style), Paragraph("Coordinate projection and depth-shaded 3D ball-and-stick rendering for PDF reports.", small_style)]
    ]
    library_table = Table(library_rows, colWidths=[1.8 * inch, 4.9 * inch], repeatRows=1)
    library_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2F5597")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.35, HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 4)
    ]))
    story += [library_table, Spacer(1, 0.15 * inch)]

    # Educational Code Snippet
    story.append(Paragraph("Illustrative Python Code: SMILES to Molecular Properties", heading_style))
    code_style = ParagraphStyle(
        "CodeStyle", parent=styles["Code"],
        fontName="Courier", fontSize=7, leading=8.5, leftIndent=5, rightIndent=5
    )
    educational_code = (
        "from rdkit import Chem\n"
        "from rdkit.Chem import Descriptors, Crippen, Lipinski, rdMolDescriptors, AllChem\n\n"
        "# 1. Parse SMILES notation\n"
        "smiles = 'CCO'  # Ethanol\n"
        "mol = Chem.MolFromSmiles(smiles)\n\n"
        "# 2. Calculate descriptors\n"
        "formula = rdMolDescriptors.CalcMolFormula(mol)\n"
        "mw = Descriptors.MolWt(mol)\n"
        "logp = Crippen.MolLogP(mol)\n"
        "tpsa = rdMolDescriptors.CalcTPSA(mol)\n"
        "hbd = Lipinski.NumHDonors(mol)\n\n"
        "# 3. 3D Conformer generation\n"
        "mol_3d = Chem.AddHs(mol)\n"
        "AllChem.EmbedMolecule(mol_3d, AllChem.ETKDGv3())\n"
        "AllChem.MMFFOptimizeMolecule(mol_3d)\n"
    )
    story.append(Preformatted(educational_code, code_style))

    try:
        doc.build(story)
        return buffer.getvalue()
    finally:
        buffer.close()
        for p in temp_images:
            if p and os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass
