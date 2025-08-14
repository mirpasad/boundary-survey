import React, { createContext, useContext, useMemo, useState } from 'react';
import { nanoid } from 'nanoid';

const CreateSurveyContext = createContext(null);
export const useCreateSurvey = () => {
  const ctx = useContext(CreateSurveyContext);
  if (!ctx) throw new Error('useCreateSurvey must be used within CreateSurveyProvider');
  return ctx;
};

function makeQuestion(type = 'singleChoice') {
  const q = { id: nanoid(), type, title: '', saved: false };
  if (['multipleChoice', 'singleChoice'].includes(type)) {
    q.options = [
      { id: nanoid(), text: 'Option 1' },
      { id: nanoid(), text: 'Option 2' },
    ];
  }
  return q;
}

export function CreateSurveyProvider({ children }) {
  const [surveyTitle, setSurveyTitle] = useState('');
  const [surveyDescription, setSurveyDescription] = useState('');
  const [questions, setQuestions] = useState([]);

  // mode & responses
  const [mode, setMode] = useState('edit'); // 'edit' | 'respond'
  const [responses, setResponses] = useState({});

  const setAnswer = (qid, value) => setResponses((prev) => ({ ...prev, [qid]: value }));
  const resetAnswers = () => setResponses({});

  // Reset entire survey
  const resetSurvey = () => {
    setSurveyTitle('');
    setSurveyDescription('');
    setQuestions([]);
    setMode('edit');
    resetAnswers();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Editing actions
  const addNewQuestion = (type = 'singleChoice') => setQuestions((p) => [...p, makeQuestion(type)]);
  const handleQuestionTitleChange = (i, t) =>
    setQuestions((p) => { const n=[...p]; n[i]={...n[i], title:t}; return n; });
  const handleQuestionTypeChange = (i, newType) =>
    setQuestions((p) => {
      const n=[...p]; const q={...n[i], type:newType};
      if (['multipleChoice','singleChoice'].includes(newType)) {
        q.options = q.options && Array.isArray(q.options) ? q.options : [{ id:nanoid(), text:'Option 1'}];
      } else { delete q.options; }
      n[i]=q; return n;
    });
  const handleOptionChange = (qi, oi, text) =>
    setQuestions((p) => { const n=[...p]; const q={...n[qi]};
      const opts=[...(q.options||[])]; opts[oi]={...opts[oi], text}; q.options=opts; n[qi]=q; return n; });
  const handleDeleteOption = (qi, oi) =>
    setQuestions((p) => { const n=[...p]; const q={...n[qi]};
      q.options=(q.options||[]).filter((_,i)=>i!==oi); n[qi]=q; return n; });
  const handleDuplicate = (i) =>
    setQuestions((p) => { const n=[...p]; const o=n[i];
      const dup={...o, id:nanoid(), saved:false, options:o.options?o.options.map(x=>({id:nanoid(), text:x.text})):undefined};
      n.splice(i+1,0,dup); return n; });
  const handleDelete = (i) => {
    setQuestions((p) => p.filter((_,idx)=>idx!==i));
    setResponses((r) => { const copy={...r}; const qid=questions[i]?.id; if(qid) delete copy[qid]; return copy; });
  };
  const toggleSaved = (i, saved) =>
    setQuestions((p) => { const n=[...p]; n[i]={...n[i], saved}; return n; });

  const onDragEnd = (result) => {
    if (!result.destination) return;
    const from = result.source.index, to = result.destination.index;
    if (from === to) return;
    setQuestions((p) => { const n=[...p]; const [m]=n.splice(from,1); n.splice(to,0,m); return n; });
  };

  // Backend → UI
  const loadFromJSON = (payload) => {
    const allowed = new Set(['multipleChoice','singleChoice','openQuestion','shortAnswer','scale','npsScore']);
    setSurveyTitle(payload?.title || surveyTitle || '');
    setSurveyDescription(payload?.description || '');
    const normalized = (payload?.questions || [])
      .filter((q) => q && allowed.has(q.type))
      .map((q) => ({
        id: nanoid(),
        type: q.type,
        title: q.title || '',
        saved: true,
        ...(q.options ? { options: q.options.map((t) => ({ id: nanoid(), text: String(t) })) } : {}),
      }));
    setQuestions(normalized);
    resetAnswers();     // start at 0% on new survey
    setMode('respond');
  };

  // Validation & progress
  const isQuestionAnswered = (q) => {
    const ans = responses[q.id];
    switch (q.type) {
      case 'singleChoice': return typeof ans === 'string' && ans.length>0;
      case 'multipleChoice': return Array.isArray(ans) && ans.length>0;
      case 'openQuestion':
      case 'shortAnswer': return typeof ans === 'string' && ans.trim().length>0;
      case 'scale': return typeof ans === 'number' && ans>=1 && ans<=10;
      case 'npsScore': return typeof ans === 'number' && ans>=0 && ans<=10;
      default: return false;
    }
  };
  const answeredCount = useMemo(
    () => questions.reduce((acc, q) => acc + (isQuestionAnswered(q) ? 1 : 0), 0),
    [questions, responses]
  );
  const totalCount = questions.length;
  const progressPercent = totalCount === 0 ? 0 : Math.round((answeredCount / totalCount) * 100);
  const isComplete = () => totalCount > 0 && answeredCount === totalCount;

  const value = useMemo(() => ({
    // state
    surveyTitle, setSurveyTitle,
    surveyDescription, setSurveyDescription,
    questions,

    // edit actions
    addNewQuestion, handleQuestionTitleChange, handleQuestionTypeChange,
    handleOptionChange, handleDeleteOption, handleDuplicate, handleDelete,
    toggleSaved, onDragEnd,

    // payload -> UI
    loadFromJSON,

    // mode & responses
    mode, setMode,
    responses, setAnswer, resetAnswers,

    // validation/progress
    isQuestionAnswered, isComplete,
    answeredCount, totalCount, progressPercent,

    // reset all
    resetSurvey,
  }), [surveyTitle, surveyDescription, questions, mode, responses, answeredCount, totalCount, progressPercent]);

  return <CreateSurveyContext.Provider value={value}>{children}</CreateSurveyContext.Provider>;
}

// Back-compat exports
export const useCreateSurveyProvider = useCreateSurvey;
export const CreateSurveyProviderMock = CreateSurveyProvider;
