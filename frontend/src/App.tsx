import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { DashboardPage } from './pages/DashboardPage';
import { TheoryPage } from './pages/TheoryPage';
import { VisualizationPage } from './pages/VisualizationPage';
import { PropertiesPage } from './pages/PropertiesPage';
import { ComparisonPage } from './pages/ComparisonPage';
import { AssessmentPage } from './pages/AssessmentPage';
import { ReportPage } from './pages/ReportPage';
import { fetchExamples } from './api';
import './App.css';

export const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<string>('home');
  const [activeSmiles, setActiveSmiles] = useState<string>('CCO');
  const [studentName, setStudentName] = useState<string>('');
  const [regNumber, setRegNumber] = useState<string>('');
  const [examples, setExamples] = useState<Record<string, string>>({
    'Ethanol': 'CCO',
    'Benzene': 'c1ccccc1',
    'Phenol': 'Oc1ccccc1',
    'Acetic Acid': 'CC(=O)O',
    'Aspirin': 'CC(=O)Oc1ccccc1C(=O)O',
    'Caffeine': 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C',
    'Glucose': 'OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O'
  });

  useEffect(() => {
    fetchExamples()
      .then((ex) => setExamples(ex))
      .catch(() => {});
  }, []);

  const handleSelectExample = (_name: string, smi: string) => {
    setActiveSmiles(smi);
    setCurrentPage('visualization');
  };

  return (
    <div className="app-container">
      <Sidebar
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        studentName={studentName}
        onStudentNameChange={setStudentName}
        regNumber={regNumber}
        onRegNumberChange={setRegNumber}
        activeSmiles={activeSmiles}
      />

      <main className="main-content">
        {currentPage === 'home' && (
          <DashboardPage
            onNavigate={setCurrentPage}
            onSelectExample={handleSelectExample}
          />
        )}
        {currentPage === 'theory' && <TheoryPage />}
        {currentPage === 'visualization' && (
          <VisualizationPage
            activeSmiles={activeSmiles}
            onSmilesChange={setActiveSmiles}
            examples={examples}
          />
        )}
        {currentPage === 'properties' && (
          <PropertiesPage
            activeSmiles={activeSmiles}
            onSmilesChange={setActiveSmiles}
            examples={examples}
            studentName={studentName}
            regNumber={regNumber}
          />
        )}
        {currentPage === 'comparison' && <ComparisonPage />}
        {currentPage === 'assessment' && (
          <AssessmentPage
            studentName={studentName}
            regNumber={regNumber}
          />
        )}
        {currentPage === 'report' && (
          <ReportPage
            studentName={studentName}
            onStudentNameChange={setStudentName}
            regNumber={regNumber}
            onRegNumberChange={setRegNumber}
            activeSmiles={activeSmiles}
          />
        )}
      </main>
    </div>
  );
};

export default App;
