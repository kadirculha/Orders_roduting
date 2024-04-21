class ExcelData:
    def __init__(self, productNo, line, blockY, chargeAddress, blockX, category):
        self.ProductNo = productNo
        self.Line = line
        self.BlockY = blockY
        self.ChargeAddress = chargeAddress
        self.BlockX = blockX
        self.Category = category

    @staticmethod
    def GetWithAddress(address, productNo, category):
        line = int(address[1:3])
        blockY = address[3:4]
        chargeAddress = int(address[4:6])
        blockX = address[6:7]

        return ExcelData(productNo, line, blockY, chargeAddress, blockX, category)

    def __str__(self):
        return f"ProductNo: {self.ProductNo}, Line: {self.Line}, BlockY: {self.BlockY}, ChargeAddress: {self.ChargeAddress}, BlockX: {self.BlockX}, Category: {self.Category},"