from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response

from dotenv import load_dotenv

import os
import random
import asyncio

load_dotenv()

api_keys = []
db = None

app = FastAPI(title="jotte.xyz api", description="an api", version=1.0, docs_url="/")
root_dir = os.path.dirname(os.path.realpath(__file__))

app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/hamsters/random")
async def random_hamster(request: Request, redirect: bool = False):
    path = os.path.join(root_dir, "images", "hamsters")
    image = random.choice(os.listdir(path))
    url = str(request.base_url)+"images/hamsters/" + image
    if redirect:
        return RedirectResponse(url)
    return {"url": url}

if __name__ == "__main__":
    code = "uvicorn app:app --host 0.0.0.0 --port 80 --reload"
    os.system(code)
