__version__ = "Ver. 1.0"

import uvicorn
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from apis import root
from app.exceptions import APIException
from app.util import convertStruct

def create_app():
    app = FastAPI(
        title="Arender API",
        description="remove background from anime images",
        version=__version__,
        debug=False
    )

    @app.exception_handler(APIException)
    async def unicorn_exception_handler(request: Request, exc: APIException):
        return UJSONResponse(
            status_code=exc.system.get("code"),
            content=await convertStruct(
                source=exc.source,
                status=exc.status,
                message=exc.system.get("message"),
                code=exc.system.get("code")
            )
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router=root, prefix="/api")
    return app

app = create_app()
