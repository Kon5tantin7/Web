from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4

app = FastAPI()

# Pydantic модели
class PhoneNumber(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Уникальный идентификатор номера телефона")
    number: str = Field(..., pattern=r"^\+?\d{10,15}$", description="Номер телефона в международном формате")
    description: Optional[str] = Field(None, description="Описание или примечания для номера телефона")

class PhoneNumberCreate(BaseModel):
    number: str = Field(..., pattern=r"^\+?\d{10,15}$", description="Номер телефона в международном формате")
    description: Optional[str] = Field(None, description="Описание или примечания для номера телефона")

class PhoneNumberUpdate(BaseModel):
    number: Optional[str] = Field(None, pattern=r"^\+?\d{10,15}$", description="Новый номер телефона")
    description: Optional[str] = Field(None, description="Новое описание для номера телефона")

# Хранилище телефонных номеров
phone_numbers: List[PhoneNumber] = []

@app.get("/", summary="Корневой маршрут")
def root():
    return {"message": "TEST"}

@app.get("/phone-numbers", response_model=List[PhoneNumber], summary="Получить все номера телефонов")
def get_phone_numbers():
    return phone_numbers
    #Возвращает список всех телефонных номеров.

@app.post("/phone-numbers", response_model=PhoneNumber, status_code=201, summary="Создать новый номер телефона")
def create_phone_number(phone: PhoneNumberCreate):
    new_phone = PhoneNumber(**phone.dict())
    phone_numbers.append(new_phone)
    return new_phone
    # Добавляет новый номер телефона в список.

@app.get("/phone-numbers/{phone_id}", response_model=PhoneNumber, summary="Получить номер телефона по ID")
def get_phone_number(phone_id: UUID):
    for phone in phone_numbers:
        if phone.id == phone_id:
            return phone
    raise HTTPException(status_code=404, detail="Номер телефона не найден")

@app.put("/phone-numbers/{phone_id}", response_model=PhoneNumber, summary="Обновить номер телефона")
def update_phone_number(phone_id: UUID, phone_data: PhoneNumberUpdate):
    for phone in phone_numbers:
        if phone.id == phone_id:
            if phone_data.number:
                phone.number = phone_data.number
            if phone_data.description:
                phone.description = phone_data.description
            return phone
    raise HTTPException(status_code=404, detail="Номер телефона не найден")

@app.delete("/phone-numbers/{phone_id}", status_code=204, summary="Удалить номер телефона")
def delete_phone_number(phone_id: UUID):
    global phone_numbers
    phone_numbers = [phone for phone in phone_numbers if phone.id != phone_id]
    return None
    #Удаляет номер телефона по его ID.

# запуск python -m uvicorn app.main:app --reload
