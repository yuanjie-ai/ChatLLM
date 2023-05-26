from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.cors import CORSMiddleware

from chatllm.api.errors.http_error import http_error_handler
from chatllm.api.errors.validation_error import http422_error_handler
from chatllm.api.routes.api import router as api_router


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(api_router)  # prefix=''

    return application


app = get_application()
