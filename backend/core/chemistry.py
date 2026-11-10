"""
Cheminformatics Virtual Laboratory - Core Chemistry Engine
RDKit molecular processing, property calculations, conformer generation, and SMARTS detection.
"""

from typing import Optional, Dict, Any, List, Tuple
from rdkit import Chem
from rdkit.Chem import (
    Descriptors,
    Crippen,
    Lipinski,
    rdMolDescriptors,
    AllChem
)

# Reference example molecules
EXAMPLE_MOLECULES = {
    "Ethanol": "CCO",
    "Benzene": "c1ccccc1",
    "Phenol": "Oc1ccccc1",
    "Acetic Acid": "CC(=O)O",
    "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
    "Caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
    "Glucose": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"
}


# ==============================================================================
# MOLECULAR PARSING & VALIDATION
# ==============================================================================

def get_molecule(smiles: str) -> Tuple[Optional[Chem.Mol], Optional[str]]:
    """
    Parse a SMILES string into an RDKit Mol object with diagnostic error tracking.
    Returns (mol, error_message).
    """
    if not smiles or not smiles.strip():
        return None, "Please enter a valid SMILES notation (input is empty)."

    clean_smiles = smiles.strip().replace("“", '"').replace("”", '"').replace("–", "-")

    try:
        mol = Chem.MolFromSmiles(clean_smiles)
        if mol is None:
            # Check if failure is due to sanitization / valence
            raw_mol = Chem.MolFromSmiles(clean_smiles, sanitize=False)
            if raw_mol is not None:
                try:
                    Chem.SanitizeMol(raw_mol)
                except Exception as sanitize_err:
                    return None, f"Chemical valence or aromaticity error: {str(sanitize_err)}"
            return None, "Invalid SMILES notation. Please verify chemical syntax, element symbols, and ring closures."

        Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
        return mol, None

    except Exception as e:
        return None, f"Molecular parsing error: {str(e)}"


# ==============================================================================
# CHEMICAL BONDING & VALENCE ANALYSIS
# ==============================================================================

def calculate_bond_information(mol: Chem.Mol) -> Dict[str, Any]:
    """
    Calculate:
    - Heavy atom graph bonds
    - Sigma (σ) bonds (including bonds to implicit & explicit hydrogens)
    - Pi (π) bonds via Kekulé single/double/triple decomposition
    - Total bond order count (σ + π)
    - Aromatic ring bond and atom counts
    - Formal charge
    """
    if mol is None:
        return {}

    mol_copy = Chem.Mol(mol)
    heavy_atom_bonds = mol_copy.GetNumBonds()

    # Add implicit hydrogens. In any chemical graph, every bonded pair has exactly 1 σ bond.
    mol_with_h = Chem.AddHs(Chem.Mol(mol_copy))
    sigma_bonds = mol_with_h.GetNumBonds()

    # Kekulization assigns alternating localized single and double bonds to aromatic systems
    kekule_mol = Chem.Mol(mol_copy)
    pi_bonds = 0
    double_bonds = 0
    triple_bonds = 0

    try:
        Chem.Kekulize(kekule_mol, clearAromaticFlags=True)
        for bond in kekule_mol.GetBonds():
            btype = bond.GetBondType()
            if btype == Chem.BondType.DOUBLE:
                double_bonds += 1
                pi_bonds += 1
            elif btype == Chem.BondType.TRIPLE:
                triple_bonds += 1
                pi_bonds += 2
            elif btype == Chem.BondType.QUADRUPLE:
                pi_bonds += 3
    except Exception:
        # Fallback if kekulization cannot clear flags
        for bond in mol_copy.GetBonds():
            btype = bond.GetBondType()
            if btype == Chem.BondType.DOUBLE:
                double_bonds += 1
                pi_bonds += 1
            elif btype == Chem.BondType.TRIPLE:
                triple_bonds += 1
                pi_bonds += 2
            elif bond.GetIsAromatic():
                pi_bonds += 0.5

    total_bonds = sigma_bonds + int(round(pi_bonds))
    aromatic_atoms = sum(1 for a in mol_copy.GetAtoms() if a.GetIsAromatic())
    formal_charge = Chem.GetFormalCharge(mol_copy)

    return {
        "Heavy Atom Bonds": heavy_atom_bonds,
        "Sigma Bonds": sigma_bonds,
        "Pi Bonds": int(round(pi_bonds)),
        "Total Bonds": total_bonds,
        "Total Atoms Including H": mol_with_h.GetNumAtoms(),
        "Double Bonds": double_bonds,
        "Triple Bonds": triple_bonds,
        "Aromatic Atoms": aromatic_atoms,
        "Formal Charge": formal_charge
    }


