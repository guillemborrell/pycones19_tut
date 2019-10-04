from pynng import Sub0


if __name__ == "__main__":
    with Sub0(dial="tcp://127.0.0.1:54321") as socket:
        print('Connecting...')
        socket.subscribe(b"")
        try:
            while True:
                message = socket.recv()
                print(message)

        except KeyboardInterrupt:
            print("Bye")
