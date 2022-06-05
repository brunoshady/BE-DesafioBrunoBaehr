import json
import typing

from starlette.responses import Response


# https://stackoverflow.com/questions/67783530/is-there-a-way-to-pretty-print-prettify-a-json-response-in-fastapi
class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")
