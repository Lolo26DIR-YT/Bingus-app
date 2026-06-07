class RiskEngine:
    def __init__(self, base_risk=3, profile=None):
        self.base_risk = max(1, min(base_risk, 5))
        self.profile = profile
        self.value = int(self.base_risk * 12)
        self.tick_count = 0

    def start(self):
        self.value = int(self.base_risk * 12)
        self.tick_count = 0

    def next_tick(self):
        self.tick_count += 1
        increment = 3 + (self.tick_count // 2)
        if self.profile:
            adjusted = self.profile.reduce_risk(increment)
        else:
            adjusted = increment
        self.value = min(100, self.value + adjusted)
        return self.value
