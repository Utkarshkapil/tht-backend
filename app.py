import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import asyncpg
from dbsetup import setup_database, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


asyncio.run(setup_database())

async def get_db_connection():
    return await asyncpg.connect(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

async def get_documents(request):
    conn = await get_db_connection()
    try:
        documents = await conn.fetch('SELECT id, type, title, position , imageurl FROM documents ORDER BY position')
        return JSONResponse([dict(doc) for doc in documents])
    finally:
        await conn.close()


async def update_documents(request):
    data = await request.json()  
    print(f"Received data: {data}")  
    conn = await get_db_connection()
    
    try:
        async with conn.transaction():
            for doc in data:
                print(f"Updating document: {doc}")  
                
                
                await conn.execute('''
                    UPDATE documents 
                    SET type = $2, title = $3, position = $4, imageurl = $5
                    WHERE id = $1
                ''', doc['id'], doc['type'], doc['title'], doc['position'], doc['imageurl'])
        
        return JSONResponse({"status": "success"})
    finally:
        await conn.close()



routes = [
    Route('/documents', endpoint=get_documents, methods=['GET']),
    Route('/documents', endpoint=update_documents, methods=['POST']),
    
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)