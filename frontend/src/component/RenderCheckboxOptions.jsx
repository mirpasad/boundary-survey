import React from "react";
import { useCreateSurveyProvider } from "./CreateSurveyProvider";
import { XIcon } from "./Icons.jsx";
import { motion } from "framer-motion";

const RenderCheckboxOptions = ({
  questionIndex,
  question,
  option,
  optionIndex,
  dupList,
}) => {
  const { handleOptionChange, handleDeleteOption } = useCreateSurveyProvider();

  const handleDeleteClick = () => {
    handleDeleteOption(questionIndex, option.id);
  };

  return (
    <motion.div 
      initial={{ opacity: 0.9 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.2, delay: optionIndex * 0.03 }}
      key={option.id} 
      className="flex my-3 gap-3 mb-4 items-center"
    >
      <div className="relative flex items-center justify-center">
        <div className="w-[22px] h-[22px] border-2 rounded-[3px] border-[#6851a7]" />
        {option && (
          <motion.div 
            initial={{ scale: 0.5 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.15 }}
            className="absolute w-[12px] h-[12px] rounded-[1px] bg-[#6851a7]" 
          />
        )}
      </div>

      <motion.input
        whileFocus={{ boxShadow: "0 0 0 1px rgba(104, 81, 167, 0.1)" }}
        type="text"
        value={option.text}
        required
        placeholder="Enter option text..."
        disabled={question.saved}
        onChange={(e) =>
          handleOptionChange(questionIndex, optionIndex, e.target.value)
        }
        className={`text-base p-2 border rounded-lg grow bg-transparent outline-none transition-all duration-200 ${
          (dupList.includes(optionIndex)) 
            ? "border-red-500 focus:ring-1 focus:ring-red-300" 
            : question.saved 
              ? "border-[#6851a7]/30" 
              : "border-[#6851a7] focus:ring-1 focus:ring-[#6851a7]/20 focus:border-transparent"
        }`}
      />
      
      {!question.saved && question.options.length > 2 && (
        <motion.button
          whileHover={{ scale: 1.05, backgroundColor: "rgba(239, 68, 68, 0.1)" }}
          whileTap={{ scale: 0.97 }}
          className="w-[32px] h-[32px] cursor-pointer flex justify-center items-center rounded-full hover:bg-red-50 transition-all duration-200"
          disabled={question.saved}
          onClick={handleDeleteClick}
          type="button"
        >
          <XIcon className="text-red-500" />
        </motion.button>
      )}
    </motion.div>
  );
};

export default RenderCheckboxOptions;