# ==============================================================================
# COMPREHENSIVE MOLECULAR PROPERTIES
# ==============================================================================

def calculate_properties(mol: Chem.Mol) -> Dict[str, Any]:
    """Calculate complete molecular descriptors using RDKit."""
    if mol is None:
        return {}

    bond_info = calculate_bond_information(mol)
    formula = rdMolDescriptors.CalcMolFormula(mol)
    canonical_smiles = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=False)
    isomeric_smiles = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)

    properties = {
        "Molecular Formula": formula,
        "Molecular Weight": round(Descriptors.MolWt(mol), 3),
        "Exact Molecular Weight": round(Descriptors.ExactMolWt(mol), 4),
        "Canonical SMILES": canonical_smiles,
        "Isomeric SMILES": isomeric_smiles,
        "LogP": round(Crippen.MolLogP(mol), 3),
        "TPSA": round(rdMolDescriptors.CalcTPSA(mol), 3),
        "Hydrogen Bond Donors": Lipinski.NumHDonors(mol),
        "Hydrogen Bond Acceptors": Lipinski.NumHAcceptors(mol),
        "Rotatable Bonds": Lipinski.NumRotatableBonds(mol),
        "Ring Count": Lipinski.RingCount(mol),
        "Aromatic Rings": rdMolDescriptors.CalcNumAromaticRings(mol),
        "Aliphatic Rings": rdMolDescriptors.CalcNumAliphaticRings(mol),
        "Number of Atoms": mol.GetNumAtoms(),
        "Heavy Atoms": mol.GetNumHeavyAtoms(),
        "Heavy Atom Bonds": bond_info.get("Heavy Atom Bonds", 0),
        "Sigma (σ) Bonds": bond_info.get("Sigma Bonds", 0),
        "Pi (π) Bonds": bond_info.get("Pi Bonds", 0),
        "Total Bonds (σ + π)": bond_info.get("Total Bonds", 0),
        "Fraction Csp3": round(rdMolDescriptors.CalcFractionCSP3(mol), 3),
        "Molar Refractivity": round(Crippen.MolMR(mol), 3),
        "Formal Charge": bond_info.get("Formal Charge", 0)
    }

    return properties


# ==============================================================================
# 3D CONFORMER GENERATION
# ==============================================================================

def generate_3d_molecule(mol: Chem.Mol, random_seed: int = 42) -> Tuple[Optional[Chem.Mol], Optional[str]]:
    """
    Generate 3D coordinates using ETKDGv3 with MMFF94 optimization and UFF fallback.
    Returns (mol_3d, error_message).
    """
    if mol is None:
        return None, "Null molecule supplied."

    try:
        mol3d = Chem.AddHs(mol)
        params = AllChem.ETKDGv3()
        params.randomSeed = random_seed
        params.clearConfs = True
        params.enforceChirality = True

        status = AllChem.EmbedMolecule(mol3d, params)

        # Fallback 1: ETKDG with random coordinates
        if status != 0:
            params.useRandomCoords = True
            status = AllChem.EmbedMolecule(mol3d, params)

        # Fallback 2: Basic distance geometry
        if status != 0:
            status = AllChem.EmbedMolecule(mol3d, randomSeed=random_seed, useRandomCoords=True)

        if status != 0:
            return None, "Unable to generate 3D coordinates. Structure may be too strained or geometrically over-constrained."

        # Optimize geometry with force field
        try:
            if AllChem.MMFFHasAllMoleculeParams(mol3d):
                AllChem.MMFFOptimizeMolecule(mol3d, maxIters=1000)
            else:
                AllChem.UFFOptimizeMolecule(mol3d, maxIters=1000)
        except Exception:
            try:
                AllChem.UFFOptimizeMolecule(mol3d, maxIters=1000)
            except Exception:
                pass

        return mol3d, None

    except Exception as e:
        return None, f"3D Conformer generation error: {str(e)}"


