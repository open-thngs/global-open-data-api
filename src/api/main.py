from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import psycopg2 as timescaledb
from dotenv import load_dotenv
import os

# load .env-Datei
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASS,
}

app = FastAPI()

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(os.getcwd(), "favicon.ico")
    return FileResponse(favicon_path)

@app.get("/ping")
def ping():
    try:
        with timescaledb.connect(**DB_CONFIG) as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()
        return {"message": "DB connected", "version": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @app.get("/data")
# def get_data():
#     try:
#         with timescaledb.connect(**DB_CONFIG) as db:
#             with db.cursor() as cursor:
#                 cursor.execute("SELECT * FROM example_table LIMIT 10;")  # Ersetze mit deiner Tabelle
#                 rows = cursor.fetchall()
#         return {"data": rows}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

