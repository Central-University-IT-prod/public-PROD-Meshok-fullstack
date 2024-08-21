import fastapi
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from api.routers_answer import answers_router
from api.routers_organizations import organizations_router
from api.routers_users import users_router

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://feedbacker.online",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    path="/",
    response_class=RedirectResponse,
    include_in_schema=False
)
async def read_root():
    """
    Redirect to docs page
    """

    return "/docs"


app.include_router(users_router)
app.include_router(organizations_router)
app.include_router(answers_router)

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host="0.0.0.0"
    )