# ==============================================================================
# FUNCTIONAL GROUP IDENTIFICATION (SMARTS)
# ==============================================================================

FUNCTIONAL_GROUP_SMARTS = [
    {
        "name": "Alcohol",
        "smarts": "[OX2H][CX4]",
        "desc": "Aliphatic hydroxyl group; participates in hydrogen bonding as donor and acceptor."
    },
    {
        "name": "Phenol",
        "smarts": "[OX2H]c",
        "desc": "Hydroxyl group directly bonded to an aromatic ring; weakly acidic."
    },
    {
        "name": "Aldehyde",
        "smarts": "[CX3H1](=O)[#6,#1]",
        "desc": "Carbonyl carbon bonded to at least one hydrogen atom."
    },
    {
        "name": "Ketone",
        "smarts": "[#6][CX3](=O)[#6]",
        "desc": "Carbonyl carbon bonded to two carbon substituents."
    },
    {
        "name": "Carboxylic Acid",
        "smarts": "[CX3](=O)[OX2H1]",
        "desc": "Acidic functional group capable of donating protons and forming H-bond dimers."
    },
    {
        "name": "Ester",
        "smarts": "[#6][CX3](=O)[OX2][#6]",
        "desc": "Carboxylic acid derivative commonly found in lipids, fragrances, and prodrugs."
    },
    {
        "name": "Ether",
        "smarts": "[OD2]([CX4])[CX4]",
        "desc": "Dialkyl oxygen linkage; acts as a weak hydrogen bond acceptor."
    },
    {
        "name": "Primary Amine",
        "smarts": "[NX3H2;!$(NC=O)][#6]",
        "desc": "Basic primary nitrogen with two attached hydrogens."
    },
    {
        "name": "Secondary Amine",
        "smarts": "[NX3H1;!$(NC=O)]([#6])[#6]",
        "desc": "Basic secondary nitrogen with one attached hydrogen."
    },
    {
        "name": "Tertiary Amine",
        "smarts": "[NX3H0;!$(NC=O)]([#6])([#6])[#6]",
        "desc": "Tertiary nitrogen with three carbon bonds; hydrogen bond acceptor only."
    },
    {
        "name": "Amide",
        "smarts": "[#7][#6](=[OX1])",
        "desc": "Nitrogen bonded to a carbonyl group; planar peptide linkage analog."
    },
    {
        "name": "Nitrile",
        "smarts": "[NX1]#[CX2]",
        "desc": "Linear sp-hybridized cyano group; strongly polar."
    },
    {
        "name": "Nitro",
        "smarts": "[$([NX3](=O)=O),$([NX3+](=O)[O-])]",
        "desc": "Strongly electron-withdrawing oxidized nitrogen moiety."
    },
    {
        "name": "Alkene",
        "smarts": "[CX3;$([C]=[C])]=[CX3;$([C]=[C])]",
        "desc": "Carbon-carbon double bond with restricted conformational rotation."
    },
    {
        "name": "Alkyne",
        "smarts": "[CX2]#[CX2]",
        "desc": "Rigid, linear carbon-carbon triple bond."
    },
    {
        "name": "Aromatic Ring",
        "smarts": "a1aaaaa1",
        "desc": "Planar cyclic system with delocalized pi-electrons obeying Hückel's 4n+2 rule."
    },
    {
        "name": "Halide",
        "smarts": "[F,Cl,Br,I]",
        "desc": "Halogen substituent (F, Cl, Br, I); modulates lipophilicity and metabolic stability."
    }
]


