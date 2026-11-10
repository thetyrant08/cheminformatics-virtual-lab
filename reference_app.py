"""
Cheminformatics Virtual Laboratory
Interactive educational virtual laboratory for molecular representation,
structure visualization, computational property analysis, and scientific reporting.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit Page Configuration
st.set_page_config(
    page_title="Cheminformatics Virtual Laboratory",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core Chemistry & Visualization Engine
from core.chemistry import (
    EXAMPLE_MOLECULES,
    get_molecule,
    calculate_bond_information,
    calculate_properties,
    generate_3d_molecule,
    identify_functional_groups,
    get_property_interpretation,
    build_key_interpretation_points
)
from core.visualization import (
    generate_2d_image,
    generate_2d_svg,
    display_3d_structure
)
from core.reporting import (
    generate_molecule_pdf,
    generate_multi_final_report
)


# ==============================================================================
# CUSTOM STYLING (Restrained Scientific Workstation Theme)
# ==============================================================================

def load_css():
    """Load restrained, professional scientific workstation styling."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# ==============================================================================
# SHARED APPLICATION STATE
# ==============================================================================

if "active_smiles" not in st.session_state:
    st.session_state.active_smiles = "CCO"

if "selected_example" not in st.session_state:
    st.session_state.selected_example = "Ethanol"

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "registration_number" not in st.session_state:
    st.session_state.registration_number = ""


def load_shared_example():
    """Load the selected reference molecule into the active SMILES state."""
    st.session_state.active_smiles = EXAMPLE_MOLECULES[st.session_state.selected_example]


# ==============================================================================
# SIDEBAR NAVIGATION & STUDENT CONTEXT
# ==============================================================================

