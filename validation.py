from pydantic import BaseModel, field_validator
from typing import Union
from models import User

class UserSchema(BaseModel):
    username:str
    password: Union[str, float]

    @field_validator('username')
    def validate_name(cls,username):
        if username.isalpha():
            return username
        raise ValueError(f"El nombre solo debe contener letras, no podes escribir {username}")
    
class LoginSchema(BaseModel):
    username:str
    password: Union[str, float]

class QuestionAnswerSchema(BaseModel):
    question_content: Union[str, float]
    answer_content: Union[str, float]