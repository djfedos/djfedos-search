FROM python:3.9

WORKDIR /usr/src/app

COPY lib_search_sdk.py .
COPY fapi_server.py .
COPY js_web_ui js_web_ui
COPY tests tests

RUN ["/bin/bash", "-c", "python -m venv venv"]
RUN ["/bin/bash", "-c", "source venv/bin/activate && pip install fastapi uvicorn pathlib pytest"]

CMD ["/bin/bash", "-c", "source venv/bin/activate && python fapi_server.py & python -m http.server -d js_web_ui"]