st.sidebar.markdown("""
<div style="padding-bottom: 12px; border-bottom: 1px solid #2D3748; margin-bottom: 12px;">
    <div style="font-size: 1.15rem; font-weight: 700; color: #E6EDF3;">🧪 Virtual Lab</div>
    <div style="font-size: 0.78rem; color: #8B949E;">Cheminformatics & Molecular Modeling</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📖 Theory",
        "🧬 Molecular Visualization",
        "📊 Molecular Properties Report",
        "📈 Structure–Property Analysis",
        "📝 Assessment",
        "📄 Final Project Report"
    ],
    key="main_navigation"
)

st.sidebar.divider()

st.sidebar.markdown("### 👩‍🎓 Student Information")
student_name = st.sidebar.text_input("Student Name", key="student_name")
registration_number = st.sidebar.text_input("Registration Number", key="registration_number")

st.sidebar.markdown("""
### 🎓 Learning Objectives
Students can learn:
- SMILES notation & syntax
- 2D & 3D molecular representation
- Chemical bonding (σ and π bonds)
- Functional group identification
- Molecular descriptors & interpretations
- Structure–property relationships
""")

st.sidebar.markdown("---")
curr_smi = st.session_state.get("active_smiles", "CCO")
st.sidebar.markdown(f"""
<div style="font-size:0.75rem; color:#8B949E;">
    <b>Active Molecule:</b><br>
    <code style="word-break:break-all;">{curr_smi}</code>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# MODULE 1: HOME
# ==============================================================================

if page == "🏠 Home":
    st.markdown("""
    <div class="lab-header">
        <div class="lab-title">🧪 Cheminformatics Virtual Laboratory</div>
        <div class="lab-subtitle">Computational Chemistry, Molecular Informatics & Structure Analysis</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Welcome to the Virtual Laboratory")
    st.write("""
    This interactive virtual laboratory provides an integrated computational environment for students 
    and researchers to explore molecular structure representation, 2D and 3D visualization, 
    chemical descriptor calculations, functional group detection, and structure–property relationships.
    """)

    st.markdown("#### 🔬 What can students do?")
    st.markdown("""
    - **Enter and Validate Molecular Structures:** Input any valid SMILES notation with real-time error checking.
    - **2D & 3D Molecular Visualization:** Inspect constitutional graphs and interactive 3D conformations with atom numbering and display modes.
    - **Chemical Bonding Analysis:** Decompose chemical frameworks into covalent $\\sigma$ bonds, $\\pi$ bonds, and aromatic electron systems.
    - **Functional Group Identification:** Automatically detect common organic functional groups using RDKit SMARTS patterns.
    - **Calculate Physicochemical Descriptors:** Compute molecular weight, LogP, TPSA, H-bonding, rotatable bonds, and fraction Csp3.
    - **Compare Multiple Molecules:** Analyze structural and property variations across candidate compounds with interactive charts.
    - **Academic Assessment & Reporting:** Test knowledge with instant scoring and download publication-quality PDF reports.
    """)

    st.markdown("---")
    st.markdown("#### 📚 Reference Example Molecules")
    st.caption("Select any standard molecule below to load directly into the shared working session.")

    example_rows = [
        {"Molecule": "Ethanol", "SMILES": "CCO", "Class": "Alcohol / Solvent", "Description": "Simple primary alcohol; classic model for hydrogen bonding."},
        {"Molecule": "Benzene", "SMILES": "c1ccccc1", "Class": "Aromatic Hydrocarbon", "Description": "Prototypical planar aromatic ring with 6 delocalized π electrons."},
        {"Molecule": "Phenol", "SMILES": "Oc1ccccc1", "Class": "Aromatic Hydroxy", "Description": "Aromatic alcohol illustrating resonance-stabilized phenoxide."},
        {"Molecule": "Acetic Acid", "SMILES": "CC(=O)O", "Class": "Carboxylic Acid", "Description": "Weak organic acid featuring carbonyl and hydroxyl interactions."},
        {"Molecule": "Aspirin", "SMILES": "CC(=O)Oc1ccccc1C(=O)O", "Class": "Analgesic / NSAID", "Description": "Classic pharmaceutical containing ester and carboxylic acid moieties."},
        {"Molecule": "Caffeine", "SMILES": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "Class": "Alkaloid / Stimulant", "Description": "Purine xanthine alkaloid and adenosine receptor antagonist."},
        {"Molecule": "Glucose", "SMILES": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O", "Class": "Carbohydrate", "Description": "Six-carbon aldohexose with multiple chiral hydroxyl centers."}
    ]

    st.dataframe(pd.DataFrame(example_rows), use_container_width=True, hide_index=True)

    col_load1, col_load2 = st.columns([3, 1])
    with col_load1:
        chosen_ex = st.selectbox("Choose Standard Molecule to Load", list(EXAMPLE_MOLECULES.keys()), key="home_load_select")
    with col_load2:
        st.write("")
        st.write("")
        if st.button("📥 Load Selected Molecule", use_container_width=True):
            st.session_state.selected_example = chosen_ex
            st.session_state.active_smiles = EXAMPLE_MOLECULES[chosen_ex]
            st.success(f"Loaded {chosen_ex} into active workspace!")

    st.markdown("---")
    st.markdown("#### 👨‍🏫 Laboratory Information")
    st.markdown("""
    **Cheminformatics Virtual Laboratory Framework**  
    Division of Chemistry & Computational Science  
    *Educational software environment powered by Python, Streamlit, RDKit, py3Dmol and ReportLab.*
    """)


# ==============================================================================
# MODULE 2: THEORY
# ==============================================================================

elif page == "📖 Theory":
    st.markdown("""
    <div class="lab-header">
        <div class="lab-title">📖 Introduction to Cheminformatics & Computational Chemistry</div>
        <div class="lab-subtitle">Core Concepts, Molecular Representations, Chemical Bonding, and Descriptors</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 1. What is Cheminformatics?
    Cheminformatics combines **Chemistry**, **Computer Science**, and **Data Analysis**.
    It applies computational techniques to store, manipulate, visualize, and analyze chemical information, 
    accelerating lead discovery, materials design, and chemical education.
    """)

    st.markdown("""
    ### 2. SMILES Notation (Simplified Molecular Input Line Entry System)
    SMILES represents chemical structures using short, human-readable ASCII text strings.

    #### Key Syntax Rules:
    - **Atoms:** Designated by atomic symbols (`C`, `N`, `O`, `P`, `S`, `F`, `Cl`, `Br`, `I`). Organic subset atoms do not require brackets.
    - **Bonds:** Single bonds are implicit. Double bonds are marked with `=`, and triple bonds with `#`.
    - **Branches:** Represented using parentheses `( )`. For example, acetic acid is `CC(=O)O`.
    - **Rings:** Denoted by integer numbers tagging the opening and closing atoms. Benzene is `c1ccccc1`.
    - **Aromaticity:** Atoms in aromatic rings are written in lowercase letters (e.g., `c`, `n`, `o`).
    """)

    # Illustrated 2D chemical examples
    st.markdown("#### Real Structure Illustrations")
    c1, c2, c3 = st.columns(3)
    with c1:
        m1, _ = get_molecule("CCO")
        if m1:
            st.image(generate_2d_image(m1, size=(280, 180)), caption="Ethanol (SMILES: CCO)")
    with c2:
        m2, _ = get_molecule("c1ccccc1")
        if m2:
            st.image(generate_2d_image(m2, size=(280, 180)), caption="Benzene (SMILES: c1ccccc1)")
    with c3:
        m3, _ = get_molecule("CC(=O)O")
        if m3:
            st.image(generate_2d_image(m3, size=(280, 180)), caption="Acetic Acid (SMILES: CC(=O)O)")

    st.markdown("""
    ### 3. Chemical Bonding: Sigma (σ) and Pi (π) Bonds
    - **Sigma (σ) Bonds:** Formed by head-on orbital overlap. Every covalent connection between two atoms contains exactly one $\\sigma$ bond. This includes all bonds to hydrogen (C–H, O–H, N–H).
    - **Pi (π) Bonds:** Formed by lateral overlap of $p$ orbitals. Double bonds contain $1\\,\\sigma$ and $1\\,\\pi$ bond; triple bonds contain $1\\,\\sigma$ and $2\\,\\pi$ bonds.
    - **Aromatic Delocalization:** In aromatic rings, conjugated $\\pi$ electrons delocalize across all ring atoms, imparting thermodynamic stability.
    """)

    st.markdown("""
    ### 4. Molecular Descriptors
    Molecular descriptors quantify structural and physicochemical properties:
    - **Molecular Weight (MW):** Average molecular mass; influences diffusion and permeability.
    - **LogP:** 1-octanol/water partition coefficient; measures relative lipophilicity.
    - **TPSA (Topological Polar Surface Area):** Polar surface area of oxygen/nitrogen heteroatoms; predicts cell and intestinal permeability.
    - **Hydrogen Bond Donors/Acceptors (HBD/HBA):** Key determinants of aqueous solubility and target binding affinity.
    - **Fraction Csp3:** Ratio of sp3 hybridized carbons; characterizes three-dimensional complexity.
    """)

    st.markdown("""
    ### 5. 3D Molecular Visualization Models
    - **Ball and Stick:** Atoms are represented as spheres and bonds as sticks, clearly depicting stereochemical bond angles.
    - **Stick:** Focuses on covalent connectivity and bonding frameworks.
    - **Space Filling (CPK):** Atoms are rendered at their van der Waals radii, illustrating steric molecular volume.
    - **Wireframe:** Minimalist skeletal line representation.
    """)


# ==============================================================================
# MODULE 3: MOLECULAR VISUALIZATION
# ==============================================================================

elif page == "🧬 Molecular Visualization":
    st.markdown("""
    <div class="lab-header">
        <div class="lab-title">🧬 Molecular Visualization Laboratory</div>
        <div class="lab-subtitle">2D Chemical Diagrams • Functional Group Overlays • Interactive 3D WebGL Models</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2.5, 1])
    with col1:
        smiles = st.text_input("Enter SMILES Notation", key="active_smiles")
    with col2:
        st.selectbox("Choose Example Molecule", list(EXAMPLE_MOLECULES.keys()), key="selected_example")
        st.button("Load Example", on_click=load_shared_example, key="load_vis_btn", use_container_width=True)

    mol, err_msg = get_molecule(smiles)

    if mol is None:
        st.error(f"❌ {err_msg}")
    else:
        st.success("✅ Valid Molecular Structure")
        properties = calculate_properties(mol)
        st.session_state.latest_smiles = smiles
        st.session_state.latest_properties = properties

        # ----------------------------------------------------------------------
        # FUNCTIONAL GROUP SCAN
        # ----------------------------------------------------------------------
        fg_matches = identify_functional_groups(mol)
        all_matched_atoms = list(set(idx for g in fg_matches for idx in g["matched_atom_indices"]))

        # Visual Controls Toolbar
        c_ctrl1, c_ctrl2 = st.columns(2)
        with c_ctrl1:
            show_atom_nums = st.checkbox("Show Atom Index Numbers", value=False)
        with c_ctrl2:
            highlight_fg = st.checkbox(f"Highlight Detected Functional Groups ({len(fg_matches)} found)", value=bool(fg_matches))

        hl_atoms = all_matched_atoms if highlight_fg else None

        col_2d, col_info = st.columns([1.2, 1])

        # 2D Structure Rendering
        with col_2d:
            st.markdown("#### 2D Molecular Structure")
            img_2d = generate_2d_image(mol, size=(680, 460), show_atom_numbers=show_atom_nums, highlight_atoms=hl_atoms)
            st.image(img_2d, use_container_width=True)

            svg_str = generate_2d_svg(mol, size=(680, 460), show_atom_numbers=show_atom_nums, highlight_atoms=hl_atoms)
            st.download_button(
                "⬇️ Download Vector SVG",
                data=svg_str,
                file_name=f"{properties['Molecular Formula']}_2D.svg",
                mime="image/svg+xml"
            )

        # Improved Molecular Information Panel (Requirement 4A)
        with col_info:
            st.markdown("#### Molecular Information Panel")
            st.markdown(f"**Molecular Formula:** <span class='formula-badge'>{properties['Molecular Formula']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Molecular Weight:** `{properties['Molecular Weight']} g/mol`")
            st.markdown(f"**Canonical SMILES:**  \n<span class='smiles-badge'>{properties['Canonical SMILES']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Isomeric SMILES:**  \n<span class='smiles-badge'>{properties['Isomeric SMILES']}</span>", unsafe_allow_html=True)

            bond_info = calculate_bond_information(mol)
            st.markdown("---")
            st.write(f"- **Heavy Atoms:** {mol.GetNumHeavyAtoms()}")
            st.write(f"- **Total Atoms (including H):** {bond_info['Total Atoms Including H']}")
            st.write(f"- **Heavy-Atom Bonds:** {bond_info['Heavy Atom Bonds']}")
            st.write(f"- **Sigma (σ) Bonds:** {bond_info['Sigma Bonds']}")
            st.write(f"- **Pi (π) Bonds:** {bond_info['Pi Bonds']}")
            st.write(f"- **Total Bonds (σ + π):** {bond_info['Total Bonds']}")
            st.write(f"- **Fraction Csp3:** {properties['Fraction Csp3']}")

            # Detected functional groups summary
            if fg_matches:
                st.markdown("---")
                st.markdown("**Detected Functional Groups:**")
                for g in fg_matches:
                    st.write(f"• **{g['name']}:** {g['count']} occurrence(s)")

        st.divider()

        # ----------------------------------------------------------------------
        # 3D INTERACTIVE MOLECULAR MODEL
        # ----------------------------------------------------------------------
        st.markdown("### 🌐 Interactive 3D Molecular Model")

        c3d_1, c3d_2, c3d_3 = st.columns([1.5, 1, 1])
        with c3d_1:
            vis_style = st.selectbox(
                "Select Molecular Representation",
                ["Ball and Stick", "Stick", "Space Filling", "Wireframe", "Cartoon"],
                index=0
            )
        with c3d_2:
            st.write("")
            st.write("")
            show_vdw = st.checkbox("Show van der Waals Surface", value=False)
        with c3d_3:
            st.write("")
            st.write("")
            gen_3d_btn = st.button("🚀 Render 3D Model", use_container_width=True)

        if gen_3d_btn or st.session_state.get("rendered_3d", False):
            st.session_state.rendered_3d = True
            with st.spinner("Generating 3D conformer coordinates (ETKDG + MMFF/UFF)..."):
                mol3d, conf_err = generate_3d_molecule(mol)

            if mol3d is None:
                st.error(f"❌ {conf_err or 'Unable to generate 3D conformer.'}")
            else:
                display_3d_structure(mol3d, style=vis_style, show_surface=show_vdw, height=580)
                st.caption("🖱️ Rotate: Left-click drag • Pan: Right-click drag • Zoom: Scroll wheel")


