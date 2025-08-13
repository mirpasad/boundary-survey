import React from 'react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import { useCreateSurvey } from './CreateSurveyProvider';

export default function CreateSurveyContent() {
  const { questions, onDragEnd, surveyTitle } = useCreateSurvey();

  const scrollTo = (qid) => {
    const el = document.getElementById(`q-${qid}`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="p-3">
      {/* NEW: show survey title card */}
      <div className="px-3 py-2 rounded bg-white border mb-2">
        <div className="text-sm font-semibold truncate" title={surveyTitle || 'Untitled Survey'}>
          {surveyTitle || 'Untitled Survey'}
        </div>
        <div className="text-xs text-slate-500">overview</div>
      </div>

      <DragDropContext onDragEnd={onDragEnd}>
        <Droppable droppableId="sidebarList" direction="vertical">
          {(provided) => (
            <div ref={provided.innerRef} {...provided.droppableProps} className="space-y-2">
              {questions.map((q, index) => (
                <Draggable key={`s-${q.id}`} draggableId={`s-${q.id}`} index={index}>
                  {(providedDraggable) => (
                    <div
                      ref={providedDraggable.innerRef}
                      {...providedDraggable.draggableProps}
                      {...providedDraggable.dragHandleProps}
                      className="px-3 py-2 rounded bg-white border cursor-pointer"
                      onClick={() => scrollTo(q.id)}   // NEW: clickable to jump
                      title={q.title || `Question ${index + 1}`}
                    >
                      <div className="text-sm font-medium line-clamp-1">
                        {q.title || `Question ${index + 1}`}
                      </div>
                      <div className="text-xs text-slate-500">{q.type}</div>
                    </div>
                  )}
                </Draggable>
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
}
