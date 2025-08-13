// src/component/QuestionItem.jsx
import React from 'react';
import { useCreateSurvey } from './CreateSurveyProvider';
import RenderMultipleOptions from './RenderMultipleOptions';
import RenderCheckboxOptions from './RenderCheckboxOptions';

export default function QuestionItem({ question, index }) {
  const {
    mode,
    responses, setAnswer,
    handleQuestionTitleChange,
    handleQuestionTypeChange,
    handleDelete,
    handleDuplicate,
    toggleSaved,
  } = useCreateSurvey();

  const isChoice = ['multipleChoice', 'singleChoice'].includes(question.type);
  const isEditMode = mode === 'edit';
  const isRespondMode = mode === 'respond';

  const checkedMulti = (qid, text) =>
    Array.isArray(responses[qid]) && responses[qid].includes(text);

  const toggleMulti = (qid, text, checked) => {
    setAnswer(qid, (prev => {
      const curr = Array.isArray(responses[qid]) ? responses[qid] : [];
      return checked ? [...curr, text] : curr.filter((x) => x !== text);
    })());
  };

  return (
    <div id={`q-${question.id}`} className="bg-white border rounded-lg p-4 shadow-sm">
      {/* Header: title + type */}
      <div className="flex flex-col md:flex-row md:items-center gap-3 mb-4">
        <input
          className="flex-1 border rounded px-3 py-2 text-[15px]"
          type="text"
          placeholder="Question title"
          value={question.title || ''}
          onChange={(e) => handleQuestionTitleChange(index, e.target.value)}
          disabled={!isEditMode || question.saved}
        />
        <select
          className="border rounded px-2 py-2 text-sm md:w-56"
          value={question.type}
          onChange={(e) => handleQuestionTypeChange(index, e.target.value)}
          disabled={!isEditMode || question.saved}
        >
          <option value="singleChoice">Single choice</option>
          <option value="multipleChoice">Multiple choice</option>
          <option value="openQuestion">Open question</option>
          <option value="shortAnswer">Short answer</option>
          <option value="scale">Scale (1–10)</option>
          <option value="npsScore">NPS (0–10)</option>
        </select>
      </div>

      {/* BODY
         EDIT mode:
           - if saving/locked (saved=true), show a READ-ONLY PREVIEW of options/inputs (never blank)
           - if editing (saved=false), show editable option editors
         RESPOND mode:
           - show interactive inputs
      */}
      {isChoice && (
        <>
          {isEditMode && question.saved && (
            <ul className="pl-1 space-y-1 text-slate-700">
              {(question.options || []).map((opt) => (
                <li key={opt.id} className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full border" aria-hidden /> {opt.text}
                </li>
              ))}
            </ul>
          )}

          {isEditMode && !question.saved && (
            <div className="space-y-2">
              {question.type === 'singleChoice' &&
                (question.options || []).map((opt, i) => (
                  <RenderMultipleOptions
                    key={opt.id}
                    questionIndex={index}
                    optionIndex={i}
                    option={opt}
                    saved={question.saved}
                  />
                ))}
              {question.type === 'multipleChoice' &&
                (question.options || []).map((opt, i) => (
                  <RenderCheckboxOptions
                    key={opt.id}
                    questionIndex={index}
                    optionIndex={i}
                    option={opt}
                    saved={question.saved}
                  />
                ))}
            </div>
          )}

          {isRespondMode && (
            <div className="space-y-2 pl-1">
              {question.type === 'singleChoice' &&
                (question.options || []).map((opt) => (
                  <label key={opt.id} className="flex items-center gap-2">
                    <input
                      type="radio"
                      name={question.id}
                      value={opt.text}
                      checked={responses[question.id] === opt.text}
                      onChange={(e) => setAnswer(question.id, e.target.value)}
                    />
                    <span>{opt.text}</span>
                  </label>
                ))}

              {question.type === 'multipleChoice' &&
                (question.options || []).map((opt) => (
                  <label key={opt.id} className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={checkedMulti(question.id, opt.text)}
                      onChange={(e) => toggleMulti(question.id, opt.text, e.target.checked)}
                    />
                    <span>{opt.text}</span>
                  </label>
                ))}
            </div>
          )}
        </>
      )}

      {question.type === 'openQuestion' && (
        <>
          {isRespondMode ? (
            <textarea
              className="w-full border rounded px-3 py-2"
              placeholder="Your answer"
              value={responses[question.id] || ''}
              onChange={(e) => setAnswer(question.id, e.target.value)}
            />
          ) : (
            <div className="pl-1 text-slate-500 text-sm italic">Free-form answer (long text)</div>
          )}
        </>
      )}

      {question.type === 'shortAnswer' && (
        <>
          {isRespondMode ? (
            <input
              className="w-full border rounded px-3 py-2"
              placeholder="Your answer"
              value={responses[question.id] || ''}
              onChange={(e) => setAnswer(question.id, e.target.value)}
            />
          ) : (
            <div className="pl-1 text-slate-500 text-sm italic">Short answer (single line)</div>
          )}
        </>
      )}

      {/* Scale with numbers visible (1–10 / 0–10) */}
      {question.type === 'scale' && (
        <div className="pl-1 flex gap-1 mt-1">
          {[...Array(10)].map((_, i) => {
            const val = i + 1;
            const active = responses[question.id] === val;
            return (
              <button
                key={i}
                type="button"
                disabled={mode !== 'respond'}
                onClick={() => setAnswer(question.id, val)}
                className={`w-7 h-7 grid place-items-center rounded text-[12px] font-medium
                  ${active ? 'bg-amber-500 text-white' : 'bg-amber-300/80 text-slate-800'}
                `}
                aria-label={`Rate ${val}`}
                title={`${val}`}
              >
                {val}
              </button>
            );
          })}
        </div>
      )}

      {question.type === 'npsScore' && (
        <div className="pl-1 flex gap-1 mt-1">
          {[...Array(11)].map((_, i) => {
            const active = responses[question.id] === i;
            return (
              <button
                key={i}
                type="button"
                disabled={mode !== 'respond'}
                onClick={() => setAnswer(question.id, i)}
                className={`w-7 h-7 grid place-items-center rounded text-[12px] font-medium
                  ${active ? 'bg-emerald-600 text-white' : 'bg-emerald-300/80 text-slate-800'}
                `}
                aria-label={`NPS ${i}`}
                title={`${i}`}
              >
                {i}
              </button>
            );
          })}
        </div>
      )}

      {/* Actions */}
      <div className="mt-4 flex flex-wrap gap-2">
        {/* Saved (locked) → show only Edit in Edit mode */}
        {isEditMode && question.saved && (
          <button
            className="px-3 py-1.5 rounded bg-slate-600 text-white text-sm"
            onClick={() => toggleSaved(index, false)}
          >
            Edit
          </button>
        )}

        {/* Editing (unlocked) → show Save + Duplicate + Delete in Edit mode */}
        {isEditMode && !question.saved && (
          <>
            <button
              className="px-3 py-1.5 rounded bg-emerald-600 text-white text-sm"
              onClick={() => toggleSaved(index, true)}
              disabled={!question.title}
              title={!question.title ? 'Add a title first' : 'Save question'}
            >
              Save
            </button>

            <button
              className="px-3 py-1.5 rounded bg-indigo-600 text-white text-sm"
              onClick={() => handleDuplicate(index)}
              disabled={!question.title}
              title={!question.title ? 'Add a title first' : 'Duplicate question'}
            >
              Duplicate
            </button>

            <button
              className="px-3 py-1.5 rounded bg-rose-600 text-white text-sm"
              onClick={() => handleDelete(index)}
            >
              Delete
            </button>
          </>
        )}
      </div>
    </div>
  );
}
