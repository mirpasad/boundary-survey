import React, { useState } from 'react';
import { useAuthStore } from '../authStore';
import api from '../axios';
import { useCreateSurvey } from './CreateSurveyProvider';
import QuestionList from './QuestionList';

export default function CreateSurvey() {
  const { token, fetchToken, clearToken } = useAuthStore();
  const {
    // bind to provider state so sidebars update
    surveyTitle, setSurveyTitle,
    surveyDescription, setSurveyDescription,

    loadFromJSON, addNewQuestion,
    mode, setMode, isComplete, responses, resetAnswers,
  } = useCreateSurvey();

  const [isLoading, setIsLoading] = useState(false);
  const [defaultType, setDefaultType] = useState('singleChoice');

  const handleGenerate = async () => {
    const description = (surveyDescription || surveyTitle || '').trim();
    if (description.length < 5) {
      alert('Please enter at least 5 characters in the Title or Description before generating.');
      return;
    }

    try {
      setIsLoading(true);
      if (!token) await fetchToken();
      const res = await api.post('/api/surveys/generate', { description });
      loadFromJSON(res.data);
    } catch (err) {
      console.error('Generate failed:', err);
      if (err?.response?.status === 401) {
        clearToken();
        alert('Session expired. Please try again.');
      } else {
        alert('Failed to generate survey. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitResponses = () => {
    if (!isComplete()) {
      alert('Please answer all questions before submitting.');
      return;
    }
    console.log('SUBMIT RESPONSES', responses);
    alert('Responses captured (see console). Wire this to a POST endpoint next.');
  };

  return (
    <div className="p-6 space-y-6">
      {/* Form header bound to provider */}
      <div className="space-y-3">
        <input
          type="text"
          className="w-full border rounded px-3 py-2"
          placeholder="Survey title (used if description is empty)"
          value={surveyTitle}
          onChange={(e) => setSurveyTitle(e.target.value)}
          maxLength={120}
        />
        <textarea
          className="w-full border rounded px-3 py-2"
          placeholder="Survey description (optional)"
          value={surveyDescription}
          onChange={(e) => setSurveyDescription(e.target.value)}
          maxLength={500}
          rows={3}
        />
      </div>

      {/* Controls row — one line */}
      <div className="flex items-center gap-3 flex-nowrap">
        <div className="flex items-center gap-2">
          <label className="text-sm text-slate-600 whitespace-nowrap">
            Default type for “Add Question”
          </label>
          <select
            className="border rounded px-2 py-2 text-sm"
            value={defaultType}
            onChange={(e) => setDefaultType(e.target.value)}
          >
            <option value="singleChoice">Single choice</option>
            <option value="multipleChoice">Multiple choice</option>
            <option value="openQuestion">Open question</option>
            <option value="shortAnswer">Short answer</option>
            <option value="scale">Scale (1–10)</option>
            <option value="npsScore">NPS (0–10)</option>
          </select>
        </div>

        <button
          className="px-4 py-2 rounded bg-indigo-600 text-white disabled:opacity-50"
          onClick={handleGenerate}
          disabled={isLoading}
        >
          {isLoading ? 'Generating…' : 'Generate Survey (AI)'}
        </button>

        <button
          className="px-4 py-2 rounded bg-slate-200"
          onClick={() => addNewQuestion(defaultType)}
        >
          Add Question
        </button>

        {/* Mode selector on same row */}
        <div className="ml-auto flex items-center gap-2">
          <span className="text-sm text-slate-600">Mode:</span>
          <select
            className="border rounded px-2 py-2 text-sm"
            value={mode}
            onChange={(e) => { resetAnswers(); setMode(e.target.value); }}
          >
            <option value="edit">Edit</option>
            <option value="respond">Respond</option>
          </select>
        </div>
      </div>

      <QuestionList />

      {mode === 'respond' && (
        <div className="pt-2">
          <button
            className="px-4 py-2 rounded bg-emerald-600 text-white"
            onClick={handleSubmitResponses}
          >
            Submit responses
          </button>
        </div>
      )}
    </div>
  );
}
