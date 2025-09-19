from fastapi import APIRouter,Depends,HTTPException
from app.database.database import get_db
from app.schemas.task import TaskGet,TaskCreate,TaskUpdate
from app.models.task import Task
from app.models.user import User
from sqlalchemy.orm import Session
from app.routers.user import get_current_user
router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/",response_model=TaskGet)
def create_task(tasks: TaskCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_task = Task(title=tasks.title, done=tasks.done, owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/",response_model=list[TaskGet])
def get_task(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.owner_id==current_user.id).all()

@router.get("/{task_id}",response_model=TaskGet)
def get_task(task_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.owner_id==current_user.id, Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}",response_model=TaskGet)
def get_task(task_id: int,task_update: TaskUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.owner_id==current_user.id, Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.done is not None:
        task.done = task_update.done

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def get_task(task_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.owner_id==current_user.id, Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": f"Task {task_id} deleted"}