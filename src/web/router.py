from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from ipc import ConcentrationStatus, MonitorMsg

from .constants import TEMPLATE_DIR
from .store import IncomingDataStore

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


def format_monitor_msg(msg: MonitorMsg) -> str:
    body: dict[str, int | float | str] = {}
    if isinstance(msg.payload, ConcentrationStatus):
        body["type"] = "concentration_status"
        body["overall_score"] = msg.payload.overall_score
        body["sleeping_confidence"] = msg.payload.sleeping_confidence
    else:
        body["type"] = "error"
        body["error_type"] = msg.payload.type
        body["error_msg"] = msg.payload.msg
    return f"data:{str(body)}\n\n"


@router.get("/monitor")
async def monitor(
    store: Annotated[IncomingDataStore, Depends(IncomingDataStore)],
) -> StreamingResponse:
    async def generator(store: IncomingDataStore):
        while True:
            await store.wait_for_change()
            if store.latest_monitor_msg:
                yield format_monitor_msg(store.latest_monitor_msg)

    return StreamingResponse(
        generator(store),
        media_type="text/event-stream",
        headers={"Connection": "keep-alive", "Cache-Control": "no-cache"},
    )
