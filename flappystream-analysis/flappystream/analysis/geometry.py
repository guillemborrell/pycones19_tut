import ujson


class Game:
    @staticmethod
    def flatten_log(log):

    def __init__(self, logs: str):
        self.data = [self.flatten_log(ujson.loads(r)) for r in logs]

        # Check if the data corresponds to the same game
