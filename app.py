from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

import os
import random

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="jotte.xyz api",
    description="an api",
    version=1.0,
    docs_url="/"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.mount(
    "/images",
    StaticFiles(directory="images"),
    name="images"
)

root_dir = os.path.dirname(os.path.realpath(__file__))


@app.get("/hamsters/random")
@limiter.limit("5/second")
def random_hamster(request: Request, redirect: bool = False):
    path = os.path.join(root_dir, "images", "hamsters")
    image = random.choice(os.listdir(path))
    url = "https://jotte.xyz/api/images/hamsters/"+image
    if redirect:
        return RedirectResponse(url)
    return {"url": url}

if __name__ == '__main__':
    os.system("uvicorn app:app --host 0.0.0.0 --port 8008 --reload --root-path /api/") # --root-path is unneccesary if you dont have the api running on a 
                                                                                       # nginx reverse proxy on a symmetric path