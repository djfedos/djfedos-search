---
hide:
  - toc
---

There is a FastAPI-based web API in [`fapi_server.py`](https://github.com/djfedos/djfedos-search/blob/main/lib_search_sdk.py). While running, it will reply 
to the queries.

Make sure that the [requirements](https://github.com/djfedos/djfedos-search/blob/main/requirements.txt)
are satisfied and run it.
Then open http://0.0.0.0:18000 in a browser (make sure that JSON content gets 
displayed properly; in Chrome it can be achieved with 
[JSON Viewer extension](https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh)).

Load an example list of tokens by clicking the "recreate" link.

Now you can try other links, especially "query" with any prefixes you like.
You can as well open `js_web_ui/index.html` in a browser and try out a demo suggestion
web app, identical to [this one](http://yairdar.info:8000).

To try out the library with a decent example base of tokens in a convenient web interface
you can also launch `neat_pywebio_app.py`.
