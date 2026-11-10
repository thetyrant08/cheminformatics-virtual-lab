import type {
  MoleculeInfoResponse,
  ComparisonResponse,
  AssessmentQuestion,
  AssessmentResult
} from './types';

// Read API URL from environment, defaulting to empty string for relative proxying
const API_BASE = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '');

export async function fetchExamples(): Promise<Record<string, string>> {
  const res = await fetch(`${API_BASE}/api/examples`);
  if (!res.ok) throw new Error('Failed to load example molecules');
  const data = await res.json();
  return data.examples;
}

export async function fetchMoleculeInfo(
  smiles: string,
  showAtomNumbers: boolean = false,
  highlightFg: boolean = false,
  highlightAtoms: number[] | null = null
): Promise<MoleculeInfoResponse> {
  const res = await fetch(`${API_BASE}/api/molecule/info`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      smiles,
      show_atom_numbers: showAtomNumbers,
      highlight_fg: highlightFg,
      highlight_atoms: highlightAtoms
    })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to process molecule' }));
    throw new Error(err.detail || 'Failed to process molecule');
  }

  return res.json();
}

export async function compareMolecules(
  molecules: { name: string; smiles: string }[]
): Promise<ComparisonResponse> {
  const res = await fetch(`${API_BASE}/api/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ molecules })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to compare molecules' }));
    throw new Error(err.detail || 'Comparison request failed');
  }

  return res.json();
}

export async function downloadSinglePdf(
  smiles: string,
  studentName: string = '',
  registrationNumber: string = ''
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/export/pdf/single`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      smiles,
      student_name: studentName,
      registration_number: registrationNumber
    })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to generate PDF' }));
    throw new Error(err.detail || 'Failed to generate PDF');
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Molecular_Properties_Report.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

export async function downloadMultiPdf(
  smilesList: string[],
  studentName: string = '',
  registrationNumber: string = ''
): Promise<void> {
  const res = await fetch(`${API_BASE}/api/export/pdf/multi`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      smiles_list: smilesList,
      student_name: studentName,
      registration_number: registrationNumber
    })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to generate combined PDF' }));
    throw new Error(err.detail || 'Failed to generate combined PDF');
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `Cheminformatics_Final_Student_Report.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

export async function fetchAssessmentQuestions(): Promise<AssessmentQuestion[]> {
  const res = await fetch(`${API_BASE}/api/assessment/questions`);
  if (!res.ok) throw new Error('Failed to load assessment questions');
  const data = await res.json();
  return data.questions;
}

export async function submitAssessment(
  answers: (string | null)[],
  studentName: string = '',
  registrationNumber: string = ''
): Promise<AssessmentResult> {
  const res = await fetch(`${API_BASE}/api/assessment/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      answers,
      student_name: studentName,
      registration_number: registrationNumber
    })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to evaluate assessment' }));
    throw new Error(err.detail || 'Assessment grading failed');
  }

  return res.json();
}
