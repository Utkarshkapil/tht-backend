import asyncio
import asyncpg


DB_NAME = "tht"
DB_USER = "postgres"
DB_PASSWORD = "typebot"
DB_HOST = "localhost"
DB_PORT = "5432"

async def create_database():
    conn = await asyncpg.connect(
        database="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    try:
        await conn.execute(f"CREATE DATABASE {DB_NAME}")
    except asyncpg.exceptions.DuplicateDatabaseError:
        print(f"Database '{DB_NAME}' already exists.")
    finally:
        await conn.close()

async def create_table():
    conn = await asyncpg.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                type VARCHAR(50) UNIQUE NOT NULL,
                title VARCHAR(100) NOT NULL,
                position INTEGER NOT NULL,
                imageUrl VARCHAR(255)  -- Added imageUrl column
            )
        ''')
    finally:
        await conn.close()

async def populate_sample_data():
    conn = await asyncpg.connect(
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    try:
        sample_data = [
            {"type": "bank-draft", "title": "Bank Draft", "position": 0, "imageUrl": "https://media1.tenor.com/m/Ce_EIG6qg0kAAAAC/happy-happy-happy-happy.gif"},
            {"type": "bill-of-lading", "title": "Bill of Lading", "position": 1, "imageUrl": "https://media1.tenor.com/m/Dtbh5RBNNvUAAAAC/happy-catto-cats.gif"},
            {"type": "invoice", "title": "Invoice", "position": 2, "imageUrl": "https://media1.tenor.com/m/ZBKOEgi5JfoAAAAC/cat-wave.gif"},
            {"type": "bank-draft-2", "title": "Bank Draft 2", "position": 3, "imageUrl": "https://media1.tenor.com/m/5BYK-WS0__gAAAAd/cool-fun.gif"},
            {"type": "bill-of-lading-2", "title": "Bill of Lading 2", "position": 4, "imageUrl": "https://media1.tenor.com/m/j5rPRPBwSOMAAAAd/cat-smacking-other-cat-cat.gif"}
        ]

        for doc in sample_data:
            await conn.execute('''
                INSERT INTO documents (type, title, position, imageUrl) 
                VALUES ($1, $2, $3, $4) 
                ON CONFLICT (type) DO NOTHING
            ''', doc['type'], doc['title'], doc['position'], doc['imageUrl'])
    finally:
        await conn.close()

async def check_connection():
    try:
        conn = await asyncpg.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        await conn.close()
        print("Database connection successful.")
        return True
    except Exception as e:
        print(f"Unable to connect to the database: {str(e)}")
        return False

async def setup_database():
    await create_database()
    await create_table()
    await populate_sample_data()
    if await check_connection():
        print("Database setup completed successfully.")
    else:
        print("Database setup failed.")

if __name__ == "__main__":
    asyncio.run(setup_database())
