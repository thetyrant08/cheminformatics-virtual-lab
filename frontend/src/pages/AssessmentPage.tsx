import React, { useState, useEffect } from 'react';
import { fetchAssessmentQuestions, submitAssessment } from '../api';
import type { AssessmentQuestion, AssessmentResult } from '../types';
import { CheckCircle2, AlertCircle, RotateCcw } from 'lucide-react';

interface AssessmentPageProps {
  studentName: string;
  regNumber: string;
}

export const AssessmentPage: React.FC<AssessmentPageProps> = ({
  studentName,
  regNumber
}) => {
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([]);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadQuestions = async () => {
    try {
      const qList = await fetchAssessmentQuestions();
      setQuestions(qList);
    } catch (err: any) {
      setError(err.message || 'Failed to load assessment questions');
    }
  };

  useEffect(() => {
    loadQuestions();
  }, []);

  const handleSelectOption = (qId: number, option: string) => {
    if (result) return; // Prevent changing after submission
    setSelectedAnswers((prev) => ({ ...prev, [qId]: option }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Verify all 12 questions are answered
    if (Object.keys(selectedAnswers).length < questions.length) {
      setError(`Please answer all ${questions.length} questions before submitting.`);
      return;
    }

    setLoading(true);
    try {
      const answersArray = questions.map((q) => selectedAnswers[q.id] || null);
      const res = await submitAssessment(answersArray, studentName, regNumber);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to submit assessment');
    } finally {
      setLoading(false);
    }
  };

  const handleRetake = () => {
    setSelectedAnswers({});
    setResult(null);
    setError(null);
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-title">
          <span>📝</span> Cheminformatics Academic Assessment
        </div>
        <div className="page-subtitle">
          Test Your Understanding of SMILES Notation, Molecular Descriptors, Bonding, and 3D Models
        </div>
      </div>

      {error && (
        <div className="alert-error">
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}

      {result && (
        <div className="sci-card" style={{ borderLeft: '4px solid #3fb950', marginBottom: '22px' }}>
          <div className="sci-card-header">
            <span>Assessment Evaluation Report</span>
            <button className="btn btn-secondary btn-sm" onClick={handleRetake}>
              <RotateCcw size={13} />
              Retake Assessment
            </button>
          </div>

          <div style={{ display: 'flex', gap: '24px', alignItems: 'center', marginBottom: '12px' }}>
            <div>
              <div style={{ fontSize: '11px', color: '#8b949e', textTransform: 'uppercase' }}>Candidate</div>
              <div style={{ fontSize: '15px', fontWeight: 600 }}>{result.student_name || 'Independent Scholar'} ({result.registration_number || 'N/A'})</div>
            </div>
            <div>
              <div style={{ fontSize: '11px', color: '#8b949e', textTransform: 'uppercase' }}>Final Score</div>
              <div style={{ fontSize: '20px', fontWeight: 700, color: '#3fb950', fontFamily: 'JetBrains Mono, monospace' }}>
                {result.score} / {result.total} ({result.percentage}%)
              </div>
            </div>
          </div>

          <div className="alert-success" style={{ marginBottom: 0 }}>
            <CheckCircle2 size={16} />
            <span>{result.performance}</span>
          </div>
        </div>
      )}

      {/* Questions Form */}
      <form onSubmit={handleSubmit}>
        {questions.map((q) => {
          const detail = result ? result.details.find((d) => d.id === q.id) : null;
          const isCorrect = detail?.is_correct;

          return (
            <div
              key={q.id}
              className="sci-card"
              style={{
                borderColor: result ? (isCorrect ? '#2ea043' : '#f85149') : undefined,
                marginBottom: '14px'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span style={{ fontWeight: 600, color: '#e6edf3' }}>{q.question}</span>
                {result && (
                  <span className={isCorrect ? 'badge-tag' : 'badge-amber'}>
                    {isCorrect ? 'CORRECT' : 'INCORRECT'}
                  </span>
                )}
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {q.options.map((opt) => {
                  const isSelected = selectedAnswers[q.id] === opt;
                  return (
                    <label
                      key={opt}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '6px 10px',
                        borderRadius: '4px',
                        backgroundColor: isSelected ? 'rgba(56, 139, 253, 0.12)' : '#1f242c',
                        border: isSelected ? '1px solid #388bfd' : '1px solid #30363d',
                        cursor: result ? 'default' : 'pointer',
                        fontSize: '13px'
                      }}
                    >
                      <input
                        type="radio"
                        name={`q_${q.id}`}
                        value={opt}
                        checked={isSelected}
                        onChange={() => handleSelectOption(q.id, opt)}
                        disabled={Boolean(result)}
                      />
                      <span>{opt}</span>
                    </label>
                  );
                })}
              </div>

              {/* Rationale feedback shown after submission */}
              {detail && (
                <div style={{ marginTop: '10px', borderTop: '1px solid #30363d', paddingTop: '8px', fontSize: '12px', color: '#8b949e' }}>
                  {!isCorrect && (
                    <div style={{ color: '#f85149', marginBottom: '4px' }}>
                      Correct Answer: <b>{detail.correct_answer}</b>
                    </div>
                  )}
                  <div><i>Rationale: {detail.explanation}</i></div>
                </div>
              )}
            </div>
          );
        })}

        {!result && (
          <div style={{ marginTop: '20px' }}>
            <button type="submit" className="btn btn-primary" disabled={loading} style={{ width: '100%', padding: '10px' }}>
              {loading ? 'Evaluating...' : 'Submit Academic Assessment'}
            </button>
          </div>
        )}
      </form>
    </div>
  );
};
