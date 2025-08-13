import React from 'react';
import { useCreateSurvey } from './CreateSurveyProvider';

export default function Sidebar() {
  const { questions, surveyTitle, resetSurvey } = useCreateSurvey();

  const scrollTo = (qid) => {
    const el = document.getElementById(`q-${qid}`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <aside className="h-screen w-60 bg-slate-900 text-slate-100 p-4 sticky top-0 hidden md:block">
      <div className="text-slate-300 text-sm mb-2">Sidebar</div>

      <nav className="space-y-1">
        <div className="text-xs uppercase tracking-wide text-slate-400 mb-2">Navigation</div>

        {/* NEW: Reset survey */}
        <button
          className="w-full text-left px-3 py-2 rounded hover:bg-slate-800"
          onClick={resetSurvey}
          title="Start a brand new survey"
        >
          Create a New Survey
        </button>

        <div className="mt-4 text-xs uppercase tracking-wide text-slate-400 mb-2">
          Question Outline
        </div>

        {/* NEW: show survey title at the top */}
        <div className="px-3 py-2 rounded bg-slate-800 text-slate-100 mb-1">
          <div className="text-[11px] uppercase text-slate-400">Survey</div>
          <div className="truncate" title={surveyTitle || 'Untitled Survey'}>
            {surveyTitle || 'Untitled Survey'}
          </div>
        </div>

        <div className="space-y-1">
          {questions.map((q, i) => (
            <button
              key={q.id}
              className="w-full text-left px-3 py-2 rounded hover:bg-slate-800 truncate"
              title={q.title || `Question ${i + 1}`}
              onClick={() => scrollTo(q.id)}
            >
              {i + 1}. {q.title || 'Untitled question'}
            </button>
          ))}
        </div>
      </nav>
    </aside>
  );
}
