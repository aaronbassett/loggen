import tornado.websocket
import aiofiles

import time


class LogHandler(tornado.websocket.WebSocketHandler):

    connected_clients = set()

    def check_origin(self, origin):
        return True

    def open(self):
        LogHandler.connected_clients.add(self)

    def on_close(self):
        LogHandler.connected_clients.remove(self)

    @classmethod
    def send_updates(cls, message):
        for connected_client in cls.connected_clients:
            connected_client.write_message(message)

    @classmethod
    def log_item(cls, message):
        LogHandler.send_updates(message)


if __name__ == "__main__":
    app = tornado.web.Application([(r"/", LogHandler)])
    app.listen(8000)

    async def tail_log():
        while True:
            async with aiofiles.open("./struct.log", mode="r") as log:
                async for line in log:
                    LogHandler.log_item(line)
                    print(line)

            time.sleep(2)

    loop = tornado.ioloop.IOLoop.current()
    loop.add_callback(tail_log)
    loop.start()
