import React, { useState, useEffect, useRef } from 'react';
import { compareMolecules } from '../api';
import type { ComparisonResponse, ComparisonRecord } from '../types';
import { AlertCircle, Download, Play } from 'lucide-react';

declare global {
  interface Window {
    Plotly: any;
  }
}

const DEFAULT_COMPARISON_INPUT = `Ethanol, CCO
Benzene, c1ccccc1
Phenol, Oc1ccccc1
Acetic Acid, CC(=O)O
Aspirin, CC(=O)Oc1ccccc1C(=O)O
Caffeine, CN1C=NC2=C1C(=O)N(C(=O)N2C)C
Glucose, OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O`;

export const ComparisonPage: React.FC = () => {
  const [rawText, setRawText] = useState<string>(DEFAULT_COMPARISON_INPUT);
  const [data, setData] = useState<ComparisonResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [selectedChartProp, setSelectedChartProp] = useState<keyof ComparisonRecord>('logp');
  const [scatterX, setScatterX] = useState<keyof ComparisonRecord>('mw');
  const [scatterY, setScatterY] = useState<keyof ComparisonRecord>('logp');

  const barChartRef = useRef<HTMLDivElement>(null);
  const scatterChartRef = useRef<HTMLDivElement>(null);

  const parseAndCompare = async () => {
    setLoading(true);
    setError(null);

    const lines = rawText.split('\n').map((l) => l.trim()).filter(Boolean);
    const molecules: { name: string; smiles: string }[] = [];

    lines.forEach((line, idx) => {
      if (line.includes(',')) {
        const parts = line.split(',');
        molecules.push({
          name: parts[0].trim(),
          smiles: parts.slice(1).join(',').trim()
        });
      } else {
        molecules.push({
          name: `Molecule ${idx + 1}`,
          smiles: line
        });
      }
    });

    try {
      const res = await compareMolecules(molecules);
      setData(res);
    } catch (err: any) {
      setError(err.message || 'Comparison failed');
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    parseAndCompare();
  }, []);

  // Render Plotly Charts
  useEffect(() => {
    if (!data || !window.Plotly) return;

    // 1. Bar Chart
    if (barChartRef.current) {
      const xVals = data.records.map((r) => r.name);
      const yVals = data.records.map((r) => r[selectedChartProp] as number);

      const propLabels: Record<string, string> = {
        mw: 'Molecular Weight (g/mol)',
        logp: 'LogP (Lipophilicity)',
        tpsa: 'TPSA (Å²)',
        hbd: 'Hydrogen Bond Donors',
        hba: 'Hydrogen Bond Acceptors',
        rotatable_bonds: 'Rotatable Bonds',
        fraction_csp3: 'Fraction Csp3'
      };

      const trace = {
        x: xVals,
        y: yVals,
        type: 'bar',
        marker: {
          color: '#2ea043',
          line: { color: '#3fb950', width: 1 }
        }
      };

      const layout = {
        title: { text: `Comparison: ${propLabels[selectedChartProp as string] || selectedChartProp}`, font: { color: '#e6edf3', size: 14 } },
        paper_bgcolor: '#161b22',
        plot_bgcolor: '#1f242c',
        font: { color: '#8b949e', family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 60 },
        xaxis: { gridcolor: '#30363d' },
        yaxis: { gridcolor: '#30363d' }
      };

      window.Plotly.newPlot(barChartRef.current, [trace], layout, { responsive: true, displayModeBar: false });
    }

    // 2. Scatter Plot
    if (scatterChartRef.current) {
      const xVals = data.records.map((r) => r[scatterX] as number);
      const yVals = data.records.map((r) => r[scatterY] as number);
      const textVals = data.records.map((r) => r.name);

      const trace = {
        x: xVals,
        y: yVals,
        mode: 'markers+text',
        text: textVals,
        textposition: 'top center',
        marker: {
          size: 10,
          color: '#388bfd',
          line: { color: '#58a6ff', width: 1.5 }
        }
      };

      const layout = {
        title: { text: `${scatterY.toUpperCase()} vs. ${scatterX.toUpperCase()}`, font: { color: '#e6edf3', size: 14 } },
        paper_bgcolor: '#161b22',
        plot_bgcolor: '#1f242c',
        font: { color: '#8b949e', family: 'Inter, sans-serif' },
        margin: { l: 50, r: 20, t: 40, b: 50 },
        xaxis: { title: scatterX.toUpperCase(), gridcolor: '#30363d' },
        yaxis: { title: scatterY.toUpperCase(), gridcolor: '#30363d' }
      };

      window.Plotly.newPlot(scatterChartRef.current, [trace], layout, { responsive: true, displayModeBar: false });
    }
  }, [data, selectedChartProp, scatterX, scatterY]);

  const handleDownloadCsv = () => {
    if (!data) return;
    const headers = ['Molecule', 'SMILES', 'Formula', 'MW', 'LogP', 'TPSA', 'HBD', 'HBA', 'Rotatable_Bonds', 'Rings', 'Fraction_Csp3'];
    const rows = data.records.map((r) => [
      r.name,
      r.smiles,
      r.formula,
      r.mw,
      r.logp,
      r.tpsa,
      r.hbd,
      r.hba,
      r.rotatable_bonds,
      r.ring_count,
      r.fraction_csp3
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers, ...rows].map((e) => e.map(i => `"${i}"`).join(',')).join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `molecular_comparison.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <span>📈</span> Structure–Property Analysis & Molecule Comparison
        </div>
        <div className="page-subtitle">
          Side-by-Side Descriptor Profiling, Property Extremes, and Interactive Comparative Visualizations
        </div>
      </div>

      {/* Input Text Area */}
      <div className="sci-card">
        <div className="sci-card-header">
          <span>Candidate Molecule Input List (One per line: Molecule Name, SMILES)</span>
          <button className="btn btn-primary btn-sm" onClick={parseAndCompare} disabled={loading}>
            <Play size={13} />
            {loading ? 'Evaluating...' : 'Run Comparison'}
          </button>
        </div>
        <textarea
          rows={6}
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
          style={{ width: '100%', fontFamily: 'JetBrains Mono, monospace', fontSize: '13px' }}
        />
      </div>

      {error && (
        <div className="alert-error">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {data && (
        <>
          {/* Property Extremes Highlights */}
          <div className="metric-grid">
            <div className="metric-card">
              <div className="metric-label">Highest MW</div>
              <div className="metric-value">{data.extremes.highest_mw.value}</div>
              <div style={{ fontSize: '11px', color: '#58a6ff' }}>{data.extremes.highest_mw.name}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Highest LogP</div>
              <div className="metric-value">{data.extremes.highest_logp.value}</div>
              <div style={{ fontSize: '11px', color: '#58a6ff' }}>{data.extremes.highest_logp.name}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Highest TPSA</div>
              <div className="metric-value">{data.extremes.highest_tpsa.value} Å²</div>
              <div style={{ fontSize: '11px', color: '#58a6ff' }}>{data.extremes.highest_tpsa.name}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Highest Fsp3</div>
              <div className="metric-value">{data.extremes.highest_fsp3.value}</div>
              <div style={{ fontSize: '11px', color: '#58a6ff' }}>{data.extremes.highest_fsp3.name}</div>
            </div>
          </div>

          {/* Comparison Table */}
          <div className="sci-card">
            <div className="sci-card-header">
              <span>Side-by-Side Descriptor Comparison Table</span>
              <button className="btn btn-secondary btn-sm" onClick={handleDownloadCsv}>
                <Download size={13} />
                Download Comparison (CSV)
              </button>
            </div>

            <div style={{ overflowX: 'auto' }}>
              <table className="sci-table">
                <thead>
                  <tr>
                    <th>Molecule</th>
                    <th>Formula</th>
                    <th>MW (g/mol)</th>
                    <th>LogP</th>
                    <th>TPSA (Å²)</th>
                    <th>HBD</th>
                    <th>HBA</th>
                    <th>RotB</th>
                    <th>Rings</th>
                    <th>Fsp3</th>
                  </tr>
                </thead>
                <tbody>
                  {data.records.map((r) => (
                    <tr key={r.name}>
                      <td><b>{r.name}</b></td>
                      <td><span className="badge-formula">{r.formula}</span></td>
                      <td>{r.mw}</td>
                      <td>{r.logp}</td>
                      <td>{r.tpsa}</td>
                      <td>{r.hbd}</td>
                      <td>{r.hba}</td>
                      <td>{r.rotatable_bonds}</td>
                      <td>{r.ring_count}</td>
                      <td>{r.fraction_csp3}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Interactive Plotly Charts */}
          <div className="grid-2col">
            <div className="sci-card">
              <div className="sci-card-header">
                <span>Bar Chart Comparison</span>
                <select
                  value={selectedChartProp as string}
                  onChange={(e) => setSelectedChartProp(e.target.value as keyof ComparisonRecord)}
                  style={{ fontSize: '12px', padding: '3px 8px' }}
                >
                  <option value="mw">Molecular Weight</option>
                  <option value="logp">LogP (Lipophilicity)</option>
                  <option value="tpsa">TPSA</option>
                  <option value="hbd">H-Bond Donors</option>
                  <option value="hba">H-Bond Acceptors</option>
                  <option value="rotatable_bonds">Rotatable Bonds</option>
                  <option value="fraction_csp3">Fraction Csp3</option>
                </select>
              </div>
              <div ref={barChartRef} style={{ width: '100%', height: '320px' }} />
            </div>

            <div className="sci-card">
              <div className="sci-card-header">
                <span>Bivariate Scatter Plot</span>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <select
                    value={scatterX as string}
                    onChange={(e) => setScatterX(e.target.value as keyof ComparisonRecord)}
                    style={{ fontSize: '11px', padding: '2px 6px' }}
                  >
                    <option value="mw">X: MW</option>
                    <option value="logp">X: LogP</option>
                    <option value="tpsa">X: TPSA</option>
                    <option value="fraction_csp3">X: Fsp3</option>
                  </select>
                  <select
                    value={scatterY as string}
                    onChange={(e) => setScatterY(e.target.value as keyof ComparisonRecord)}
                    style={{ fontSize: '11px', padding: '2px 6px' }}
                  >
                    <option value="logp">Y: LogP</option>
                    <option value="tpsa">Y: TPSA</option>
                    <option value="mw">Y: MW</option>
                    <option value="hbd">Y: HBD</option>
                  </select>
                </div>
              </div>
              <div ref={scatterChartRef} style={{ width: '100%', height: '320px' }} />
            </div>
          </div>
        </>
      )}
    </div>
  );
};
