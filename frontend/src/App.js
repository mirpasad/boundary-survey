import React from "react";
import CreateSurveyPage from "./pages/CreateSurveyPage";
import { CreateSurveyProviderMock } from "./component/CreateSurveyProvider";
import { Toaster } from "react-hot-toast";

function App() {
  return (
    <CreateSurveyProviderMock>
      <Toaster position="top-right" />
      <CreateSurveyPage surveySeriesId="abc123" />
    </CreateSurveyProviderMock>
  );
}

export default App;
