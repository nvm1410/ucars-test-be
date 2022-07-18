import datetime as dt
from fastapi import FastAPI, status, HTTPException, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy import null
from database import SessionLocal
import models
import base64
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CarBrand(BaseModel):  # serializer
    id: str
    name: str
    description: str
    is_active: bool
    logo: str
    model_count: int
    last_update: dt.datetime

    class Config:
        orm_mode = True


db = SessionLocal()


@app.get('/brands', response_model=List[CarBrand], status_code=200)
def get_all_brands():
    brands = db.query(models.CarBrand).all()

    return brands


@app.get('/brands/{brand_id}', response_model=CarBrand, status_code=status.HTTP_200_OK)
def get_brand(brand_id: str):
    brand = db.query(models.CarBrand).filter(
        models.CarBrand.id == brand_id).first()
    return brand


@app.post('/brands', response_model=CarBrand,
          status_code=status.HTTP_201_CREATED)
def create_brand(id: str = Form(), name: str = Form(), description: str = Form(), is_active: bool = Form(), model_count: int = Form(), logo: str = Form()):
    # db_brand = db.query(models.CarBrand).filter(
    #     models.CarBrand.name == name).first()

    # if db_brand is not None:
    #     raise HTTPException(status_code=400, detail="Car brand already exists")
    new_brand = models.CarBrand(
        id=id,
        name=name,
        description=description,
        is_active=is_active,
        logo=logo,
        model_count=model_count,
        last_update=dt.datetime.now()
    )

    db.add(new_brand)
    db.commit()

    return new_brand


@app.put('/brands/{brand_id}', response_model=CarBrand, status_code=status.HTTP_200_OK)
def update_brand(brand_id: str, name: str = Form(), description: str = Form(), is_active: bool = Form(), logo: str = Form()):
    brand_to_update = db.query(models.CarBrand).filter(
        models.CarBrand.id == brand_id).first()

    brand_to_update.name = name
    brand_to_update.description = description
    brand_to_update.is_active = is_active
    brand_to_update.logo = logo
    brand_to_update.last_update=dt.datetime.now()

    db.commit()

    return brand_to_update


@app.delete('/brands/{brand_id}')
def delete_brand(brand_id: str):
    brand_to_delete = db.query(models.CarBrand).filter(
        models.CarBrand.id == brand_id).first()

    if brand_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

    db.delete(brand_to_delete)
    db.commit()

    return brand_to_delete


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
