import React, { useState } from 'react';
import { downloadMultiPdf } from '../api';
import { Download, AlertCircle, CheckCircle2 } from 'lucide-react';

interface ReportPageProps {
  studentName: string;
  onStudentNameChange: (name: string) => void;
  regNumber: string;
  onRegNumberChange: (reg: string) => void;
  activeSmiles: string;
}

export const ReportPage: React.FC<ReportPageProps> = ({
  studentName,
  onStudentNameChange,
  regNumber,
  onRegNumberChange,
  activeSmiles
}) => {
  const [smilesText, setSmilesText] = useState<string>(
    `${activeSmiles}\nc1ccccc1\nOc1ccccc1\nCC(=O)Oc1ccccc1C(=O)O`
  );
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleGeneratePdf = async () => {
    setError(null);
    setSuccess(null);

    const lines = smilesText.split('\n').map((l) => l.trim()).filter(Boolean);
    if (lines.length === 0) {
      setError('Please provide at least one SMILES notation.');
      return;
    }

    setLoading(true);
    try {
      await downloadMultiPdf(lines, studentName, regNumber);
      setSuccess(`Successfully generated PDF dossier for ${lines.length} molecule(s)! Check your browser downloads.`);
    } catch (err: any) {
      setError(err.message || 'Failed to generate PDF report');
    } finally {
      setLoading(false);
    }
  };

  const parsedLines = smilesText.split('\n').map((l) => l.trim()).filter(Boolean);

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <span>📄</span> Final Project Report Generator
        </div>
        <div className="page-subtitle">
          Publication-Quality ReportLab PDF Dossiers with 2D/3D Structures, Descriptors, and Methodology Notes
        </div>
      </div>

      {error && (
        <div className="alert-error">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {success && (
        <div className="alert-success">
          <CheckCircle2 size={16} />
          <span>{success}</span>
        </div>
      )}

      <div className="sci-card">
        <div className="sci-card-header">
          <span>Student & Investigator Information</span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
          <div>
            <label style={{ fontSize: '12px', color: '#8b949e', display: 'block', marginBottom: '4px' }}>
              Student / Investigator Name
            </label>
            <input
              type="text"
              placeholder="e.g. Jane Doe"
              value={studentName}
              onChange={(e) => onStudentNameChange(e.target.value)}
              style={{ width: '100%' }}
            />
          </div>
          <div>
            <label style={{ fontSize: '12px', color: '#8b949e', display: 'block', marginBottom: '4px' }}>
              Registration / Academic ID
            </label>
            <input
              type="text"
              placeholder="e.g. RA2311003010001"
              value={regNumber}
              onChange={(e) => onRegNumberChange(e.target.value)}
              style={{ width: '100%' }}
            />
          </div>
        </div>
      </div>

      <div className="sci-card">
        <div className="sci-card-header">
          <span>Target Molecules List (Enter one SMILES per line)</span>
          <span className="badge-tag">{parsedLines.length} molecule(s) queued</span>
        </div>
        <p style={{ fontSize: '12px', color: '#8b949e', marginBottom: '8px' }}>
          The backend ReportLab engine compiles all valid structures into a single comprehensive multi-page PDF document.
        </p>
        <textarea
          rows={6}
          value={smilesText}
          onChange={(e) => setSmilesText(e.target.value)}
          style={{ width: '100%', fontFamily: 'JetBrains Mono, monospace', fontSize: '13px' }}
        />
        <div style={{ marginTop: '12px' }}>
          <button
            className="btn btn-primary"
            onClick={handleGeneratePdf}
            disabled={loading || parsedLines.length === 0}
            style={{ width: '100%', padding: '10px' }}
          >
            <Download size={14} />
            {loading ? 'Compiling Multi-Molecule PDF Dossier...' : 'Compile & Download Combined PDF Report'}
          </button>
        </div>
      </div>

      <div className="sci-card" style={{ fontSize: '12px', color: '#8b949e' }}>
        <div style={{ fontWeight: 600, color: '#e6edf3', marginBottom: '4px' }}>
          Report Dossier Specifications:
        </div>
        <ul style={{ marginLeft: '18px', lineHeight: '1.7' }}>
          <li><b>Structural Characterization:</b> Vector 2D constitutional graph and 3D ball-and-stick CPK projection.</li>
          <li><b>Molecular Descriptors:</b> Complete 35+ descriptor table with student-friendly pedagogical interpretation column.</li>
          <li><b>Point-wise Conclusions:</b> Executive summary highlighting lipophilicity, polarity, bonding, and saturation.</li>
          <li><b>Methodology & Libraries:</b> Educational Python implementation and RDKit/Streamlit/ReportLab role analysis.</li>
        </ul>
      </div>
    </div>
  );
};
