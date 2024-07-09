import random
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# 데이터베이스 연결 설정
DATABASE_URL = ""
engine = create_engine(DATABASE_URL, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def make_short_url(link):
    # make random string with 6 characters
    short_url = ''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 6))
    return short_url

def save_link(db: Session, link):
    # 기존 name 이 있는지 확인합니다 있다면 short_url을 반환합니다.
    result = db.execute(text("SELECT * FROM links WHERE name = :link"), {"link": link}).fetchall()
    if len(result) > 0:
        short_url = result[0][2]
        return short_url
    else:
        short_url = make_short_url(link)
        db.execute(text("INSERT INTO links (name, url) VALUES (:link, :short_url)"), {"link": link, "short_url": short_url})
        db.commit()
        return short_url

# FastAPI 객체를 생성합니다.
app = FastAPI()

origins = [
    "http://s.udm.kr",
    "http://s.udm.kr:8000",
    "http://s.udm.kr/createlink",
    "http://s.udm.kr/createlink:8000",
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET 요청을 처리하는 함수를 등록합니다.
@app.get("/createlink/")
def get_link(link: str, db: Session = Depends(get_db)):
    short_url = "s.udm.kr/"+save_link(db, link)
    return {
        "short_url": short_url
    }

# uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="s.udm.kr", port=8000)
