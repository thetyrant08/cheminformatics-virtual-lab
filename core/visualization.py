"""
Cheminformatics Virtual Laboratory - Visualization Engine
High-DPI 2D molecular rendering and interactive WebGL 3D py3Dmol display.
"""

from io import BytesIO
from typing import Optional, List
from PIL import Image
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
import py3Dmol
import streamlit.components.v1 as components


def generate_2d_image(
    mol: Chem.Mol,
    size: tuple = (700, 500),
    show_atom_numbers: bool = False,
    highlight_atoms: Optional[List[int]] = None
) -> Image.Image:
    """
    Generate high-clarity 2D molecular structure diagram.
    Preserves original function signature while adding atom numbering and highlight support.
    """
    if mol is None:
        return Image.new("RGBA", size, (255, 255, 255, 0))

    mol_copy = Chem.Mol(mol)

    if show_atom_numbers:
        for atom in mol_copy.GetAtoms():
            atom.SetProp("atomLabel", f"{atom.GetSymbol()}_{atom.GetIdx()}")

    drawer = rdMolDraw2D.MolDraw2DCairo(size[0], size[1])
    opts = drawer.drawOptions()
    opts.padding = 0.08
    opts.bondLineWidth = 2.2
    opts.setBackgroundColour((1.0, 1.0, 1.0, 1.0))

    atom_colors = {}
    if highlight_atoms:
        for idx in highlight_atoms:
            atom_colors[idx] = (0.2, 0.65, 0.3) # Muted scientific green

    drawer.DrawMolecule(
        mol_copy,
        highlightAtoms=highlight_atoms or [],
        highlightAtomColors=atom_colors
    )
    drawer.FinishDrawing()
    png_bytes = drawer.GetDrawingText()
    return Image.open(BytesIO(png_bytes))


def generate_2d_svg(
    mol: Chem.Mol,
    size: tuple = (700, 500),
    show_atom_numbers: bool = False,
    highlight_atoms: Optional[List[int]] = None
) -> str:
    """Generate vector SVG representation of the molecular structure."""
    if mol is None:
        return ""

    mol_copy = Chem.Mol(mol)
    if show_atom_numbers:
        for atom in mol_copy.GetAtoms():
            atom.SetProp("atomLabel", f"{atom.GetSymbol()}_{atom.GetIdx()}")

    drawer = rdMolDraw2D.MolDraw2DSVG(size[0], size[1])
    opts = drawer.drawOptions()
    opts.padding = 0.08
    opts.bondLineWidth = 2.2

    atom_colors = {}
    if highlight_atoms:
        for idx in highlight_atoms:
            atom_colors[idx] = (0.2, 0.65, 0.3)

    drawer.DrawMolecule(
        mol_copy,
        highlightAtoms=highlight_atoms or [],
        highlightAtomColors=atom_colors
    )
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def display_3d_structure(
    mol3d: Chem.Mol,
    style: str = "Ball and Stick",
    show_surface: bool = False,
    width: int = 900,
    height: int = 600
):
    """
    Render interactive 3D WebGL molecular model using py3Dmol.
    Preserves original styles: Ball and Stick, Stick, Space Filling, Wireframe, Cartoon.
    """
    if mol3d is None:
        components.html(
            "<div style='text-align:center; color:#888; padding:40px;'>3D Conformer not available.</div>",
            height=height
        )
        return

    mol_block = Chem.MolToMolBlock(mol3d)
    view = py3Dmol.view(width=width, height=height)
    view.addModel(mol_block, "mol")

    if style == "Ball and Stick":
        view.setStyle({
            "stick": {"radius": 0.16},
            "sphere": {"scale": 0.30}
        })
    elif style == "Stick":
        view.setStyle({
            "stick": {"radius": 0.22}
        })
    elif style == "Space Filling":
        view.setStyle({
            "sphere": {"scale": 1.0}
        })
    elif style == "Wireframe":
        view.setStyle({
            "line": {"linewidth": 2.2}
        })
    elif style == "Cartoon":
        view.setStyle({
            "stick": {"radius": 0.10},
            "sphere": {"scale": 0.20}
        })
    else:
        view.setStyle({
            "stick": {"radius": 0.16},
            "sphere": {"scale": 0.30}
        })

    if show_surface:
        view.addSurface(
            py3Dmol.VDW,
            {"opacity": 0.7, "color": "white"}
        )

    view.setBackgroundColor("white")
    view.zoomTo()

    html = view._make_html()
    components.html(html, height=height + 20)
