import pandas as pd


class GameLogs:
    def __init__(self, logs: pd.DataFrame):
        self.logs = logs

    def append(self, logs: pd.DataFrame):
        self.logs = pd.concat([self.logs, logs])

    def relative(self):
        return pd.DataFrame({
            'game': self.logs.uuid.str[:8],
            'dx': self.logs.pipes_position_x - self.logs.bird_x,
            'dy': self.logs.bird_y - self.logs.pipes_position_y,
            'speed': self.logs.bird_speed,
            'alive': self.logs.alive}
        )[lambda df: df.dx + self.logs.pipes_w + self.logs.bird_radius > 0]
