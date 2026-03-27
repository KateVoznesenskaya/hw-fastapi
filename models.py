from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Enum
from datetime import datetime
import enum

metadata = MetaData()

class Status(enum.Enum):
    waiting = 'waiting'
    progress = 'in progress'
    ok = 'ok'

tasks_table = Table(
    'tasks_table',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('description', String, default=''),
    Column('status', Enum(Status), default=Status.waiting),
    Column('priority', Integer, default=0),
    Column('date', TIMESTAMP, default=datetime.now),
)