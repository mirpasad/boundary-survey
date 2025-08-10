import React from "react";
import CreateSurveyPage from "./pages/CreateSurveyPage";
import { CreateSurveyProviderMock } from "./component/CreateSurveyProvider";
import { Toaster } from "react-hot-toast";

// Main application component that sets up providers and renders the survey page
function App() {
  return (
    <CreateSurveyProviderMock>
      <Toaster position="top-right" /> {/* Notification toaster */}
      <CreateSurveyPage surveySeriesId="abc123" /> {/* Survey page */}
    </CreateSurveyProviderMock>
  );
}

export default App; // Export App component
