from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from utils import getAllBerriesStadistics, sendImage, generateHistogram


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", { "request":request } )

@app.get("/histogram")
async def getHistogram():
    histogram = await generateHistogram()
    if histogram:
        return sendImage("./assets/histogram.png")
    else:
        return sendImage("./assets/wrong.png")


@app.get("/allBerryStats")
async def getAllBerries():
    response = await getAllBerriesStadistics()
    return {"Response": response}

def customOpenapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Poke Berries stats API",
        version="1.0",
        description="This is a very basic API related with the pokemon berries",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://pngset.com/images/download-frutas-do-pokmon-go-image-with-no-background-pinap-berry-pokemon-go-plant-food-vegetable-carrot-transparent-png-2678217.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = customOpenapi