import React, { createContext, useContext, useState, useCallback } from "react";

const CreateSurveyContext = createContext();

export const CreateSurveyProviderMock = ({ children }) => {
  const [surveyTitle, setSurveyTitle] = useState("My Survey Title");
  const [surveyDescription, setSurveyDescription] = useState("This is a sample survey.");
  const [questions, setQuestions] = useState([]);
  const [dupList, setDupList] = useState([]);
  const [isAddingOption, setIsAddingOption] = useState(false);
  const defaultQuestionType = "shortAnswer";

  const addNewQuestion = (type = defaultQuestionType) => {
    const newQuestion = {
      id: Date.now() + Math.random(),
      type,
      title: "",
      saved: false,
      options:
        type === "multipleChoice" || type === "singleChoice"
          ? [
              { id: Date.now() + Math.random(), text: "" },
              { id: Date.now() + Math.random() + 1, text: "" },
            ]
          : [],
    };
    setQuestions((prev) => [...prev, newQuestion]);
  };

  const handleDeleteQuestion = (index) => {
    setQuestions((prev) => prev.filter((_, i) => i !== index));
  };

  const handleAddOption = useCallback(
    (questionIndex) => {
      if (isAddingOption) return;
      setIsAddingOption(true);

      setQuestions((prev) => {
        const newQuestions = [...prev];
        if (!newQuestions[questionIndex].options) newQuestions[questionIndex].options = [];
        newQuestions[questionIndex].options.push({
          id: Date.now() + Math.random(),
          text: "",
        });
        setTimeout(() => setIsAddingOption(false), 0);
        return newQuestions;
      });
    },
    [isAddingOption]
  );

  const handleTitleChange = (questionIndex, title) => {
    setQuestions((prev) => {
      const newQuestions = [...prev];
      newQuestions[questionIndex].title = title;
      return newQuestions;
    });
  };

  const handleQuestionTypeChange = (questionIndex, type) => {
    setQuestions((prev) => {
      const newQuestions = [...prev];
      newQuestions[questionIndex].type = type;

      if (type === "multipleChoice" || type === "singleChoice") {
        if (!newQuestions[questionIndex].options || newQuestions[questionIndex].options.length < 2) {
          newQuestions[questionIndex].options = [
            { id: Date.now() + Math.random(), text: "" },
            { id: Date.now() + Math.random() + 1, text: "" },
          ];
        }
      } else {
        newQuestions[questionIndex].options = [];
      }

      return newQuestions;
    });
  };

  const handleOptionChange = (questionIndex, optionIndex, value) => {
    setQuestions((prev) => {
      const newQuestions = [...prev];
      if (newQuestions[questionIndex].options) {
        newQuestions[questionIndex].options[optionIndex].text = value;
      }
      return newQuestions;
    });
  };

  const handleSaveQuestion = (questionIndex) => {
    setQuestions((prev) => {
      const newQuestions = [...prev];
      newQuestions[questionIndex].saved = true;
      return newQuestions;
    });
  };

  const handleEditQuestion = (questionIndex) => {
    setQuestions((prev) => {
      const newQuestions = [...prev];
      newQuestions[questionIndex].saved = false;
      return newQuestions;
    });
  };

  const handleDuplicate = (questionIndex) => {
    const mkId = () => (crypto?.randomUUID?.() || (Date.now() + Math.random()).toString());
    const q = questions[questionIndex];
    const duplicated = {
      ...q,
      id: mkId(),
      saved: false,
      options: (q.options || []).map(o => ({ id: mkId(), text: o.text })),
    };
    setQuestions((prev) => [...prev, duplicated]);
  };

  const handleDeleteOption = (questionIndex, optionId) => {
    setQuestions((prev) => {
      const newQuestions = [...prev];
      if (newQuestions[questionIndex].options) {
        const optionIndex = newQuestions[questionIndex].options.findIndex((option) => option.id === optionId);
        if (optionIndex !== -1) newQuestions[questionIndex].options.splice(optionIndex, 1);
      }
      return newQuestions;
    });
  };

  const onDragEnd = (result) => {
    if (!result.destination) return;
    const items = Array.from(questions);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);
    setQuestions(items);
  };

  const handleCreateSurvey = () => {
    console.log("Mock create survey:", {
      title: surveyTitle,
      description: surveyDescription,
      questions,
    });
  };

  const loadFromJSON = (survey) => {
    const mkId = () => (crypto?.randomUUID?.() || (Date.now() + Math.random()).toString());
    setSurveyTitle(survey.title || "");
    setSurveyDescription(survey.description || "");
    const allowed = new Set(["multipleChoice","singleChoice","openQuestion","shortAnswer","scale","npsScore"]);
    const normalized = (survey.questions || [])
      .filter(q => q?.type && allowed.has(q.type) && q.title)
      .map((q) => ({
        id: mkId(),
        type: q.type,
        title: q.title,
        saved: false,
        options: (q.options || []).map((opt) => ({ id: mkId(), text: opt })),
      }));
    setQuestions(normalized);
  };

  return (
    <CreateSurveyContext.Provider
      value={{
        surveyTitle,
        setSurveyTitle,
        surveyDescription,
        setSurveyDescription,
        questions,
        setQuestions,
        defaultQuestionType,
        addNewQuestion,
        handleDeleteQuestion,
        handleAddOption,
        handleTitleChange,
        handleQuestionTypeChange,
        handleOptionChange,
        handleSaveQuestion,
        handleEditQuestion,
        handleDuplicate,
        handleDeleteOption,
        onDragEnd,
        dupList,
        handleCreateSurvey,
        loadFromJSON,
      }}
    >
      {children}
    </CreateSurveyContext.Provider>
  );
};

export const useCreateSurveyProvider = () => useContext(CreateSurveyContext);
