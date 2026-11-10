import React, { useEffect, useRef, useState } from 'react';
import { RotateCcw, Layers } from 'lucide-react';

declare global {
  interface Window {
    $3Dmol: any;
  }
}

interface MoleculeViewer3DProps {
  molBlock: string;
  height?: number;
}

export const MoleculeViewer3D: React.FC<MoleculeViewer3DProps> = ({
  molBlock,
  height = 480
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<any>(null);

  const [style, setStyle] = useState<string>('Ball and Stick');
  const [showSurface, setShowSurface] = useState<boolean>(false);
  const [bgColor, setBgColor] = useState<string>('white');
  const [hoverInfo, setHoverInfo] = useState<string>('');

  const render3D = () => {
    if (!containerRef.current || !window.$3Dmol || !molBlock) return;

    // Clear previous viewer
    containerRef.current.innerHTML = '';

    const config = { backgroundColor: bgColor };
    const viewer = window.$3Dmol.createViewer(containerRef.current, config);
    viewerRef.current = viewer;

    viewer.addModel(molBlock, 'mol');

    // Apply Representation Styles
    if (style === 'Ball and Stick') {
      viewer.setStyle({}, {
        stick: { radius: 0.16 },
        sphere: { scale: 0.3 }
      });
    } else if (style === 'Stick') {
      viewer.setStyle({}, {
        stick: { radius: 0.22 }
      });
    } else if (style === 'Space Filling') {
      viewer.setStyle({}, {
        sphere: { scale: 1.0 }
      });
    } else if (style === 'Wireframe') {
      viewer.setStyle({}, {
        line: { linewidth: 2 }
      });
    } else if (style === 'Cartoon') {
      viewer.setStyle({}, {
        stick: { radius: 0.1 },
        sphere: { scale: 0.2 }
      });
    } else {
      viewer.setStyle({}, {
        stick: { radius: 0.16 },
        sphere: { scale: 0.3 }
      });
    }

    // Optional van der Waals Surface
    if (showSurface) {
      viewer.addSurface(window.$3Dmol.SurfaceType.VDW, {
        opacity: 0.65,
        color: 'white'
      });
    }

    // Atom Hover Callback
    viewer.setHoverable(
      {},
      true,
      (atom: any) => {
        if (atom) {
          setHoverInfo(
            `Atom: ${atom.elem || ''} (Index: ${atom.serial || atom.index || 0}, Position: x: ${atom.x?.toFixed(2)}, y: ${atom.y?.toFixed(2)}, z: ${atom.z?.toFixed(2)})`
          );
        }
      },
      () => {
        setHoverInfo('');
      }
    );

    viewer.zoomTo();
    viewer.render();
  };

  useEffect(() => {
    render3D();
  }, [molBlock, style, showSurface, bgColor]);

  const handleReset = () => {
    if (viewerRef.current) {
      viewerRef.current.zoomTo();
      viewerRef.current.render();
    }
  };

  return (
    <div className="sci-card">
      <div className="sci-card-header">
        <span>Interactive 3D Molecular Conformer (3Dmol.js)</span>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <select
            value={style}
            onChange={(e) => setStyle(e.target.value)}
            style={{ fontSize: '12px', padding: '4px 8px' }}
          >
            <option value="Ball and Stick">Ball and Stick</option>
            <option value="Stick">Stick Model</option>
            <option value="Space Filling">Space Filling (CPK)</option>
            <option value="Wireframe">Wireframe</option>
            <option value="Cartoon">Cartoon</option>
          </select>

          <label style={{ fontSize: '12px', display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={showSurface}
              onChange={(e) => setShowSurface(e.target.checked)}
            />
            <Layers size={13} />
            vdW Surface
          </label>

          <select
            value={bgColor}
            onChange={(e) => setBgColor(e.target.value)}
            style={{ fontSize: '12px', padding: '4px 8px' }}
          >
            <option value="white">Paper White</option>
            <option value="#161b22">Slate Dark</option>
          </select>

          <button className="btn btn-secondary btn-sm" onClick={handleReset} title="Reset Camera View">
            <RotateCcw size={13} />
          </button>
        </div>
      </div>

      <div
        ref={containerRef}
        style={{
          width: '100%',
          height: `${height}px`,
          position: 'relative',
          borderRadius: '4px',
          overflow: 'hidden',
          backgroundColor: bgColor
        }}
      />

      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '8px', fontSize: '11px', color: '#8b949e' }}>
        <span>Rotate: Left-click drag • Pan: Right-click drag • Zoom: Scroll wheel</span>
        <span>{hoverInfo || 'Hover over atoms to inspect Cartesian coordinates'}</span>
      </div>
    </div>
  );
};
