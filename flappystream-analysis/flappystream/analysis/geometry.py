import ujson


class GameLogs:
    def __init__(self, logs: str):
        self.data = [self.flatten_log(ujson.loads(r)) for r in logs]
