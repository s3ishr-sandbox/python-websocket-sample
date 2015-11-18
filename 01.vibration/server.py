import tornado.ioloop
import tornado.web
import tornado.websocket

class MainHandler(tornado.web.RequestHandler):
    """同じディレクトリにあるindex.htmlを返すクラス"""
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")

# コネクション一覧をまとめておく変数
conn = []

class WebSocket(tornado.websocket.WebSocketHandler):
    """WebSocketで接続されたときの動作を定義するクラス"""

    def open(self):
        """接続されたらコネクション一覧に追加する"""
        print("[WS] Open")
        if self not in conn:    # 二重登録防止
            conn.append(self)

    def on_message(self, message):
        """ブラウザから通信を受け取ったときの処理"""
        print("[WS] Receive: ", message)
        for c in conn:    # 登録されたコネクション全てに送信 
            c.write_message(message)

    def on_close(self):
        """切断されたときの後始末"""
        print("[WS] Close")
        if self in conn:
            conn.remove(self)

app = tornado.web.Application([
    (r"/", MainHandler), # "http://a.b.c.d:8080/"
    (r"/ws", WebSocket), # "http://a.b.c.d:8080/ws"
])

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
