from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from .constants import TEMPLATE_DIR
from .store import IncomingDataStore

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/monitor")
async def monitor(
    store: Annotated[IncomingDataStore, Depends(IncomingDataStore)],
) -> StreamingResponse:
    async def generator(store: IncomingDataStore):
        while True:
            await store._changed_event.wait()
            yield "data:1\n\n"
            print("sent")

    return StreamingResponse(
        generator(store),
        media_type="text/event-stream",
        headers={"Connection": "keep-alive", "Cache-Control": "no-cache"},
    )
