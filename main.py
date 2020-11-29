"""Module for downloading youtube videos!"""
from pytube import YouTube
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route("/downloadvideo", methods=["POST"])
def download_video():
    """ Endpoint to download youtube video """
    try:
        data = request.json
        link = data["link"]
        # """Take link as param and downloads that video in current dir"""
        print("Download video event has been triggered!")
        print("We are trying to download: {}".format(link))
        YouTube(link).streams.first().download()
        return {"message": "Video downloaded succesfully", "success": True}
    except Exception as err:
        return {
            "message": "Error while downloading",
            "success": False,
            "Error": str(err),
        }


if __name__ == "__main__":
    app.run(debug=True)
