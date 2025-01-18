from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID, uuid4

app = FastAPI()

@app.get("/", summary="Корневой маршрут")
def root():
    return {"message": "TEST"}

class PhoneNumber(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Уникальный идентификатор номера телефона")
    number: str = Field(..., pattern=r"^\+?\d{10,15}$", description="Номер телефона в международном формате")

class PhoneNumberCreate(BaseModel):
    number: str = Field(..., pattern=r"^\+?\d{10,15}$", description="Номер телефона в международном формате")

# Хранилище для номеров телефонов
phone_numbers: List[PhoneNumber] = []

@app.get("/phone-numbers", response_model=List[PhoneNumber], summary="Получить все номера телефонов")
def get_phone_numbers():
    #Возвращает список всех телефонных номеров.

    return phone_numbers

@app.post("/phone-numbers", response_model=PhoneNumber, status_code=201, summary="Добавить новый номер телефона")
def create_phone_number(phone: PhoneNumberCreate):
    # Добавляет новый номер телефона в список.

    new_phone = PhoneNumber(**phone.dict())
    phone_numbers.append(new_phone)
    return new_phone

@app.delete("/phone-numbers/{phone_id}", status_code=204, summary="Удалить номер телефона")
def delete_phone_number(phone_id: UUID):
    #Удаляет номер телефона по его ID.

    global phone_numbers
    phone_numbers = [pn for pn in phone_numbers if pn.id != phone_id]
    return None

# запуск python -m uvicorn app.main:app --reload