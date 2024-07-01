from fastapi.exceptions import RequestValidationError
from url_shortener.adapters import url_mapping, logger
from fastapi import FastAPI, Request, HTTPException as GlobalStarletteHTTPException
from fastapi.responses import RedirectResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
from flask import jsonify
from datetime import datetime
app = FastAPI()


class UrlMap(BaseModel):
    url_short: str
    url_long: str


@app.middleware("http")
async def log_transaction_filter(request: Request, call_next):
    start_time = datetime.now()
    method_name= request.method
    qp_map = request.query_params
    pp_map = request.path_params
    with open("request_log.txt", mode="a") as reqfile:
        content = f"method: {method_name}, query param: {qp_map}, path params: {pp_map} received at {datetime.now()} \n"
        reqfile.write(content)
        response = await call_next(request)
        process_time = datetime.now() - start_time
        response.headers["X-Time-Elapsed"] = str(process_time)
        return response


@app.post("/add")
async def create(url_map: UrlMap):
    """Create a translatable address"""
    url_obj = url_mapping()
    try:
        url_obj.add(url_map.url_short, url_map.url_long)
    except Exception as excep:
        logger.error(excep.args)
        raise GlobalStarletteHTTPException(status_code=500, detail="{}".format(excep.args))
    return JSONResponse(status_code=200, content={"message": "Url mapping created"})


@app.get("/get")
async def get(url_short: str):
    """Get translateable address"""
    url_obj = url_mapping()
    translated = url_obj.get(url_short)
    return translated


@app.get("/{full_path:path}")
async def catch_all(request: Request, full_path: str):
    url_obj = url_mapping()
    long_url = str(request.url)
    result = url_obj.get(long_url)
    if result is None:
        raise GlobalStarletteHTTPException(status_code=404, detail="The short url {} does not found".format(long_url))
    else:
        url_obj.update_count(result.url_short)
    return RedirectResponse(result.url_long, status_code=303)


@app.delete("/delete")
async def delete_url(url_short: str):
    url_obj = url_mapping()
    try:
        url_obj.remove(url_short)
    except Exception as exp:
        raise GlobalStarletteHTTPException(status_code=500, detail="{}".format(url_obj.remove(url_short)))
    return {"message": "Record has been deleted"}


@app.exception_handler(GlobalStarletteHTTPException)
async def global_exception_handler(req: Request, ex: str):
    return PlainTextResponse(f"Error message: {ex}", status_code=ex.status_code)

@app.exception_handler(RequestValidationError)
async def validationerror_exception_handler(req: Request, ex: str):
    return PlainTextResponse(f"Error message: {str(ex)}", status_code=400)
