from flask import Flask, Response, request
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lyric import Lyric

app = Flask(__name__)


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "music.163.com",
    "Referer": "http://music.163.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}


@app.route("/")
def home():
    return Response("success", mimetype="text/plain")


@app.route("/lyric", methods=["GET", "POST"])
def lyric():
    if request.method == 'POST':
        song_id = request.form.get("id")
        format = request.form.get("format")
    elif request.method == 'GET':
        song_id = request.args.get("id")
        format = request.args.get("format")

    lyric = ""
    try:
        res = requests.post("http://music.163.com/api/song/lyric?id=" +
                            song_id + "&lv=-1", headers=headers).json()
        if res['code'] == 200:
            lyric = res['lrc']['lyric']
            if format == 'lrc':
                pass
            elif format == 'txt':
                lyric = Lyric().parse_lrc(lyric).to_txt()
            elif format == 'srt':
                lyric = Lyric().parse_lrc(lyric).to_srt()
            else:
                lyric = Lyric().parse_lrc(lyric).to_srt()
    except:
        lyric = ""

    return Response(lyric, mimetype="text/plain")


if __name__ == '__main__':
    app.run()
