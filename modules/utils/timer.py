class HackTimer:
    def __init__(self, duration_seconds):
        self.duration_seconds = duration_seconds
        self.elapsed = 0

    def tick(self, seconds=1):
        self.elapsed += seconds
        return self.elapsed >= self.duration_seconds

    def progress(self):
        return min(1.0, self.elapsed / max(1, self.duration_seconds))
