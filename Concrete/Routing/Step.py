class Step:
    def __init__(self, lineOrderMovement, positionYMovement):
        self.LineOrderMovement = lineOrderMovement
        self.PositionYMovement = positionYMovement

    @staticmethod
    def GetTotalDistance(distanceBetweenBlocks, distanceBetweenLines, steps):
        last_line = steps[0].LineOrderMovement
        distance = 0

        for step in steps:
            if last_line != step.LineOrderMovement:
                distance = distance + abs(step.LineOrderMovement - last_line) * distanceBetweenLines

            last_line = step.LineOrderMovement
            distance = distance + abs(step.PositionYMovement) * distanceBetweenBlocks

        return distance

    def __str__(self):
        return f"MovL: {self.LineOrderMovement}, MovY: {self.PositionYMovement}"