# ==============================================================================
# MODULE 4: MOLECULAR PROPERTIES REPORT
# ==============================================================================

elif page == "📊 Molecular Properties Report":
    st.markdown("""
    <div class="lab-header">
        <div class="lab-title">📊 Molecular Properties Report</div>
        <div class="lab-subtitle">Complete Descriptor Calculation, Functional Group Profiling, and PDF Reporting</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2.5, 1])
    with col1:
        smiles = st.text_input("Enter SMILES Notation", key="active_smiles")
    with col2:
        st.selectbox("Choose Example Molecule", list(EXAMPLE_MOLECULES.keys()), key="selected_example")
        st.button("Load Example", on_click=load_shared_example, key="load_prop_btn", use_container_width=True)

    mol, err_msg = get_molecule(smiles)

    if mol is None:
        st.error(f"❌ {err_msg}")
    else:
        st.success("✅ Valid Molecular Structure")
        properties = calculate_properties(mol)
        st.session_state.latest_smiles = smiles
        st.session_state.latest_properties = properties

        col_2d, col_basic = st.columns([1.2, 1])

        with col_2d:
            st.markdown("#### 🧬 2D Molecular Structure")
            img_2d = generate_2d_image(mol, size=(680, 440))
            st.image(img_2d, use_container_width=True)

        # Improved Molecular Information Panel (Requirement 4A)
        with col_basic:
            st.markdown("#### 📋 Molecular Information Panel")
            st.markdown(f"**Input SMILES:**  \n<span class='smiles-badge'>{smiles}</span>", unsafe_allow_html=True)
            st.markdown(f"**Canonical SMILES:**  \n<span class='smiles-badge'>{properties['Canonical SMILES']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Isomeric SMILES:**  \n<span class='smiles-badge'>{properties['Isomeric SMILES']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Molecular Formula:** <span class='formula-badge'>{properties['Molecular Formula']}</span>", unsafe_allow_html=True)
            st.write(f"**Heavy Atoms:** {properties['Heavy Atoms']}")
            st.write(f"**Total Atoms:** {properties['Number of Atoms']}")
            st.write(f"**Heavy-Atom Bonds:** {properties['Heavy Atom Bonds']}")
            st.write(f"**Sigma (σ) Bonds:** {properties['Sigma (σ) Bonds']}")
            st.write(f"**Pi (π) Bonds:** {properties['Pi (π) Bonds']}")
            st.write(f"**Total Bonds (σ + π):** {properties['Total Bonds (σ + π)']}")

        st.divider()

        # Key Property Metric Cards
        st.markdown("#### 📊 Key Molecular Descriptors")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Molecular Weight", f"{properties['Molecular Weight']} g/mol")
        m2.metric("LogP (Lipophilicity)", properties["LogP"])
        m3.metric("TPSA (Polar Area)", f"{properties['TPSA']} Å²")
        m4.metric("Ring Count", properties["Ring Count"])

        m5, m6, m7, m8 = st.columns(4)
        m5.metric("H-Bond Donors", properties["Hydrogen Bond Donors"])
        m6.metric("H-Bond Acceptors", properties["Hydrogen Bond Acceptors"])
        m7.metric("Rotatable Bonds", properties["Rotatable Bonds"])
        m8.metric("Fraction Csp3", properties["Fraction Csp3"])

        # Functional Group Identification (Requirement 4B)
        st.divider()
        st.markdown("#### 🏷️ Functional Group Identification")
        fg_list = identify_functional_groups(mol)
        if fg_list:
            fg_rows = [
                {
                    "Functional Group": g["name"],
                    "Occurrences": g["count"],
                    "Matched Atom Indices": str(g["matched_atom_indices"]),
                    "Chemical Role": g["description"]
                }
                for g in fg_list
            ]
            st.dataframe(pd.DataFrame(fg_rows), use_container_width=True, hide_index=True)
        else:
            st.info("No common heteroatomic functional groups identified in this framework.")

        # Complete Property Table
        st.divider()
        st.markdown("#### 📑 Complete Molecular Property Table")
        report_data = []
        for key, value in properties.items():
            report_data.append({
                "Property": key,
                "Value": str(value),
                "Pedagogical Interpretation": get_property_interpretation(key, value, properties)
            })

        report_df = pd.DataFrame(report_data)
        st.dataframe(report_df, use_container_width=True, hide_index=True)

        # Export Controls
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            csv_bytes = report_df[["Property", "Value"]].to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Properties Report (CSV)",
                data=csv_bytes,
                file_name=f"{properties['Molecular Formula']}_Properties_Report.csv",
                mime="text/csv",
                use_container_width=True
            )

        with exp_col2:
            if st.button("📄 Generate Molecular PDF Report", use_container_width=True):
                with st.spinner("Compiling molecular PDF report..."):
                    pdf_data = generate_molecule_pdf(smiles, mol, properties)
                st.download_button(
                    "⬇️ Download Molecular Properties PDF",
                    data=pdf_data,
                    file_name=f"{properties['Molecular Formula']}_Properties_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )


# ==============================================================================
# MODULE 5: STRUCTURE–PROPERTY ANALYSIS & COMPARISON (Requirement 4C)
# ==============================================================================

elif page == "📈 Structure–Property Analysis":
    st.markdown("""
    <div class="lab-header">
        <div class="lab-title">📈 Structure–Property Analysis & Molecular Comparison</div>
        <div class="lab-subtitle">Side-by-Side Descriptor Evaluation, Difference Highlighting, and Comparison Plots</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("Compare multiple molecules. Enter one molecule per line in the format: **Molecule Name, SMILES**")

    default_data = """Ethanol, CCO
Benzene, c1ccccc1
Phenol, Oc1ccccc1
Acetic Acid, CC(=O)O
Aspirin, CC(=O)Oc1ccccc1C(=O)O
Caffeine, CN1C=NC2=C1C(=O)N(C(=O)N2C)C
Glucose, OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"""

    molecule_input = st.text_area("Enter Molecule List", value=default_data, height=180)

    rows = []
    skipped = []

    for line in molecule_input.splitlines():
        if not line.strip():
            continue
        if "," in line:
            name, smi = line.split(",", 1)
            name = name.strip()
            smi = smi.strip()
        else:
            name = f"Molecule {len(rows)+1}"
            smi = line.strip()

        m, err = get_molecule(smi)
        if m:
            prop = calculate_properties(m)
            rows.append({
                "Molecule": name,
                "SMILES": smi,
                "Formula": prop["Molecular Formula"],
                "MW (g/mol)": prop["Molecular Weight"],
                "LogP": prop["LogP"],
                "TPSA (Å²)": prop["TPSA"],
                "HBD": prop["Hydrogen Bond Donors"],
                "HBA": prop["Hydrogen Bond Acceptors"],
                "Rotatable Bonds": prop["Rotatable Bonds"],
                "Ring Count": prop["Ring Count"],
                "Aromatic Rings": prop["Aromatic Rings"],
                "Fraction Csp3": prop["Fraction Csp3"]
            })
        else:
            skipped.append(line.strip())

    if skipped:
        st.warning(f"Skipped invalid entries: {', '.join(skipped)}")

    if rows:
        df = pd.DataFrame(rows)

        st.markdown("#### 📋 Side-by-Side Descriptor Comparison Table")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Highlight Property Extremes / Summary
        st.markdown("#### 🔍 Property Extremes & Differences")
        c_ext1, c_ext2, c_ext3, c_ext4 = st.columns(4)
        c_ext1.metric("Highest MW", f"{df.loc[df['MW (g/mol)'].idxmax()]['Molecule']} ({df['MW (g/mol)'].max():.1f})")
        c_ext2.metric("Highest LogP", f"{df.loc[df['LogP'].idxmax()]['Molecule']} ({df['LogP'].max():.2f})")
        c_ext3.metric("Highest TPSA", f"{df.loc[df['TPSA (Å²)'].idxmax()]['Molecule']} ({df['TPSA (Å²)'].max():.1f} Å²)")
        c_ext4.metric("Highest Fsp3", f"{df.loc[df['Fraction Csp3'].idxmax()]['Molecule']} ({df['Fraction Csp3'].max():.2f})")

        # Interactive Comparison Charts (Plotly)
        st.markdown("---")
        st.markdown("#### 📊 Comparative Visualizations")

        chart_tab1, chart_tab2 = st.tabs(["Bar Chart Comparison", "Bivariate Scatter Plot"])

        with chart_tab1:
            prop_choice = st.selectbox(
                "Select Descriptor to Compare",
                ["MW (g/mol)", "LogP", "TPSA (Å²)", "HBD", "HBA", "Rotatable Bonds", "Fraction Csp3"],
                index=1
            )
            fig_bar = px.bar(
                df,
                x="Molecule",
                y=prop_choice,
                color=prop_choice,
                color_continuous_scale="Teal",
                title=f"Comparison: {prop_choice}"
            )
            fig_bar.update_layout(paper_bgcolor="#0F141C", plot_bgcolor="#171D26", font=dict(color="#E6EDF3"))
            st.plotly_chart(fig_bar, use_container_width=True)

        with chart_tab2:
            sc_c1, sc_c2 = st.columns(2)
            with sc_c1:
                x_prop = st.selectbox("X Axis Descriptor", ["MW (g/mol)", "LogP", "TPSA (Å²)", "Fraction Csp3"], index=0)
            with sc_c2:
                y_prop = st.selectbox("Y Axis Descriptor", ["LogP", "TPSA (Å²)", "MW (g/mol)", "HBD"], index=0)

            fig_scatter = px.scatter(
                df,
                x=x_prop,
                y=y_prop,
                color="Molecule",
                text="Molecule",
                title=f"{y_prop} vs. {x_prop}"
            )
            fig_scatter.update_traces(textposition="top center", marker=dict(size=12))
            fig_scatter.update_layout(paper_bgcolor="#0F141C", plot_bgcolor="#171D26", font=dict(color="#E6EDF3"))
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Download CSV
        st.divider()
        csv_comp = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Comparison Table (CSV)",
            data=csv_comp,
            file_name="structure_property_comparison.csv",
            mime="text/csv"
        )
    else:
        st.warning("Please enter at least one valid molecule in the format: Molecule Name, SMILES")


