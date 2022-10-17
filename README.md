# NeteaseLyric

获取网易云音乐歌词，并转化为 srt 格式。可以部署到 vercel，也可以本地运行

## 本地运行

安装依赖

```shell
pip install -r requirements.txt
```

运行

```shell
python api/index.py
```

## 获取歌词

### srt 格式

```
http://127.0.0.1:5000/lyric?id=65800
```

或

```
http://127.0.0.1:5000/lyric?id=65800&format=srt
```

### lrc 格式

```
http://127.0.0.1:5000/lyric?id=65800&format=lrc
```

### txt 格式

```
http://127.0.0.1:5000/lyric?id=65800&format=txt
```
