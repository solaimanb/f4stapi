from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

class Quiz(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

quizes = []

@app.post("/quizes/", response_model=Quiz)
def create_quiz(quiz: Quiz):
    quiz.id = uuid4()
    quizes.append(quiz)
    return quiz

@app.get("/quizes", response_model=List[Quiz])
def read_quizes():
    return quizes

@app.get("/quizes/{quiz_id}", response_model=Quiz)
def read_quiz(quiz_id: UUID):
    for quiz in quizes:
        if quiz.id == quiz_id:
            return quiz
    raise HTTPException(status_code=404, detail="quiz not found")

@app.put("/quizes/{quiz_id}", response_model=Quiz)
def update_quiz(quiz_id: UUID, quiz_update: Quiz):
    for idx, quiz in enumerate(quizes):
        if quiz.id == quiz_id:
            update_quiz = quiz.copy(update=quiz_update.dict(exclude_unset=True))
            quizes[idx] = update_quiz
            return update_quiz
    raise HTTPException(status_code=404, detail="quiz not found")

@app.delete("/quizes/{quiz_id}")
def delete_quiz(quiz_id: UUID):
    for idx, quiz in enumerate(quizes):
        if quiz.id == quiz_id:
            return quizes.pop(idx)
    raise HTTPException(status_code=404, detail="quiz not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)