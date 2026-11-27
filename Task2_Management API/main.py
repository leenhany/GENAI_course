from fastapi import FastAPI,HTTPException
from models import Task
from schemas import TaskCreate,TaskUpdate,TakeResponse
from dataclasses import asdict

app=FastAPI(title="Task management API")

# dictionary to carry the task number and value from Task type
tasks: dict[int,Task]={}

#--->post
@app.post("/tasks",response_model=TakeResponse)

def create_task(task_data:TaskCreate):
    task_id=len(tasks)+1
    #conver task to dict
    task_dict=task_data.model_dump()
    #creatae dataclass
    new_task=Task(task_id=task_id,**task_dict)
    #store tha task
    tasks[task_id]=new_task
    #convert dataclass to dict
    response_dict=asdict(new_task)
    #convert dict to pydantic reponse
    return TakeResponse(**response_dict)

#---->Get
@app.get("/tasks",response_model=list[TakeResponse])
def get_tasks():
    res=[]
    for task in tasks.values():
        #convert data class to dict
        task_dict=asdict(task)
        #conver dict to pydantic 
        resp=TakeResponse(**task_dict)
        res.append(resp)
    return res    

#-----> Delete
@app.delete("/tasks/{task_id}")
def delete_task(task_id:int):
    if task_id not in tasks:
        raise HTTPException(status_code=404,detail=f"Task {task_id} Not found")
    del tasks[task_id]
    return{"message":f"Task {task_id} deleted successfully"}

#--->patch
@app.patch("/tasks/{task_id}",response_model=TakeResponse)
def edit_task(task_id:int,updated_data:TaskUpdate):
    if task_id not in tasks:
            raise HTTPException(status_code=404,detail=f"Task {task_id} Not found")

    #get only fields updated by user
    updated_dict=updated_data.model_dump(exclude_unset=True)
    #get existing task
    ex_task=tasks[task_id]
    #convert ex task to dict
    ex_dict=asdict(ex_task)
    #merge ex task with updated data
    updated_dict={**ex_dict,**updated_dict}
    #create new Task dataclass
    updated_task=Task(**updated_dict)
    #replace old task with new in database
    tasks[task_id]=updated_task
    #convert to dict and response model
    response_dict=asdict(updated_task)

    return TakeResponse(**response_dict)





