from main import Task, TaskCreate, TaskUp
from models import Status
from datetime import datetime

async def test_task():
    task = Task(
        id = 1,
        title = 'task 1',
        description = 'description task 1',
        status = Status.ok,
        priority = 0,
        date = datetime.now()
    )
    assert task.id == 1
    assert task.title == 'task 1'
    assert task.description == 'description task 1'
    assert task.status == Status.ok
    assert task.priority == 0
    assert task.date == datetime.now()

async def test_task_create():
    task = TaskCreate(
        title = 'task 2',
        description = 'description task 2',
        status = Status.waiting,
        priority = 3,
    )
    assert task.title == 'task 2'
    assert task.description == 'description task 2'
    assert task.status == Status.waiting
    assert task.priority == 3

async def test_task_up():
    task = TaskUp(
        title = 'task 3',
        description = 'description task 3',
        status = Status.progress,
        priority = 2,
    )
    assert task.title == 'task 3'
    assert task.description == 'description task 3'
    assert task.status == Status.progress
    assert task.priority == 2