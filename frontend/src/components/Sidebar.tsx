import React from 'react';
import {
  Home,
  BookOpen,
  Eye,
  BarChart2,
  LineChart,
  FileQuestion,
  FileText,
  FlaskConical
} from 'lucide-react';

interface SidebarProps {
  currentPage: string;
  onPageChange: (page: string) => void;
  studentName: string;
  onStudentNameChange: (name: string) => void;
  regNumber: string;
  onRegNumberChange: (reg: string) => void;
  activeSmiles: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentPage,
  onPageChange,
  studentName,
  onStudentNameChange,
  regNumber,
  onRegNumberChange,
  activeSmiles
}) => {
  const navItems = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'theory', label: 'Theory & Learning', icon: BookOpen },
    { id: 'visualization', label: 'Molecular Visualization', icon: Eye },
    { id: 'properties', label: 'Properties Report', icon: BarChart2 },
    { id: 'comparison', label: 'Structure–Property Analysis', icon: LineChart },
    { id: 'assessment', label: 'Assessment & Quiz', icon: FileQuestion },
    { id: 'report', label: 'Final Project Report', icon: FileText }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-title">
          <FlaskConical size={18} color="#3fb950" />
          <span>Cheminformatics Lab</span>
        </div>
        <div className="sidebar-subtitle">Molecular Modeling Workstation</div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPage === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => onPageChange(item.id)}
            >
              <Icon size={16} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-section">
        <div className="sidebar-section-title">Student Information</div>
        <input
          type="text"
          className="student-input"
          placeholder="Student Name"
          value={studentName}
          onChange={(e) => onStudentNameChange(e.target.value)}
        />
        <input
          type="text"
          className="student-input"
          placeholder="Registration Number"
          value={regNumber}
          onChange={(e) => onRegNumberChange(e.target.value)}
        />
      </div>

      <div className="sidebar-section">
        <div className="sidebar-section-title">Active Working Molecule</div>
        <div className="active-mol-pill">
          <code style={{ wordBreak: 'break-all', color: '#58a6ff' }}>{activeSmiles}</code>
        </div>
      </div>

      <div className="sidebar-section" style={{ fontSize: '11px', color: '#6e7681' }}>
        Division of Chemistry<br />
        Virtual Laboratory Framework<br />
        Powered by RDKit & 3Dmol.js
      </div>
    </aside>
  );
};
