class Line:
    def __init__(self, order=None, filled_blocks=None):
        if order is not None:
            self.Order = order
            self.FilledBlocks = filled_blocks
        else:
            self.Order = 0
            self.FilledBlocks = []

    def __str__(self):
        return f"Order: {self.Order}, FilledBlocks: {self.FilledBlocks}"