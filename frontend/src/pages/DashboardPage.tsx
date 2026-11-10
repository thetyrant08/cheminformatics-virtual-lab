import React from 'react';
import { Eye, BarChart2, LineChart, FileText, ArrowRight } from 'lucide-react';

interface DashboardPageProps {
  onNavigate: (page: string) => void;
  onSelectExample: (name: string, smiles: string) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  onNavigate,
  onSelectExample
}) => {
  const exampleList = [
    { name: 'Ethanol', smiles: 'CCO', desc: 'Simple primary alcohol; classic hydrogen bonding model.' },
    { name: 'Benzene', smiles: 'c1ccccc1', desc: 'Planar aromatic hydrocarbon with 6 delocalized π electrons.' },
    { name: 'Phenol', smiles: 'Oc1ccccc1', desc: 'Aromatic hydroxyl showing resonance-stabilized phenoxide.' },
    { name: 'Acetic Acid', smiles: 'CC(=O)O', desc: 'Simple carboxylic acid with carbonyl/hydroxyl interactions.' },
    { name: 'Aspirin', smiles: 'CC(=O)Oc1ccccc1C(=O)O', desc: 'Classic pharmaceutical containing ester and carboxylic acid.' },
    { name: 'Caffeine', smiles: 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C', desc: 'Purine xanthine alkaloid and adenosine receptor antagonist.' },
    { name: 'Glucose', smiles: 'OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O', desc: 'Six-carbon aldohexose with multiple chiral hydroxyl centers.' }
  ];

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <span>🧪</span> Cheminformatics Virtual Laboratory
        </div>
        <div className="page-subtitle">
          Interactive Computational Chemistry, Molecular Modeling & Cheminformatics Workstation
        </div>
      </div>

      <div className="sci-card">
        <div className="sci-card-header">
          <span>Welcome to the Virtual Laboratory</span>
          <span className="badge-tag">Academic Workstation</span>
        </div>
        <p style={{ color: '#8b949e', marginBottom: '14px' }}>
          This virtual laboratory provides an integrated scientific environment for exploring chemical 
          representation, molecular descriptor calculations, 2D and 3D visualization, functional group detection, 
          structure–property relationships, and automated scientific report generation.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '12px' }}>
          <button className="btn btn-secondary" onClick={() => onNavigate('visualization')} style={{ justifyContent: 'space-between' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Eye size={15} color="#3fb950" />
              <span>3D Visualization</span>
            </span>
            <ArrowRight size={14} />
          </button>

          <button className="btn btn-secondary" onClick={() => onNavigate('properties')} style={{ justifyContent: 'space-between' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <BarChart2 size={15} color="#58a6ff" />
              <span>Properties Report</span>
            </span>
            <ArrowRight size={14} />
          </button>

          <button className="btn btn-secondary" onClick={() => onNavigate('comparison')} style={{ justifyContent: 'space-between' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <LineChart size={15} color="#d29922" />
              <span>Molecular Comparison</span>
            </span>
            <ArrowRight size={14} />
          </button>

          <button className="btn btn-secondary" onClick={() => onNavigate('report')} style={{ justifyContent: 'space-between' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileText size={15} color="#bc8cff" />
              <span>Final Report</span>
            </span>
            <ArrowRight size={14} />
          </button>
        </div>
      </div>

      <div className="sci-card">
        <div className="sci-card-header">
          <span>Reference Standard Molecules</span>
          <span style={{ fontSize: '12px', color: '#8b949e' }}>Click any molecule to load into workspace</span>
        </div>

        <table className="sci-table">
          <thead>
            <tr>
              <th>Molecule Name</th>
              <th>SMILES Notation</th>
              <th>Chemical Classification / Description</th>
              <th style={{ textAlign: 'right' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {exampleList.map((item) => (
              <tr key={item.name}>
                <td><b>{item.name}</b></td>
                <td><code className="badge-smiles">{item.smiles}</code></td>
                <td style={{ color: '#8b949e' }}>{item.desc}</td>
                <td style={{ textAlign: 'right' }}>
                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => onSelectExample(item.name, item.smiles)}
                  >
                    Load Molecule
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="sci-card" style={{ fontSize: '12px', color: '#8b949e' }}>
        <div style={{ fontWeight: 600, color: '#e6edf3', marginBottom: '6px' }}>
          Cheminformatics Virtual Laboratory Framework
        </div>
        Division of Chemistry & Molecular Science • Faculty of Engineering and Technology<br />
        Built using Python, FastAPI, RDKit, React, Vite, TypeScript, 3Dmol.js and ReportLab.
      </div>
    </div>
  );
};
