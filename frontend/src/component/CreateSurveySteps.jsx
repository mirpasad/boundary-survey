import React from "react";
import { StepCirlcleIcon, StepsFillIcon } from "./Icons";

const CreateSurveySteps = ({ children, step }) => {
    return (
    <div className="rounded-[20px] border-2 border-light-gray bg-white p-2 flex flex-col ">
      <div className="flex justify-between items-center">
        <div className="flex flex-col items-center gap-3 pl-1 max-w-[35px]">
          <span className="flex justify-center items-center w-full h-full">
            <StepsFillIcon />
          </span>
        </div>

        <span className="w-full h-[1px] bg-antiquate inline-block"></span>
        <div className="flex flex-col items-center max-w-[30px] gap-3">
          {step > 1 ? (
            <span className="flex justify-center items-center w-full h-full">
              <StepsFillIcon />
            </span>
          ) : (
            <span className="border-antiquate border-2 rounded-full min-h-[25px] min-w-[25px] bg-[#F1F1F1] flex justify-center items-center">
              <StepCirlcleIcon />
            </span>
          )}
        </div>
        <span className="w-full h-[1px] bg-antiquate inline-block"></span>
        <div className="flex flex-col items-center gap-3 pr-1 max-w-[35px]">
          {step > 2 ? (
            <span className="flex justify-center items-center w-full h-full">
              <StepsFillIcon />
            </span>
          ) : (
            <span className="border-antiquate border-2 rounded-full min-h-[25px] min-w-[25px] bg-[#F1F1F1] flex justify-center items-center">
              <StepCirlcleIcon />
            </span>
          )}
        </div>
      </div>
      <div className="flex justify-between items-center text-[13px] mt-1 font-switzer text-primary text-center">
        <h3 className="text-center">Design</h3>
        <h3 className="text-center pr-4">Preview</h3>
        <h3>Publish</h3>
      </div>
      <div className="mt-4">{children}</div>
    </div>
  );
};

export default CreateSurveySteps;
