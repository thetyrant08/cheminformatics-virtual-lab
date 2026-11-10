import React, { useState, useEffect } from 'react';
import { fetchMoleculeInfo, downloadSinglePdf } from '../api';
import type { MoleculeInfoResponse } from '../types';
import { AlertCircle, Download, FileText, Play } from 'lucide-react';
import { MoleculeViewer2D } from '../components/MoleculeViewer2D';
import { MoleculeViewer3D } from '../components/MoleculeViewer3D';

interface PropertiesPageProps {
  activeSmiles: string;
  onSmilesChange: (smiles: string) => void;
  examples: Record<string, string>;
  studentName: string;
  regNumber: string;
}

export const PropertiesPage: React.FC<PropertiesPageProps> = ({
  activeSmiles,
  onSmilesChange,
  examples,
  studentName,
  regNumber
}) => {
  const [inputSmiles, setInputSmiles] = useState<string>(activeSmiles);
  const [selectedExample, setSelectedExample] = useState<string>('Ethanol');
  const [data, setData] = useState<MoleculeInfoResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [pdfLoading, setPdfLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadProperties = async (smi: string) => {
    if (!smi || !smi.trim()) {
      setError('Please enter a valid SMILES notation.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetchMoleculeInfo(smi);
      setData(res);
      onSmilesChange(smi);
    } catch (err: any) {
      setError(err.message || 'Failed to calculate properties');
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProperties(activeSmiles);
  }, []);

  const handleApply = (e: React.FormEvent) => {
    e.preventDefault();
    loadProperties(inputSmiles);
  };

  const handleExampleSelect = (name: string) => {
    setSelectedExample(name);
    const smi = examples[name];
    if (smi) {
      setInputSmiles(smi);
      loadProperties(smi);
    }
  };

  const handleDownloadCsv = () => {
    if (!data) return;
    const rows = [
      ['Property', 'Value'],
      ['Input SMILES', data.smiles],
      ['Canonical SMILES', data.properties['Canonical SMILES']],
      ...Object.entries(data.properties).map(([k, v]) => [k, String(v)])
    ];
    const csvContent = 'data:text/csv;charset=utf-8,' + rows.map((e) => e.map(i => `"${i}"`).join(',')).join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `${data.properties['Molecular Formula']}_Properties_Report.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleDownloadPdf = async () => {
    if (!data) return;
    setPdfLoading(true);
    try {
      await downloadSinglePdf(data.smiles, studentName, regNumber);
    } catch (err: any) {
      alert(`PDF generation failed: ${err.message}`);
    } finally {
      setPdfLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <span>📊</span> Molecular Properties Report
        </div>
        <div className="page-subtitle">
          RDKit-Derived Physicochemical Descriptors, Valence Accounting & Scientific Report Generation
        </div>
      </div>

      {/* Input Toolbar */}
      <div className="sci-card" style={{ padding: '12px 16px' }}>
        <form onSubmit={handleApply} style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '260px' }}>
            <input
              type="text"
              placeholder="Enter SMILES notation..."
              value={inputSmiles}
              onChange={(e) => setInputSmiles(e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            <Play size={13} />
            {loading ? 'Calculating...' : 'Calculate Properties'}
          </button>

          <select
            value={selectedExample}
            onChange={(e) => handleExampleSelect(e.target.value)}
            style={{ fontSize: '13px' }}
          >
            {Object.keys(examples).map((ex) => (
              <option key={ex} value={ex}>{ex}</option>
            ))}
          </select>
        </form>
      </div>

      {error && (
        <div className="alert-error">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {data && (
        <>
          {/* Key Metric Grid */}
          <div className="metric-grid">
            <div className="metric-card">
              <div className="metric-label">Molecular Weight</div>
              <div className="metric-value">{data.properties['Molecular Weight']}</div>
              <div style={{ fontSize: '10px', color: '#8b949e' }}>g/mol</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">LogP (Crippen)</div>
              <div className="metric-value">{data.properties['LogP']}</div>
              <div style={{ fontSize: '10px', color: '#8b949e' }}>Lipophilicity</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">TPSA</div>
              <div className="metric-value">{data.properties['TPSA']}</div>
              <div style={{ fontSize: '10px', color: '#8b949e' }}>Å² Polar Area</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Ring Count</div>
              <div className="metric-value">{data.properties['Ring Count']}</div>
              <div style={{ fontSize: '10px', color: '#8b949e' }}>{data.properties['Aromatic Rings']} aromatic</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">H-Bond Donors</div>
              <div className="metric-value">{data.properties['Hydrogen Bond Donors']}</div>
              <div style={{ fontSize: '10px', color: '#8b949e' }}>Lipinski &le; 5</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">H-Bond Acceptors</div>
              <div className="metric-value">{data.properties['Hydrogen Bond Acceptors']}</div>
              <div style={{ fontSize: '10px', color: '#8b949e' }}>Lipinski &le; 10</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Rotatable Bonds</div>
              <div className="metric-value">{data.properties['Rotatable Bonds']}</div>
              <div style={{ fontSize: '10px', color: '#8b949e' }}>Flexibility</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Fraction Csp3</div>
              <div className="metric-value">{data.properties['Fraction Csp3']}</div>
              <div style={{ fontSize: '10px', color: '#8b949e' }}>3D Saturation</div>
            </div>
          </div>

          {/* 2D Diagram & Basic Identifiers */}
          <div className="grid-2col">
            <MoleculeViewer2D
              svg={data.svg_2d}
              formula={data.properties['Molecular Formula']}
              showAtomNumbers={false}
              onToggleAtomNumbers={() => {}}
              highlightFg={false}
              onToggleHighlightFg={() => {}}
              hasFunctionalGroups={false}
            />

            <div className="sci-card">
              <div className="sci-card-header">
                <span>Structural Identifiers</span>
                <span className="badge-formula">{data.properties['Molecular Formula']}</span>
              </div>
              <table className="sci-table" style={{ fontSize: '12px' }}>
                <tbody>
                  <tr>
                    <td style={{ color: '#8b949e' }}>Input SMILES</td>
                    <td><code className="badge-smiles">{data.smiles}</code></td>
                  </tr>
                  <tr>
                    <td style={{ color: '#8b949e' }}>Canonical SMILES</td>
                    <td><code className="badge-smiles">{data.properties['Canonical SMILES']}</code></td>
                  </tr>
                  <tr>
                    <td style={{ color: '#8b949e' }}>Isomeric SMILES</td>
                    <td><code className="badge-smiles">{data.properties['Isomeric SMILES']}</code></td>
                  </tr>
                  <tr>
                    <td style={{ color: '#8b949e' }}>Exact Mass</td>
                    <td>{data.properties['Exact Molecular Weight']} Da</td>
                  </tr>
                  <tr>
                    <td style={{ color: '#8b949e' }}>Heavy Atom Bonds</td>
                    <td>{data.properties['Heavy Atom Bonds']}</td>
                  </tr>
                  <tr>
                    <td style={{ color: '#8b949e' }}>Sigma (σ) Bonds</td>
                    <td>{data.properties['Sigma (σ) Bonds']}</td>
                  </tr>
                  <tr>
                    <td style={{ color: '#8b949e' }}>Pi (π) Bonds</td>
                    <td>{data.properties['Pi (π) Bonds']}</td>
                  </tr>
                  <tr>
                    <td style={{ color: '#8b949e' }}>Molar Refractivity</td>
                    <td>{data.properties['Molar Refractivity']} cm³/mol</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Detected Functional Groups Table */}
          {data.functional_groups.length > 0 && (
            <div className="sci-card">
              <div className="sci-card-header">
                <span>Functional Group Identification (SMARTS Detection)</span>
                <span className="badge-tag">{data.functional_groups.length} groups detected</span>
              </div>
              <table className="sci-table">
                <thead>
                  <tr>
                    <th>Functional Group</th>
                    <th>Count</th>
                    <th>Matched Atom Indices</th>
                    <th>Chemical Significance & Role</th>
                  </tr>
                </thead>
                <tbody>
                  {data.functional_groups.map((g) => (
                    <tr key={g.name}>
                      <td><b>{g.name}</b></td>
                      <td><span className="badge-tag">{g.count}</span></td>
                      <td><code>{JSON.stringify(g.matched_atom_indices)}</code></td>
                      <td style={{ color: '#8b949e' }}>{g.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Complete Properties Table with Interpretations */}
          <div className="sci-card">
            <div className="sci-card-header">
              <span>Complete Molecular Property Table</span>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button className="btn btn-secondary btn-sm" onClick={handleDownloadCsv}>
                  <Download size={13} />
                  Download CSV
                </button>
                <button className="btn btn-primary btn-sm" onClick={handleDownloadPdf} disabled={pdfLoading}>
                  <FileText size={13} />
                  {pdfLoading ? 'Compiling PDF...' : 'Generate PDF Report'}
                </button>
              </div>
            </div>

            <table className="sci-table">
              <thead>
                <tr>
                  <th style={{ width: '22%' }}>Descriptor</th>
                  <th style={{ width: '18%' }}>Calculated Value</th>
                  <th>Pedagogical Interpretation</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(data.properties).map(([key, val]) => (
                  <tr key={key}>
                    <td><b>{key}</b></td>
                    <td><code>{String(val)}</code></td>
                    <td style={{ color: '#8b949e' }}>{data.interpretations[key] || ''}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* 3D Model Display */}
          <MoleculeViewer3D molBlock={data.mol_block_3d} height={440} />
        </>
      )}
    </div>
  );
};
