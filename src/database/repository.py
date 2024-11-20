from typing import List

from fastapi.params import Depends
from sqlalchemy import select, delete
from sqlalchemy.orm import  Session
from sqlalchemy.testing.pickleable import User

from database.connection import get_db
from database.orm import ToDo

