export interface MoleculeProperties {
  "Molecular Formula": string;
  "Molecular Weight": number;
  "Exact Molecular Weight": number;
  "Canonical SMILES": string;
  "Isomeric SMILES": string;
  "LogP": number;
  "TPSA": number;
  "Hydrogen Bond Donors": number;
  "Hydrogen Bond Acceptors": number;
  "Rotatable Bonds": number;
  "Ring Count": number;
  "Aromatic Rings": number;
  "Aliphatic Rings": number;
  "Number of Atoms": number;
  "Heavy Atoms": number;
  "Heavy Atom Bonds": number;
  "Sigma (σ) Bonds": number;
  "Pi (π) Bonds": number;
  "Total Bonds (σ + π)": number;
  "Fraction Csp3": number;
  "Molar Refractivity": number;
  "Formal Charge": number;
  [key: string]: any;
}

export interface FunctionalGroup {
  name: string;
  count: number;
  matched_atom_indices: number[];
  description: string;
  smarts: string;
}

export interface BondInfo {
  "Heavy Atom Bonds": number;
  "Sigma Bonds": number;
  "Pi Bonds": number;
  "Total Bonds": number;
  "Total Atoms Including H": number;
  "Double Bonds": number;
  "Triple Bonds": number;
  "Aromatic Atoms": number;
  "Formal Charge": number;
}

export interface MoleculeInfoResponse {
  smiles: string;
  valid: boolean;
  properties: MoleculeProperties;
  bond_info: BondInfo;
  functional_groups: FunctionalGroup[];
  fg_atom_indices: number[];
  svg_2d: string;
  mol_block_3d: string;
  conformer_error: string | null;
  interpretations: Record<string, string>;
  key_interpretation_points: string[];
}

export interface ComparisonRecord {
  name: string;
  smiles: string;
  formula: string;
  mw: number;
  logp: number;
  tpsa: number;
  hbd: number;
  hba: number;
  rotatable_bonds: number;
  ring_count: number;
  aromatic_rings: number;
  fraction_csp3: number;
  heavy_atoms: number;
}

export interface ComparisonResponse {
  records: ComparisonRecord[];
  skipped: { name: string; smiles: string; error: string }[];
  extremes: {
    highest_mw: { name: string; value: number };
    highest_logp: { name: string; value: number };
    highest_tpsa: { name: string; value: number };
    highest_fsp3: { name: string; value: number };
  };
}

export interface AssessmentQuestion {
  id: number;
  question: string;
  options: string[];
}

export interface AssessmentSubmissionDetail {
  id: number;
  question: string;
  student_answer: string | null;
  correct_answer: string;
  is_correct: boolean;
  explanation: string;
}

export interface AssessmentResult {
  student_name: string;
  registration_number: string;
  score: number;
  total: number;
  percentage: number;
  performance: string;
  details: AssessmentSubmissionDetail[];
}
