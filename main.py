from fastapi import FastAPI, Form, UploadFile,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3
# from pymongo import MongoClient
# import json

# # MongoDB 연결 설정
# client = MongoClient('mongodb://localhost:27017/')  # 로컬 MongoDB 인스턴스에 연결
# db = client['memo_app']  # 사용할 데이터베이스 이름
# collection = db['notes']  # 사용할 컬렉션 이름

# # JSON 데이터 파일 로드
# with open('data.json', 'r') as file:
#     data = json.load(file)

# # 데이터 삽입
# if isinstance(data, list):  # JSON 데이터가 리스트 형식인 경우
#     collection.insert_many(data)
# else:  # JSON 데이터가 단일 객체인 경우
#     collection.insert_one(data)

# print("데이터 삽입 완료")

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

# IF NOT EXISTS 문법은 해당 테이블이 없을 때만 생성하는 SQL문이다.
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
	            id INTEGER PRIMARY KEY,
	            title TEXT NOT NULL,
	            image BLOB,
	            price INTEGER NOT NULL,
	            description TEXT,
	            place TEXT NOT NULL,
	            insertAt INTEGE NOT NULL
            );
            """)

app = FastAPI()

@app.post('/items')
async def create_itme(image:UploadFile,
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
):

    image_bytes = await image.read()
    
    # f문자열 파이썬에서 사용하는 방법
    cur.execute(f"""
                INSERT INTO items (title, image, price, description, place, insertAt)
                VALUES ('{title}','{image_bytes.hex()}', {price},'{description}','{place}',{insertAt})
                """)
    con.commit()
    # print(image,title,price,description,place,insertAt)
    return '200'

@app.get('/items')
async def get_items():
    # 컬럼명도 같이 가져옴
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    rows = cur.execute(f"""
                       SELECT * FROM items;
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    # 16진법
    image_bytes = cur.execute(f"""
                          SELECT image FROM items WHERE id={item_id}
                          """).fetchone()[0]
    
    return Response(content=bytes.fromhex(image_bytes), media_type='image/*')

@app.post('/signup')
def signup(id:Annotated[str,Form()],
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit()
    print(id,password)
    return '200'

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

