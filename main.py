from fastapi import FastAPI
from pydantic import BaseModel


class Transport(BaseModel):
    vin: str
    reg_number: str | None = None
    sts_number: str | None = None


app = FastAPI()


@app.get("/check-transport/")
async def check_auto(transport: Transport):
    return transport
