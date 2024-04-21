class OrderPicker:
    def __init__(self, lineOrder=None, positionY=None):
        if lineOrder is not None:
            self.LineOrder = 0
            self.PositionY = 0
        else:
            self.LineOrder = lineOrder
            self.PositionY = positionY