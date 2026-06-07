class OperatorProfile:
    def __init__(self, name):
        self.name = name
        self.modifier = 1.0
        if name == "Novice":
            self.modifier = 1.2
        elif name == "Intermédiaire":
            self.modifier = 1.0
        elif name == "Expert":
            self.modifier = 0.85
        elif name == "Ghost":
            self.modifier = 0.7

    def adjust_duration(self, base_seconds):
        return int(base_seconds * self.modifier)

    def reduce_risk(self, risk_value):
        if self.name == "Ghost":
            return max(0, risk_value - 4)
        if self.name == "Expert":
            return max(0, risk_value - 2)
        return risk_value
