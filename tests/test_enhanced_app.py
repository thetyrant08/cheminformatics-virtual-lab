"""
Cheminformatics Virtual Laboratory - Automated Test Suite
Validates enhanced scientific calculations and core workflows across the 7 required test molecules:
Ethanol, Benzene, Phenol, Acetic acid, Aspirin, Caffeine, Glucose.
"""

import unittest
import os
import sys

# Ensure root directory is on import path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.chemistry import (
    EXAMPLE_MOLECULES,
    get_molecule,
    calculate_bond_information,
    calculate_properties,
    generate_3d_molecule,
    identify_functional_groups
)
from core.visualization import (
    generate_2d_image,
    generate_2d_svg
)
from core.reporting import (
    generate_molecule_pdf,
    generate_multi_final_report
)


class TestEnhancedVirtualLab(unittest.TestCase):
    """Test verification suite covering all 7 benchmark molecules."""

    REQUIRED_MOLECULES = {
        "Ethanol": "CCO",
        "Benzene": "c1ccccc1",
        "Phenol": "Oc1ccccc1",
        "Acetic acid": "CC(=O)O",
        "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
        "Caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
        "Glucose": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"
    }

    def test_smiles_validation_required_molecules(self):
        """Verify all 7 benchmark molecules parse and validate successfully."""
        for name, smi in self.REQUIRED_MOLECULES.items():
            mol, err = get_molecule(smi)
            self.assertIsNotNone(mol, f"Failed to parse {name} ({smi}): {err}")
            self.assertIsNone(err)

    def test_smiles_validation_invalid_cases(self):
        """Verify unparseable and empty inputs return friendly error messages without throwing."""
        empty_mol, empty_err = get_molecule("")
        self.assertIsNone(empty_mol)
        self.assertIn("empty", empty_err.lower())

        inv_mol, inv_err = get_molecule("C1CC(InvalidSyntax)===")
        self.assertIsNone(inv_mol)
        self.assertIsNotNone(inv_err)

    def test_molecular_descriptors_calculation(self):
        """Verify descriptor calculation for all 7 molecules."""
        for name, smi in self.REQUIRED_MOLECULES.items():
            mol, _ = get_molecule(smi)
            props = calculate_properties(mol)

            # Check that required properties exist and are non-null
            self.assertIn("Molecular Formula", props)
            self.assertIn("Molecular Weight", props)
            self.assertIn("Canonical SMILES", props)
            self.assertIn("Isomeric SMILES", props)
            self.assertIn("LogP", props)
            self.assertIn("TPSA", props)
            self.assertIn("Hydrogen Bond Donors", props)
            self.assertIn("Hydrogen Bond Acceptors", props)
            self.assertIn("Rotatable Bonds", props)
            self.assertIn("Ring Count", props)
            self.assertIn("Aromatic Rings", props)
            self.assertIn("Fraction Csp3", props)

            # Specific scientific sanity checks
            if name == "Ethanol":
                self.assertEqual(props["Molecular Formula"], "C2H6O")
                self.assertEqual(props["Fraction Csp3"], 1.0)
                self.assertEqual(props["Hydrogen Bond Donors"], 1)
            elif name == "Benzene":
                self.assertEqual(props["Molecular Formula"], "C6H6")
                self.assertEqual(props["Aromatic Rings"], 1)
                self.assertEqual(props["Fraction Csp3"], 0.0)
            elif name == "Aspirin":
                self.assertEqual(props["Molecular Formula"], "C9H8O4")
                self.assertEqual(props["Hydrogen Bond Donors"], 1)
                self.assertEqual(props["Hydrogen Bond Acceptors"], 3)
            elif name == "Glucose":
                self.assertEqual(props["Hydrogen Bond Donors"], 5)
                self.assertEqual(props["Fraction Csp3"], 1.0)

    def test_bond_information_accounting(self):
        """Verify sigma and pi bond calculations."""
        # Benzene C6H6: 12 sigma, 3 pi, total 15
        mol, _ = get_molecule("c1ccccc1")
        bonds = calculate_bond_information(mol)
        self.assertEqual(bonds["Sigma Bonds"], 12)
        self.assertEqual(bonds["Pi Bonds"], 3)
        self.assertEqual(bonds["Total Bonds"], 15)

    def test_functional_group_identification(self):
        """Verify functional group identification matches appropriate chemical classes."""
        # Ethanol has Alcohol
        mol_eth, _ = get_molecule("CCO")
        fg_eth = identify_functional_groups(mol_eth)
        self.assertTrue(any(g["name"] == "Alcohol" for g in fg_eth))

        # Phenol has Phenol & Aromatic Ring
        mol_phe, _ = get_molecule("Oc1ccccc1")
        fg_phe = identify_functional_groups(mol_phe)
        phe_names = [g["name"] for g in fg_phe]
        self.assertIn("Phenol", phe_names)
        self.assertIn("Aromatic Ring", phe_names)

        # Aspirin has Carboxylic Acid & Ester
        mol_asp, _ = get_molecule("CC(=O)Oc1ccccc1C(=O)O")
        fg_asp = identify_functional_groups(mol_asp)
        asp_names = [g["name"] for g in fg_asp]
        self.assertIn("Carboxylic Acid", asp_names)
        self.assertIn("Ester", asp_names)

    def test_2d_and_3d_visualization_generation(self):
        """Verify 2D and 3D generation for all 7 molecules."""
        for name, smi in self.REQUIRED_MOLECULES.items():
            mol, _ = get_molecule(smi)

            # 2D Raster & SVG
            img = generate_2d_image(mol, size=(300, 200))
            self.assertIsNotNone(img)
            svg = generate_2d_svg(mol, size=(300, 200))
            self.assertTrue(svg.startswith("<?xml") or "<svg" in svg)

            # 3D Conformer
            mol3d, err = generate_3d_molecule(mol)
            self.assertIsNotNone(mol3d, f"3D conformer generation failed for {name}: {err}")
            self.assertIsNone(err)

    def test_pdf_report_compilation(self):
        """Verify ReportLab PDF generation for single and batch multi-molecule reports."""
        mol, _ = get_molecule("CCO")
        props = calculate_properties(mol)

        # Single molecule PDF
        pdf_single = generate_molecule_pdf("CCO", mol, props)
        self.assertIsNotNone(pdf_single)
        self.assertTrue(pdf_single.startswith(b"%PDF"))

        # Multi-molecule batch PDF
        batch = [
            ("CCO", mol, props),
            ("c1ccccc1", get_molecule("c1ccccc1")[0], calculate_properties(get_molecule("c1ccccc1")[0]))
        ]
        pdf_multi = generate_multi_final_report("Test Student", "REG999", batch)
        self.assertIsNotNone(pdf_multi)
        self.assertTrue(pdf_multi.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
