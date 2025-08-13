// src/component/QuestionList.jsx
import React from 'react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import QuestionItem from './QuestionItem';
import { useCreateSurvey } from './CreateSurveyProvider';

export default function QuestionList() {
  const { questions, onDragEnd } = useCreateSurvey();

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <Droppable droppableId="questions" direction="vertical">
        {(provided) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
            className="space-y-3"
          >
            {questions.map((q, index) => (
              <Draggable key={q.id} draggableId={q.id} index={index}>
                {(providedDraggable) => (
                  <div
                    ref={providedDraggable.innerRef}
                    {...providedDraggable.draggableProps}
                    {...providedDraggable.dragHandleProps}
                  >
                    <QuestionItem question={q} index={index} />
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
}
