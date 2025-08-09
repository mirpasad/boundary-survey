import React from "react";
import CreateSurveyPage from "./pages/CreateSurveyPage";
import { CreateSurveyProviderMock } from "./component/CreateSurveyProvider";

function App() {
  return (
    <CreateSurveyProviderMock>
      <CreateSurveyPage surveySeriesId="abc123" />
    </CreateSurveyProviderMock>
  );
}

export default App;
