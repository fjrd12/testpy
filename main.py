from url_shortener.adapters import url_mapping
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from flask import jsonify
app = FastAPI()


class UrlMap(BaseModel):
    url_short: str
    url_long: str


@app.post("/add")
def create(url_map: UrlMap):
    """Create a translatable address"""
    url_obj = url_mapping()
    url_obj.add(url_map.url_short, url_map.url_long)
    return {"message": "Url mapping created"}


@app.get("/get")
def get(url_short: str):
    """Get translateable address"""
    url_obj = url_mapping()
    translated = url_obj.get(url_short)
    return translated


@app.get("/{full_path:path}")
def catch_all(request: Request, full_path: str):
    url_obj = url_mapping()
    long_url = str(request.url)
    result = url_obj.get(long_url)
    if result is None:
        raise HTTPException(status_code=404, detail="The short url {} does not found".format(long_url))
    else:
        url_obj.update_count(result.url_short)
    return RedirectResponse(result.url_long, status_code=303)


@app.delete("/delete")
def delete_url(url_short: str):
    url_obj = url_mapping()
    url_obj.remove(url_short)
    return {"message": "Record has been deleted"}

