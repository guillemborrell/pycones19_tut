from pynng import Sub0
from streamz import Stream
import ujson
from flappystream.analysis import flatten_record


if __name__ == "__main__":
    with Sub0(dial="tcp://127.0.0.1:54321") as socket:
        print('Connecting...')
        socket.subscribe(b"")
        try:
            stream = Stream()
            stream.map(ujson.loads).flatten().map(flatten_record).sink(print)

            while True:
                stream.emit(socket.recv())

        except KeyboardInterrupt:
            print("Bye")
