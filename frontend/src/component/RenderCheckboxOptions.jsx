import React from 'react';
import { useCreateSurvey } from './CreateSurveyProvider';

export default function RenderCheckboxOptions({
  questionIndex,
  optionIndex,
  option,
  saved,
}) {
  const { handleOptionChange, handleDeleteOption } = useCreateSurvey();

  return (
    <div className="flex items-center gap-2">
      <input
        type="checkbox"
        disabled
        className="w-4 h-4 text-indigo-600"
      />
      <input
        className="flex-1 border rounded px-3 py-2"
        placeholder={`Option ${optionIndex + 1}`}
        value={option.text || ''}
        onChange={(e) => handleOptionChange(questionIndex, optionIndex, e.target.value)}
        disabled={saved}
      />
      {!saved && (
        <button
          className="px-2 py-1 text-sm rounded bg-rose-50 text-rose-700 border"
          onClick={() => handleDeleteOption(questionIndex, optionIndex)}
          title="Remove option"
        >
          Remove
        </button>
      )}
    </div>
  );
}
