from fastapi import FastAPI, Form, UploadFile,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

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
    print(image,title,price,description,place,insertAt)
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
    

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

