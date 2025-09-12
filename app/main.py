from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker
from .scheduler import start_scheduler

DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Book(Base):
	__tablename__ = "books"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	release_date = Column(String, index=True)
	publisher = Column(String, index=True)
	isbn = Column(String, index=True)
	bisac = Column(String, index=True)
	status = Column(String, index=True)
	genre = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books BR Releases")
templates = Jinja2Templates(directory="templates")

class BookOut(BaseModel):
	title: str
	release_date: Optional[str] = None
	publisher: Optional[str] = None
	isbn: Optional[str] = None
	bisac: Optional[str] = None
	status: Optional[str] = None
	genre: Optional[str] = None

	class Config:
		from_attributes = True

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/books", response_model=List[BookOut])
async def list_books(
	editora: Optional[str] = Query(None, alias="publisher"),
	genero: Optional[str] = Query(None, alias="genre"),
	status: Optional[str] = None,
):
	with SessionLocal() as db:
		stmt = select(Book)
		if editora:
			stmt = stmt.where(Book.publisher.ilike(f"%{editora}%"))
		if genero:
			stmt = stmt.where(Book.genre.ilike(f"%{genero}%"))
		if status:
			stmt = stmt.where(Book.status.ilike(f"%{status}%"))
		rows = db.execute(stmt).scalars().all()
		return [BookOut.model_validate(r) for r in rows]

@app.on_event("startup")
async def seed_and_schedule():
	# seed minimal sample once
	sample = [
		dict(title="A Rainha da rua Paissandu", release_date="2025-09", publisher="Intrínseca", isbn="", bisac="BIO005000", status="lançado", genre="Biografia"),
		dict(title="Nós Já Moramos Aqui", release_date="2025-09", publisher="Intrínseca", isbn="", bisac="FIC015000", status="pré-venda", genre="Terror"),
		dict(title="A Dama da Morte", release_date="2025-01-27", publisher="Arqueiro", isbn="978-6555651236", bisac="FIC014000", status="lançado", genre="Histórica"),
	]
	with SessionLocal() as db:
		existing = db.execute(select(Book)).scalars().first()
		if not existing:
			for s in sample:
				db.add(Book(**s))
			db.commit()
	# start daily scheduler
	start_scheduler()