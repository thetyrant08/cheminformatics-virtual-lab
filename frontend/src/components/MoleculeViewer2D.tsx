import React from 'react';
import { Download } from 'lucide-react';

interface MoleculeViewer2DProps {
  svg: string;
  formula?: string;
  showAtomNumbers: boolean;
  onToggleAtomNumbers: (val: boolean) => void;
  highlightFg: boolean;
  onToggleHighlightFg: (val: boolean) => void;
  hasFunctionalGroups: boolean;
}

export const MoleculeViewer2D: React.FC<MoleculeViewer2DProps> = ({
  svg,
  formula,
  showAtomNumbers,
  onToggleAtomNumbers,
  highlightFg,
  onToggleHighlightFg,
  hasFunctionalGroups
}) => {
  const downloadSvg = () => {
    if (!svg) return;
    const blob = new Blob([svg], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${formula || 'molecule'}_2D.svg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="sci-card">
      <div className="sci-card-header">
        <span>2D Molecular Connectivity Diagram</span>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <label style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={showAtomNumbers}
              onChange={(e) => onToggleAtomNumbers(e.target.checked)}
            />
            Atom Numbers
          </label>
          <label style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={highlightFg}
              onChange={(e) => onToggleHighlightFg(e.target.checked)}
              disabled={!hasFunctionalGroups}
            />
            Highlight Groups
          </label>
          <button className="btn btn-secondary btn-sm" onClick={downloadSvg} title="Download Vector SVG">
            <Download size={13} />
            SVG
          </button>
        </div>
      </div>

      <div
        style={{
          backgroundColor: '#ffffff',
          borderRadius: '4px',
          padding: '12px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '360px',
          overflow: 'hidden'
        }}
        dangerouslySetInnerHTML={{ __html: svg }}
      />
    </div>
  );
};
