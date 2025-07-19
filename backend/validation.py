from pydantic import BaseModel, field_validator
from typing import Union


class UserSchema(BaseModel):
    username: str
    password: Union[str, int]
    confirm_password: Union[str, int]

    @field_validator('username')
    @classmethod
    def validate_name(cls, username):
        if username.isalpha():
            return username
        raise ValueError(f"El nombre solo debe contener letras, no podés escribir '{username}'")

    @field_validator('confirm_password')
    @classmethod
    def validate_password_match(cls, confirm_password, info):
        password = info.data.get('password')
        if password != confirm_password:
            raise ValueError("Las contraseñas no coinciden")
        return confirm_password
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, password):
        if isinstance(password, (str, int)) and len(str(password)) >= 8:
            return password
        raise ValueError("La contraseña debe tener al menos 8 caracteres")


class LoginSchema(BaseModel):
    username:str
    password: Union[str, int]

class FlashCardSchema(BaseModel):
    question_content: Union[str, int]
    answer_content: Union[str, int]

class FillBlankSchema(BaseModel):
    sentence: Union[str, int]
    hidden_word: Union[str, int]

class NotesSchema(BaseModel):
    title: Union[str, int]
    content: Union[str, int]