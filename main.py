from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime
from database import get_async_session
from models import tasks_table, Status
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

class Task(BaseModel):
    id: int
    title: str
    description: str | None
    status: Status
    priority: int
    date: datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None
    status: Status
    priority: int

class TaskUp(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status  | None = None
    priority: int | None = None

app = FastAPI()

@app.post('/task/')
async def create_task(new_task: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    task = insert(tasks_table).values(**new_task.model_dump())
    await session.execute(task)
    await session.commit()
    return {"status": "success"}
@app.get('/task/')
async def read_task(session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(tasks_table))
    return [list(x) for x in res]
@app.get('/task/title/{title}')
async def read_task_title(title: str, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(tasks_table).where(tasks_table.c.title == title))
    return [list(x) for x in res]
@app.get('/task/id/{id}')
async def read_task_id(id: int, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(tasks_table).where(tasks_table.c.id == id))
    return [list(x) for x in res]
@app.delete('/task/{title}')
async def delete_task(title: str, session: AsyncSession = Depends(get_async_session)):
    await session.execute(delete(tasks_table).where(tasks_table.c.title == title))
    await session.commit()
    return {"status": "success"}
@app.put('/task/{title}')
async def up_task(title: str, new_data: TaskUp, session: AsyncSession = Depends(get_async_session)):
    if new_data.title is not None:
        await session.execute(update(tasks_table).where(tasks_table.c.title == title).values(title = new_data.title))
    if new_data.description is not None:
        await session.execute(update(tasks_table).where(tasks_table.c.title == title).values(description = new_data.description))
    if new_data.status is not None:
        await session.execute(update(tasks_table).where(tasks_table.c.title == title).values(status = new_data.status))
    if new_data.priority is not None:
        await session.execute(update(tasks_table).where(tasks_table.c.title == title).values(priority = new_data.priority))
    await session.commit()
    return {"status": "success"}
@app.get('/task/sort/')
async def sort_task(by: str, desc: bool = False, session: AsyncSession = Depends(get_async_session)):
    if by == 'title':
        if desc:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.title.desc()))
        else:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.title))
    elif by == 'description':
        if desc:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.description.desc()))
        else:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.description))
    elif by == 'status':
        if desc:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.status.desc()))
        else:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.status))
    elif by == 'priority':
        if desc:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.priority.desc()))
        else:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.priority))
    elif by == 'date':
        if desc:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.date.desc()))
        else:
            res = await session.execute(select(tasks_table).order_by(tasks_table.c.date))
    await session.commit()
    return [list(x) for x in res]
@app.get('/task/search/')
async def search_task(s: str, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(tasks_table).where(tasks_table.c.title.contains(s) | tasks_table.c.description.contains(s)))
    return [list(x) for x in res]
@app.get('/task/top/{n}/')
async def top_task(n: int, session: AsyncSession = Depends(get_async_session)):
    res = await session.execute(select(tasks_table).order_by(tasks_table.c.priority.desc()).limit(n))
    return [list(x) for x in res]