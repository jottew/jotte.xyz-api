from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv

import os
import random

load_dotenv()

app = FastAPI(title="jotte.xyz api", description="an api", version=1.0, docs_url="/")
root_dir = os.path.dirname(os.path.realpath(__file__))

app.mount("/hamsters/image", StaticFiles(directory="images/hamsters"), name="hamsters")



@app.get("/hamsters/random")
async def random_hamster(request: Request, redirect: bool = False):
    path = os.path.join(root_dir, "images", "hamsters")
    image = random.choice(os.listdir(path))
    url = str(request.base_url)+"hamsters/image/" + image
    if redirect:
        return RedirectResponse(url)
    return {
        "url": url,
        "notice": "If one of these pictures in the database is your hamster, or you have rights to the image and wish for it to be removed, contact admin@jotte.xyz",
    }


"""
if __name__ == "__main__":
    code = "uvicorn main:app --host 0.0.0.0 --port 80 --reload"
    os.system(code)
"""