# ==============================================================================
# MODULE 6: ASSESSMENT
# ==============================================================================

elif page == "📝 Assessment":
    st.markdown("""
    <div class="lab-header">
        <div class="lab-title">📝 Cheminformatics Academic Assessment</div>
        <div class="lab-subtitle">Test Your Understanding of SMILES, Bonding, Descriptors, and 3D Models</div>
    </div>
    """, unsafe_allow_html=True)

    questions = [
        {
            "question": "1. What is the full expansion of the acronym SMILES?",
            "options": [
                "Simplified Molecular Input Line Entry System",
                "Standard Molecular Information Language Encoding System",
                "Simple Molecular Identification and Labeling System"
            ],
            "answer": "Simplified Molecular Input Line Entry System",
            "explanation": "SMILES stands for Simplified Molecular Input Line Entry System, introduced by Arthur Weininger."
        },
        {
            "question": "2. What does a SMILES string represent?",
            "options": [
                "A molecular structure using a text string",
                "A spectroscopy technique",
                "A laboratory analytical instrument"
            ],
            "answer": "A molecular structure using a text string",
            "explanation": "SMILES uses compact alphanumeric characters to specify molecular connectivity and stereochemistry."
        },
        {
            "question": "3. Which SMILES notation represents ethanol?",
            "options": ["CCO", "c1ccccc1", "CC(=O)O"],
            "answer": "CCO",
            "explanation": "CCO denotes two connected carbon atoms followed by a hydroxyl oxygen (CH3-CH2-OH)."
        },
        {
            "question": "4. Which SMILES notation represents benzene?",
            "options": ["c1ccccc1", "CCO", "O=C=O"],
            "answer": "c1ccccc1",
            "explanation": "c1ccccc1 denotes a 6-membered aromatic ring with opening and closing ring tag 1."
        },
        {
            "question": "5. In SMILES, parentheses '( )' are mainly used to indicate:",
            "options": ["Branches", "Molecular weight", "Atom colour"],
            "answer": "Branches",
            "explanation": "Parentheses enclose side-chain branches attached to the preceding atom, such as in CC(=O)O."
        },
        {
            "question": "6. Which descriptor is commonly associated with molecular lipophilicity?",
            "options": ["LogP", "TPSA", "HBD"],
            "answer": "LogP",
            "explanation": "LogP quantifies differential solubility between 1-octanol and water, reflecting lipophilicity."
        },
        {
            "question": "7. What does TPSA describe?",
            "options": [
                "Topological Polar Surface Area",
                "Total Pi Surface Area",
                "Thermal Property Surface Analysis"
            ],
            "answer": "Topological Polar Surface Area",
            "explanation": "TPSA estimates the surface area contributed by polar atoms (O, N, and attached hydrogens)."
        },
        {
            "question": "8. What does HBA stand for in Lipinski's Rule of Five?",
            "options": ["Hydrogen Bond Acceptor", "Heavy Bond Atom", "Hydrogen Bond Analysis"],
            "answer": "Hydrogen Bond Acceptor",
            "explanation": "HBA stands for Hydrogen Bond Acceptor (typically nitrogen and oxygen lone pairs)."
        },
        {
            "question": "9. What does HBD stand for in Lipinski's Rule of Five?",
            "options": ["Hydrogen Bond Donor", "Heavy Bond Descriptor", "Hydrogen Bond Distance"],
            "answer": "Hydrogen Bond Donor",
            "explanation": "HBD stands for Hydrogen Bond Donor (typically OH and NH groups)."
        },
        {
            "question": "10. In chemical bonding, how many pi (π) bonds exist in a double bond?",
            "options": ["1", "2", "0"],
            "answer": "1",
            "explanation": "A standard covalent double bond consists of 1 sigma (σ) bond and 1 pi (π) bond."
        },
        {
            "question": "11. How many pi (π) bonds are present in a triple bond?",
            "options": ["2", "1", "3"],
            "answer": "2",
            "explanation": "A covalent triple bond consists of 1 sigma (σ) bond and 2 orthogonal pi (π) bonds."
        },
        {
            "question": "12. Which molecular model is useful for visualizing approximate van der Waals steric volume?",
            "options": ["Space Filling", "Wireframe only", "Text SMILES"],
            "answer": "Space Filling",
            "explanation": "Space Filling (CPK) models scale spheres to van der Waals radii to represent steric volume."
        }
    ]

    student_answers = []
    for i, q in enumerate(questions):
        ans = st.radio(
            q["question"],
            q["options"],
            index=None,
            key=f"assess_q_{i}"
        )
        student_answers.append(ans)

    if st.button("Submit Assessment", use_container_width=True):
        if any(a is None for a in student_answers):
            st.warning("⚠️ Please answer all questions before submitting the assessment.")
            st.stop()

        score = 0
        for i, q in enumerate(questions):
            if student_answers[i] == q["answer"]:
                score += 1

        percentage = (score / len(questions)) * 100
        st.markdown("### Assessment Results")
        c_sc1, c_sc2 = st.columns(2)
        c_sc1.metric("Your Score", f"{score} / {len(questions)}")
        c_sc2.metric("Percentage", f"{percentage:.1f}%")

        if percentage >= 80:
            st.success("🎉 Excellent performance! Strong understanding of cheminformatics principles.")
        elif percentage >= 50:
            st.info("👍 Good performance! Continue practicing and review areas of uncertainty.")
        else:
            st.warning("📚 Please review the Theory section and retake the assessment.")

        st.markdown("---")
        st.markdown("#### Detailed Question Corrections & Explanations")
        for i, q in enumerate(questions):
            correct = student_answers[i] == q["answer"]
            status_tag = "<span style='color:#3FB950;'>CORRECT</span>" if correct else "<span style='color:#F85149;'>INCORRECT</span>"
            st.markdown(f"""
            <div class="sci-card">
                <div><b>{q['question']}</b> — {status_tag}</div>
                <div style="font-size:0.85rem; margin-top:4px;">
                    Your answer: <code>{student_answers[i]}</code> | Correct answer: <b>{q['answer']}</b>
                </div>
                <div style="font-size:0.82rem; color:#8B949E; margin-top:4px;">
                    <i>Rationale: {q['explanation']}</i>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# MODULE 7: FINAL PROJECT REPORT
# ==============================================================================

elif page == "📄 Final Project Report":
    st.markdown("""
    <div class="lab-header">
        <div class="lab-title">📄 Final Student Molecular Analysis Report</div>
        <div class="lab-subtitle">Single or Multi-Molecule Publication-Quality PDF Report Generation</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("Enter one SMILES string per line. The report will compile all valid molecules into a single downloadable PDF.")

    c_rep1, c_rep2 = st.columns(2)
    with c_rep1:
        name = st.text_input("Student Name for Report", value=st.session_state.get("student_name", ""), key="final_rep_name")
        st.session_state.student_name = name
    with c_rep2:
        reg = st.text_input("Registration Number for Report", value=st.session_state.get("registration_number", ""), key="final_rep_reg")
        st.session_state.registration_number = reg

    default_smiles = st.session_state.get("latest_smiles", st.session_state.get("active_smiles", "CCO"))
    multi_smiles_text = st.text_area(
        "Enter SMILES (one molecule per line)",
        value=st.session_state.get("final_report_smiles_multi", default_smiles),
        height=140,
        key="final_report_smiles_multi",
        help="Example: CCO on line 1, c1ccccc1 on line 2, and so on."
    )

    smiles_entries = [line.strip() for line in multi_smiles_text.splitlines() if line.strip()]
    molecule_records = []
    invalid_smiles = []

    for smiles_item in smiles_entries:
        mol_item, err = get_molecule(smiles_item)
        if mol_item is None:
            invalid_smiles.append(f"{smiles_item} ({err})")
            continue
        props_item = calculate_properties(mol_item)
        molecule_records.append((smiles_item, mol_item, props_item))

    if invalid_smiles:
        st.warning("These entries could not be parsed and will be omitted:\n" + "\n".join(invalid_smiles))

    if molecule_records:
        st.success(f"{len(molecule_records)} valid molecule(s) prepared for PDF dossier generation.")

        preview_rows = []
        for idx, (smi_it, m_it, p_it) in enumerate(molecule_records, start=1):
            preview_rows.append({
                "No.": idx,
                "Input SMILES": smi_it,
                "Molecular Formula": p_it["Molecular Formula"],
                "Molecular Weight": f"{p_it['Molecular Weight']} g/mol"
            })
        st.dataframe(pd.DataFrame(preview_rows), use_container_width=True, hide_index=True)

        if st.button("📄 Generate Combined PDF Report for All Molecules", use_container_width=True):
            with st.spinner(f"Generating comprehensive PDF dossier for {len(molecule_records)} molecule(s)..."):
                pdf_data = generate_multi_final_report(name, reg, molecule_records)

            st.success("✅ Combined molecular report compiled successfully!")
            st.download_button(
                label="⬇️ Download Combined Molecular Report (PDF)",
                data=pdf_data,
                file_name="Cheminformatics_Final_Student_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.info("Enter at least one valid SMILES string above to compile the PDF report.")


# ==============================================================================
# FOOTER
# ==============================================================================

st.divider()
st.caption(
    "🧪 Cheminformatics Virtual Laboratory | "
    "Developed using Python, Streamlit, RDKit, py3Dmol and ReportLab"
)
