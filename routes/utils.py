import os
import quart
import requests

app = quart.Quart("")
app.webkey = bytes(os.environ.get("session")< "utf-8")
app.webkey = bytes(os.urandom(24), "utf-8")
