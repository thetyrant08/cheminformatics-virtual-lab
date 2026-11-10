import React, { useState, useEffect } from 'react';
import { MoleculeViewer2D } from '../components/MoleculeViewer2D';
import { MoleculeViewer3D } from '../components/MoleculeViewer3D';
import { fetchMoleculeInfo } from '../api';
import type { MoleculeInfoResponse } from '../types';
import { AlertCircle, CheckCircle2, Play } from 'lucide-react';

interface VisualizationPageProps {
  activeSmiles: string;
  onSmilesChange: (smiles: string) => void;
  examples: Record<string, string>;
}

export const VisualizationPage: React.FC<VisualizationPageProps> = ({
  activeSmiles,
  onSmilesChange,
  examples
}) => {
  const [inputSmiles, setInputSmiles] = useState<string>(activeSmiles);
  const [selectedExample, setSelectedExample] = useState<string>('Ethanol');
  const [data, setData] = useState<MoleculeInfoResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [showAtomNumbers, setShowAtomNumbers] = useState<boolean>(false);
  const [highlightFg, setHighlightFg] = useState<boolean>(false);

  const loadMolecule = async (smi: string) => {
    if (!smi || !smi.trim()) {
      setError('Please enter a valid SMILES notation.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetchMoleculeInfo(smi, showAtomNumbers, highlightFg);
      setData(res);
      onSmilesChange(smi);
    } catch (err: any) {
      setError(err.message || 'Failed to parse molecule');
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMolecule(activeSmiles);
  }, []);

  const handleApply = (e: React.FormEvent) => {
    e.preventDefault();
    loadMolecule(inputSmiles);
  };

  const handleExampleSelect = (name: string) => {
    setSelectedExample(name);
    const smi = examples[name];
    if (smi) {
      setInputSmiles(smi);
      loadMolecule(smi);
    }
  };

  const toggleAtomNumbers = async (val: boolean) => {
    setShowAtomNumbers(val);
    if (data) {
      try {
        const res = await fetchMoleculeInfo(data.smiles, val, highlightFg);
        setData(res);
      } catch (e) {}
    }
  };

  const toggleHighlightFg = async (val: boolean) => {
    setHighlightFg(val);
    if (data) {
      try {
        const res = await fetchMoleculeInfo(data.smiles, showAtomNumbers, val);
        setData(res);
      } catch (e) {}
    }
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <span>🧬</span> Molecular Visualization Laboratory
        </div>
        <div className="page-subtitle">
          High-DPI 2D Vector Connectivity Diagrams & Interactive 3D WebGL Conformers
        </div>
      </div>

      {/* Input Toolbar */}
      <div className="sci-card" style={{ padding: '12px 16px' }}>
        <form onSubmit={handleApply} style={{ display: 'flex', gap: '10px', alignItems: 'center', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '260px' }}>
            <input
              type="text"
              placeholder="Enter SMILES notation (e.g. CCO, c1ccccc1, CC(=O)Oc1ccccc1C(=O)O)..."
              value={inputSmiles}
              onChange={(e) => setInputSmiles(e.target.value)}
              style={{ width: '100%' }}
            />
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            <Play size={13} />
            {loading ? 'Processing...' : 'Apply & Visualize'}
          </button>

          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            <select
              value={selectedExample}
              onChange={(e) => handleExampleSelect(e.target.value)}
              style={{ fontSize: '13px' }}
            >
              {Object.keys(examples).map((ex) => (
                <option key={ex} value={ex}>{ex}</option>
              ))}
            </select>
          </div>
        </form>
      </div>

      {/* Error / Validation Banner */}
      {error && (
        <div className="alert-error">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {data && (
        <>
          <div className="alert-success" style={{ padding: '8px 14px', marginBottom: '16px' }}>
            <CheckCircle2 size={15} />
            <span>Valid Molecular Graph: <b>{data.properties['Molecular Formula']}</b> ({data.properties['Molecular Weight']} g/mol)</span>
          </div>

          <div className="grid-2col">
            {/* 2D Molecular Diagram */}
            <MoleculeViewer2D
              svg={data.svg_2d}
              formula={data.properties['Molecular Formula']}
              showAtomNumbers={showAtomNumbers}
              onToggleAtomNumbers={toggleAtomNumbers}
              highlightFg={highlightFg}
              onToggleHighlightFg={toggleHighlightFg}
              hasFunctionalGroups={data.functional_groups.length > 0}
            />

            {/* Improved Molecular Information Panel */}
            <div className="sci-card">
              <div className="sci-card-header">
                <span>Molecular Information Panel</span>
                <span className="badge-formula">{data.properties['Molecular Formula']}</span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '13px' }}>
                <div>
                  <span style={{ color: '#8b949e' }}>Canonical SMILES:</span><br />
                  <code className="badge-smiles">{data.properties['Canonical SMILES']}</code>
                </div>
                <div>
                  <span style={{ color: '#8b949e' }}>Isomeric SMILES:</span><br />
                  <code className="badge-smiles">{data.properties['Isomeric SMILES']}</code>
                </div>

                <div style={{ borderTop: '1px solid #30363d', paddingTop: '8px', marginTop: '4px' }}>
                  <table className="sci-table" style={{ fontSize: '12px' }}>
                    <tbody>
                      <tr>
                        <td style={{ color: '#8b949e' }}>Molecular Weight</td>
                        <td><b>{data.properties['Molecular Weight']} g/mol</b></td>
                      </tr>
                      <tr>
                        <td style={{ color: '#8b949e' }}>Heavy Atoms / Total</td>
                        <td>{data.properties['Heavy Atoms']} / {data.properties['Total Atoms Including H'] || data.bond_info['Total Atoms Including H']}</td>
                      </tr>
                      <tr>
                        <td style={{ color: '#8b949e' }}>Covalent Bonds (Heavy)</td>
                        <td>{data.properties['Heavy Atom Bonds']}</td>
                      </tr>
                      <tr>
                        <td style={{ color: '#8b949e' }}>Sigma (σ) Bonds</td>
                        <td><b>{data.properties['Sigma (σ) Bonds']}</b></td>
                      </tr>
                      <tr>
                        <td style={{ color: '#8b949e' }}>Pi (π) Bonds</td>
                        <td><b>{data.properties['Pi (π) Bonds']}</b></td>
                      </tr>
                      <tr>
                        <td style={{ color: '#8b949e' }}>Fraction Csp3</td>
                        <td>{data.properties['Fraction Csp3']}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {/* Detected Functional Groups */}
                {data.functional_groups.length > 0 && (
                  <div style={{ borderTop: '1px solid #30363d', paddingTop: '8px' }}>
                    <div style={{ fontSize: '11px', color: '#8b949e', textTransform: 'uppercase', marginBottom: '4px', fontWeight: 600 }}>
                      Detected Functional Groups
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '5px' }}>
                      {data.functional_groups.map((fg) => (
                        <span key={fg.name} className="badge-tag">
                          {fg.name} ({fg.count})
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* 3D Interactive Conformer */}
          <MoleculeViewer3D molBlock={data.mol_block_3d} height={460} />
        </>
      )}
    </div>
  );
};
