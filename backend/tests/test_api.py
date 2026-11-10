"""
Cheminformatics Virtual Laboratory - FastAPI Backend Test Suite
Validates all endpoints across the 7 required test molecules.
"""

import unittest
import sys
import os

# Put backend on path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


class TestFastAPIBackend(unittest.TestCase):
    """Test suite for FastAPI endpoints."""

    REQUIRED_MOLECULES = {
        "Ethanol": "CCO",
        "Benzene": "c1ccccc1",
        "Phenol": "Oc1ccccc1",
        "Acetic acid": "CC(=O)O",
        "Aspirin": "CC(=O)Oc1ccccc1C(=O)O",
        "Caffeine": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
        "Glucose": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"
    }

    def test_health_check(self):
        """Test GET /api/health."""
        res = client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("rdkit_version", data)

    def test_examples_endpoint(self):
        """Test GET /api/examples."""
        res = client.get("/api/examples")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("examples", data)
        self.assertIn("Ethanol", data["examples"])

    def test_molecule_info_required_molecules(self):
        """Test POST /api/molecule/info on all 7 benchmark molecules."""
        for name, smi in self.REQUIRED_MOLECULES.items():
            res = client.post("/api/molecule/info", json={"smiles": smi, "show_atom_numbers": True})
            self.assertEqual(res.status_code, 200, f"Failed on {name}: {res.text}")
            data = res.json()
            self.assertTrue(data["valid"])
            self.assertIn("properties", data)
            self.assertIn("svg_2d", data)
            self.assertIn("mol_block_3d", data)
            self.assertIn("functional_groups", data)
            self.assertIn("interpretations", data)

            props = data["properties"]
            self.assertIn("Molecular Formula", props)
            self.assertIn("Molecular Weight", props)
            self.assertIn("LogP", props)
            self.assertIn("TPSA", props)
            self.assertIn("Fraction Csp3", props)

    def test_invalid_smiles_handling(self):
        """Test error handling for unparseable chemical input."""
        res = client.post("/api/molecule/info", json={"smiles": "InvalidSmilesXYZ123==="})
        self.assertEqual(res.status_code, 400)
        self.assertIn("detail", res.json())

    def test_compare_endpoint(self):
        """Test POST /api/compare."""
        items = [{"name": n, "smiles": s} for n, s in list(self.REQUIRED_MOLECULES.items())[:4]]
        res = client.post("/api/compare", json={"molecules": items})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data["records"]), 4)
        self.assertIn("extremes", data)

    def test_assessment_endpoints(self):
        """Test assessment questions retrieval and grading."""
        # 1. Get questions
        q_res = client.get("/api/assessment/questions")
        self.assertEqual(q_res.status_code, 200)
        q_data = q_res.json()
        self.assertEqual(len(q_data["questions"]), 12)

        # 2. Submit answers
        sample_answers = [
            "Simplified Molecular Input Line Entry System",
            "A molecular structure using a text string",
            "CCO",
            "c1ccccc1",
            "Branches",
            "LogP",
            "Topological Polar Surface Area",
            "Hydrogen Bond Acceptor",
            "Hydrogen Bond Donor",
            "1",
            "2",
            "Space Filling"
        ]
        sub_res = client.post(
            "/api/assessment/submit",
            json={
                "answers": sample_answers,
                "student_name": "Test Student",
                "registration_number": "REG100"
            }
        )
        self.assertEqual(sub_res.status_code, 200)
        sub_data = sub_res.json()
        self.assertEqual(sub_data["score"], 12)
        self.assertEqual(sub_data["percentage"], 100.0)

    def test_pdf_export_endpoints(self):
        """Test single and multi PDF generation."""
        # Single PDF
        p1 = client.post("/api/export/pdf/single", json={"smiles": "CCO"})
        self.assertEqual(p1.status_code, 200)
        self.assertTrue(p1.content.startswith(b"%PDF"))

        # Multi PDF
        p2 = client.post(
            "/api/export/pdf/multi",
            json={
                "student_name": "Student A",
                "registration_number": "123",
                "smiles_list": ["CCO", "c1ccccc1"]
            }
        )
        self.assertEqual(p2.status_code, 200)
        self.assertTrue(p2.content.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
