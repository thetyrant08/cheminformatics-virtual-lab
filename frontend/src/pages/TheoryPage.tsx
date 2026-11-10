import React from 'react';

export const TheoryPage: React.FC = () => {
  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <span>📖</span> Theory & Cheminformatics Fundamentals
        </div>
        <div className="page-subtitle">
          Educational principles of chemical representation, molecular descriptors, and 3D modeling
        </div>
      </div>

      <div className="sci-card">
        <div className="sci-card-header">
          <span>1. Introduction to Cheminformatics</span>
        </div>
        <p style={{ color: '#8b949e', marginBottom: '8px' }}>
          <b>Cheminformatics</b> represents the intersection of <b>Chemistry</b>, <b>Computer Science</b>, 
          and <b>Information Technology</b>. It applies computational graph theory, mathematical models, 
          and data analysis techniques to process, store, visualize, and analyze chemical structures.
        </p>
        <p style={{ color: '#8b949e' }}>
          Cheminformatics enables the calculation of quantitative structure-property relationships (QSPR), 
          virtual screening of potential pharmaceuticals, and automated chemical database management.
        </p>
      </div>

      <div className="sci-card">
        <div className="sci-card-header">
          <span>2. SMILES Notation (Simplified Molecular Input Line Entry System)</span>
        </div>
        <p style={{ color: '#8b949e', marginBottom: '10px' }}>
          SMILES is an ASCII line notation developed by Arthur Weininger that describes molecular graphs as compact text strings.
        </p>

        <table className="sci-table" style={{ marginBottom: '14px' }}>
          <thead>
            <tr>
              <th>Feature</th>
              <th>SMILES Syntax</th>
              <th>Chemical Example</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Atoms</b></td>
              <td>Organic elements (C, N, O, P, S, halogens). Elements outside organic subset require brackets.</td>
              <td><code>CCO</code> (Ethanol)</td>
            </tr>
            <tr>
              <td><b>Bonds</b></td>
              <td>Single bonds implicit; <code>=</code> for double bonds; <code>#</code> for triple bonds.</td>
              <td><code>C=O</code> (Formaldehyde), <code>C#N</code> (HCN)</td>
            </tr>
            <tr>
              <td><b>Branches</b></td>
              <td>Enclosed in parentheses <code>( )</code> attached to parent atom.</td>
              <td><code>CC(=O)O</code> (Acetic Acid)</td>
            </tr>
            <tr>
              <td><b>Rings</b></td>
              <td>Integer digits tag ring openings and closures.</td>
              <td><code>c1ccccc1</code> (Benzene), <code>C1CCCCC1</code> (Cyclohexane)</td>
            </tr>
            <tr>
              <td><b>Aromaticity</b></td>
              <td>Lowercase letters represent aromatic ring atoms.</td>
              <td><code>c1ccncc1</code> (Pyridine)</td>
            </tr>
            <tr>
              <td><b>Chirality</b></td>
              <td><code>@</code> for anticlockwise; <code>@@</code> for clockwise configuration.</td>
              <td><code>N[C@@H](C)C(=O)O</code> (L-Alanine)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="sci-card">
        <div className="sci-card-header">
          <span>3. Chemical Bonding: Sigma (σ) and Pi (π) Bonds</span>
        </div>
        <p style={{ color: '#8b949e', marginBottom: '10px' }}>
          In valence bond and molecular orbital theory, covalent bonds are classified according to orbital overlap geometry:
        </p>
        <ul style={{ color: '#8b949e', marginLeft: '20px', lineHeight: '1.8' }}>
          <li>
            <b>Sigma (σ) Bonds:</b> Formed by direct end-to-end head-on orbital overlap along the internuclear axis. 
            Every single, double, or triple bond contains <b>exactly one foundational σ bond</b>. Covalent bonds to implicit and explicit hydrogens (C–H, O–H, N–H) are exclusively σ bonds.
          </li>
          <li>
            <b>Pi (π) Bonds:</b> Formed by parallel lateral overlap of unhybridized p-orbitals. 
            A double bond contains $1\\,\\sigma + 1\\,\\pi$ bond; a triple bond contains $1\\,\\sigma + 2\\,\\pi$ bonds.
          </li>
          <li>
            <b>Delocalized π-Electrons:</b> In aromatic systems like benzene, continuous cyclic p-orbital overlap creates a delocalized π-cloud above and below the ring plane.
          </li>
        </ul>
      </div>

      <div className="sci-card">
        <div className="sci-card-header">
          <span>4. Molecular Descriptors</span>
        </div>
        <ul style={{ color: '#8b949e', marginLeft: '20px', lineHeight: '1.8' }}>
          <li><b>Molecular Weight (MW):</b> Sum of average atomic masses; influences diffusion and membrane permeability.</li>
          <li><b>LogP (Crippen):</b> Octanol-water partition coefficient; primary metric for relative lipophilicity.</li>
          <li><b>TPSA:</b> Topological Polar Surface Area (Å²); calculates the contribution of polar nitrogen and oxygen atoms to predict passive intestinal absorption.</li>
          <li><b>Hydrogen Bond Donors / Acceptors:</b> Measures potential for forming directional hydrogen-bond networks with biological targets or solvent.</li>
          <li><b>Fraction Csp3:</b> Ratio of sp3 carbons to total carbons (N_sp3 / N_total); characterizes 3D saturation and spatial complexity.</li>
        </ul>
      </div>

      <div className="sci-card">
        <div className="sci-card-header">
          <span>5. 3D Molecular Conformations & Force Fields</span>
        </div>
        <p style={{ color: '#8b949e', marginBottom: '8px' }}>
          RDKit utilizes the <b>ETKDG</b> (Experimental-Torsion Knowledge Distance Geometry) algorithm to embed realistic 3D coordinates based on experimental small-molecule crystal structures from the Cambridge Structural Database (CSD).
        </p>
        <p style={{ color: '#8b949e' }}>
          Subsequent geometry optimization applies the <b>MMFF94</b> (Merck Molecular Force Field) or <b>UFF</b> (Universal Force Field) to relax bond angles, stretch distances, and steric clashes.
        </p>
      </div>
    </div>
  );
};