def identify_functional_groups(mol: Chem.Mol) -> List[Dict[str, Any]]:
    """
    Detect standard organic functional groups in a molecule using curated SMARTS.
    Returns a list of detected functional group dictionaries.
    """
    if mol is None:
        return []

    mol_copy = Chem.Mol(mol)
    detected = []

    for item in FUNCTIONAL_GROUP_SMARTS:
        name = item["name"]
        smarts = item["smarts"]
        desc = item["desc"]

        try:
            pattern = Chem.MolFromSmarts(smarts)
            if pattern is None:
                continue

            matches = mol_copy.GetSubstructMatches(pattern)
            if matches:
                # Deduplicate matches
                unique_matches = []
                for match in matches:
                    sorted_m = tuple(sorted(match))
                    if sorted_m not in unique_matches:
                        unique_matches.append(sorted_m)

                count = len(unique_matches)
                matched_atoms = list(set(idx for match in unique_matches for idx in match))

                detected.append({
                    "name": name,
                    "count": count,
                    "matched_atom_indices": matched_atoms,
                    "description": desc,
                    "smarts": smarts
                })

        except Exception:
            continue

    return detected


# ==============================================================================
# PROPERTY INTERPRETATION HELPERS
# ==============================================================================

def get_property_interpretation(property_name: str, value: Any, properties: Dict[str, Any]) -> str:
    """Return a student-friendly interpretation for each reported property."""
    if property_name == "Molecular Formula":
        return "Shows the stoichiometric elemental composition of the molecular structure."

    if property_name == "Molecular Weight":
        return "Represents average molecular mass. Governs diffusion, formulation, and permeability."

    if property_name == "Exact Molecular Weight":
        return "The monoisotopic mass calculated from exact isotopic masses; essential for mass spectrometry."

    if property_name in ("Canonical SMILES", "Isomeric SMILES"):
        return "Standardized 1D text representation of the molecular graph and stereochemical configuration."

    if property_name == "LogP":
        if isinstance(value, (int, float)):
            if value < 0:
                return "Negative value indicates preference for the aqueous phase and relatively high hydrophilicity."
            elif value < 1:
                return "Indicates low to moderate lipophilicity, suggesting preference for polar environments."
            elif value < 3:
                return "Indicates moderate lipophilicity, optimal for balanced oral bioavailability (0 to 3)."
            else:
                return "Indicates high lipophilicity and a stronger preference for hydrophobic environments."
        return "Octanol-water partition coefficient; measures relative lipophilicity."

    if property_name == "TPSA":
        if isinstance(value, (int, float)):
            if value < 60:
                return "Low polar surface area (<60 Å²), indicating high likelihood of membrane permeability."
            elif value <= 140:
                return "Moderate polar surface area (60 to 140 Å²), typical of orally absorbed small-molecule drugs."
            else:
                return "High polar surface area (>140 Å²), indicating strong hydration and limited cell permeability."
        return "Topological Polar Surface Area; sum of surfaces of polar atoms (oxygen, nitrogen, and attached hydrogens)."

    if property_name == "Hydrogen Bond Donors":
        return f"{value} donor site(s) (OH, NH) capable of donating hydrogen in intermolecular interactions (Lipinski limit <= 5)."

    if property_name == "Hydrogen Bond Acceptors":
        return f"{value} acceptor site(s) (O, N lone pairs) capable of accepting hydrogen bonds (Lipinski limit <= 10)."

    if property_name == "Rotatable Bonds":
        if value == 0:
            return "No freely rotatable bonds; indicates a rigid molecular framework."
        return f"{value} rotatable bond(s); reflects conformational flexibility (Veber limit <= 10 for oral bioavailability)."

    if property_name == "Ring Count":
        return f"{value} total ring(s); contributes to overall 3D shape and scaffold rigidity."

    if property_name == "Aromatic Rings":
        return f"{value} aromatic ring(s); provides planar delocalized π-electron systems and π-stacking capability."

    if property_name == "Aliphatic Rings":
        return f"{value} non-aromatic ring(s); imparts spatial cyclic structure without π-electron delocalization."

    if property_name == "Number of Atoms":
        return "Counts atoms explicitly present in the molecular graph."

    if property_name == "Heavy Atoms":
        return f"{value} non-hydrogen heavy atom(s); standard metric for molecular size."

    if property_name == "Heavy Atom Bonds":
        return f"{value} covalent bond(s) connecting non-hydrogen atoms in the molecular graph."

    if property_name == "Sigma (σ) Bonds":
        return f"{value} σ bond(s); every bonded pair contains one σ bond, including covalent bonds to hydrogen."

    if property_name == "Pi (π) Bonds":
        return f"{value} π bond(s); arises from multiple covalent bonds and aromatic ring systems."

    if property_name == "Total Bonds (σ + π)":
        return f"{value} total bond components obtained by summing calculated σ and π bond counts."

    if property_name == "Fraction Csp3":
        if isinstance(value, (int, float)):
            if value < 0.25:
                return f"Fsp3 = {value}: Low sp³ fraction; structure is predominantly planar, aromatic, or unsaturated."
            elif value <= 0.60:
                return f"Fsp3 = {value}: Intermediate sp³ fraction; balanced mix of saturated 3D and planar features."
            else:
                return f"Fsp3 = {value}: High sp³ fraction (>0.60); indicates a saturated, 3D molecular framework."
        return "Ratio of sp³ hybridized carbons to total carbons; measures 3D structural complexity."

    if property_name == "Molar Refractivity":
        return f"{value} cm³/mol; relates to molecular volume and electronic polarizability."

    return "Quantitative molecular descriptor calculated from the chemical structure."


