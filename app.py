from quart import Quart, render_template, request, redirect, url_for
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import time
import os

app = Quart(__name__)

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text(""" 
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """))

@app.before_serving
async def startup_tasks():
    await init_db()
    time.sleep(1)

@app.route('/')
async def index():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(text('SELECT * FROM items'))
            items = result.fetchall()
    return await render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
async def add_item():
    form_data = await request.form  
    name = form_data['name']
    async with async_session() as session:
        async with session.begin():
            await session.execute(text('INSERT INTO items (name) VALUES (:name)'), {"name": name})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
