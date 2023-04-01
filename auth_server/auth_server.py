import json
import requests
from dotenv import load_dotenv
from os import environ as env
from flask import Flask, render_template, request
from redis import Redis

load_dotenv()

app = Flask(__name__)

r_client = Redis(
    host=env["REDIS_HOST"],
    port=env["REDIS_PORT"],
    password=env["REDIS_PASSWORD"],
    decode_responses=True,
)


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        data = json.loads(request.data)

        r_client.set(
            f'{data["tg_id"]}_tokens',
            json.dumps(
                {
                    "access_token": data["access_token"],
                    "refresh_token": data["refresh_token"],
                }
            ),
        )

        url = f"https://api.telegram.org/bot{env['BOT_TOKEN']}/sendMessage"

        params = {
            "chat_id": data["tg_id"],
            "text": "Successful sign in! \u2705",
        }

        res = requests.post(url, data=params)

        return "ok"
    return render_template(
        "sign_in.html",
        tg_id=request.args["tg_id"],
        api_url=env["API_AUTH_URL"],
    )


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    return render_template(
        "sign_up.html",
        tg_id=request.args["tg_id"],
        api_url=env["API_AUTH_URL"],
    )


if __name__ == "__main__":
    app.run(host="auth")
