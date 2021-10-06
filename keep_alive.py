from flask import Flask
from threading import Thread

app = Flask("")


@app.route("/")
def ontxt():
    return "I'm back and running!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# What he wrote down, the whole crowd
