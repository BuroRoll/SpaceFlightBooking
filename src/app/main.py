import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.v1.users.auth import router as user_router
from routers.v1.booking.booking import router as booking_router
from database import engine, Base

# space_booking
# 6zP\2P+\3^%x9g

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(booking_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE', 'OPTIONS', 'PUT'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
                   'Access-Control-Allow-Origin',
                   'Authorization', 'Origin', 'Accept'],
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