def build_key_interpretation_points(properties: Dict[str, Any]) -> List[str]:
    """Create concise point-wise conclusions for reports."""
    points = []

    points.append(
        f"<b>• Molecular identity:</b> Formula <b>{properties['Molecular Formula']}</b>, "
        f"Molecular Weight <b>{properties['Molecular Weight']} g/mol</b>."
    )

    logp = properties["LogP"]
    if logp < 0:
        lip_desc = "hydrophilic"
    elif logp < 1:
        lip_desc = "low in lipophilicity"
    elif logp < 3:
        lip_desc = "moderately lipophilic (favorable oral profile)"
    else:
        lip_desc = "strongly lipophilic"

    points.append(
        f"<b>• Lipophilicity:</b> LogP = <b>{logp}</b> ({lip_desc}). "
        f"Reflects the balance between partition into non-polar and polar phases."
    )

    points.append(
        f"<b>• Molecular Polarity:</b> TPSA = <b>{properties['TPSA']} Å²</b>. "
        f"Measures the surface area contribution of polar heteroatoms."
    )

    points.append(
        f"<b>• Hydrogen Bonding:</b> Contains <b>{properties['Hydrogen Bond Donors']}</b> donor(s) "
        f"and <b>{properties['Hydrogen Bond Acceptors']}</b> acceptor(s)."
    )

    points.append(
        f"<b>• Conformational Flexibility:</b> <b>{properties['Rotatable Bonds']}</b> rotatable bond(s) "
        f"indicate structural flexibility."
    )

    points.append(
        f"<b>• Cyclic Architecture:</b> <b>{properties['Ring Count']}</b> ring(s), including "
        f"<b>{properties['Aromatic Rings']}</b> aromatic ring(s)."
    )

    points.append(
        f"<b>• Bonding Breakdown:</b> <b>{properties.get('Sigma (σ) Bonds', 0)}</b> σ bonds and "
        f"<b>{properties.get('Pi (π) Bonds', 0)}</b> π bonds."
    )

    points.append(
        f"<b>• Three-Dimensional Character:</b> Fraction Csp³ = <b>{properties['Fraction Csp3']}</b>, "
        f"characterizing the balance of saturated versus planar carbon atoms."
    )

    return points
