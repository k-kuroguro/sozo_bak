from threading import Thread

from ipc import ZmqPublisher, ZmqSubscriber
from local import App as LocalApp
from web import App as WebApp


def main():
    socket_addr = "ipc:///tmp/monitoring"
    topic = "monitoring"
    publisher = ZmqPublisher(socket_addr, topic)
    subscriber = ZmqSubscriber(socket_addr, topic)

    webapp = WebApp(subscriber)
    localapp = LocalApp(publisher)

    web_thread = Thread(
        target=webapp.run,
        kwargs={"host": "0.0.0.0", "port": 8080, "threaded": True},
    )
    local_thread = Thread(target=localapp.run)

    web_thread.start()
    local_thread.start()

    web_thread.join()
    local_thread.join()


if __name__ == "__main__":
    main()
