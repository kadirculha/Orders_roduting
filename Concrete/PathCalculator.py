import math
from Concrete.Routing import SShape, MidPoint, LargestGap
from Concrete.Routing.Line import Line
from Concrete.Routing.OrderPicker import OrderPicker
from Concrete.Routing.ShortestPath import ShortestPath  
from Concrete.Routing.Step import Step

class PathCalculator:
    @staticmethod
    def GetDistance(excelDatas, lineChargeAddressHeight, beginLineOrder, beginPositionY, targetLineOrder, algorithm):
        # Excel verilerini gruplayarak işlemek için
        filteredDataByOrder = PathCalculator.GetGrouppedDataByExcelData(excelDatas, lineChargeAddressHeight)

        # Üst ve alt hatları almak için
        topLines = PathCalculator.GetLines(True, filteredDataByOrder)
        bottomLines = PathCalculator.GetLines(False, filteredDataByOrder)

        # Başlangıç konumunu belirlemek için OrderPicker oluşturuyoruz
        orderPicker = OrderPicker(beginLineOrder, beginPositionY)
        steps = []

        # Üst hatlar varsa, belirtilen algoritmayı kullanarak rotayı al
        if len(topLines) > 0:
            if algorithm == "SShape":
                steps.extend(SShape.SShapeRouting.GetRoute(orderPicker, topLines, lineChargeAddressHeight, -1, -1))  # Düzeltme: -1 -> orderPicker.LineHeight ve -1 -> orderPicker.PositionY
            elif algorithm == "MidPoint":
                steps.extend(MidPoint.MidPointRouting.GetRoute(orderPicker, topLines, lineChargeAddressHeight, -1, -1))  # Düzeltme: -1 -> orderPicker.LineHeight ve -1 -> orderPicker.PositionY
            elif algorithm == "LargestGap":
                steps.extend(LargestGap.LargestGapRouting.GetRoute(orderPicker, topLines, lineChargeAddressHeight, -1, orderPicker.PositionY))  # Düzeltme: -1 -> orderPicker.LineHeight ve -1 -> orderPicker.PositionY
        else:
            # Üst hat yoksa, sadece başlangıç konumunu ekleyin
            steps.append(Step(beginLineOrder, lineChargeAddressHeight + 1))

        # OrderPicker'ı sıfırlayın ve alt hatlar için benzer adımları alın
        orderPicker.PositionY = 0
        if len(bottomLines) > 0:
            if algorithm == "SShape":
                steps.extend(SShape.SShapeRouting.GetRoute(orderPicker, bottomLines, lineChargeAddressHeight, -1, orderPicker.PositionY))  # Düzeltme: -1 -> orderPicker.LineHeight ve 0 -> orderPicker.PositionY
            elif algorithm == "MidPoint":
                steps.extend(MidPoint.MidPointRouting.GetRoute(orderPicker, bottomLines, lineChargeAddressHeight, -1, orderPicker.PositionY))  # Düzeltme: -1 -> orderPicker.LineHeight ve 0 -> orderPicker.PositionY
            elif algorithm == "LargestGap":
                steps.extend(LargestGap.LargestGapRouting.GetRoute(orderPicker, bottomLines, lineChargeAddressHeight, -1, orderPicker.PositionY))  # Düzeltme: -1 -> orderPicker.LineHeight ve 0 -> orderPicker.PositionY

        # Hedef hattına en kısa yol için adımları al
        orderPicker.PositionY = lineChargeAddressHeight + 1
        steps.extend(ShortestPath.GetRoute(orderPicker, targetLineOrder, lineChargeAddressHeight + 1, lineChargeAddressHeight))

        return {
            "OrderPicker": orderPicker,
            "Steps": steps
        }

    @staticmethod
    def GetLines(isTop, filteredData):
        lines = []
        for item in filteredData:
            if item["Top"] == isTop:
                charge_addresses = [item["ChargeAddress"]]

                found = False

                foundLine = None
                for i in range(len(lines)):
                    if lines[i].Order == item["Line"]:
                        found = True
                        foundLine = lines[i]
                        break

                if found == False:
                    lines.append(Line(item["Line"], charge_addresses))
                else:
                    foundLine.FilledBlocks.extend(charge_addresses)

        return lines

    @staticmethod
    def GetGrouppedDataByExcelData(excelDatas, lineChargeAddressHeight):
        result = []

        for excelData in excelDatas:
            new_item = {
                "Line": excelData["Line"],  # Burada item["Line"] yerine excelData["Line"] kullanılmalı
                "Top": math.ceil(excelData["ChargeAddress"] / 2) <= lineChargeAddressHeight,
                "ChargeAddress": math.ceil(excelData["ChargeAddress"] / 2) % lineChargeAddressHeight,
                "BlockX": excelData["BlockX"],
                "BlockY": excelData["BlockY"],
                "ProductNo": excelData["ProductNo"]
            }

            found = False
            for r in result:
                if r["Line"] == new_item["Line"] and r["Top"] == new_item["Top"] and r["ChargeAddress"] == new_item["ChargeAddress"]:
                    r["Items"].append({
                        "BlockX": new_item["BlockX"],
                        "BlockY": new_item["BlockY"],
                        "ProductNo": new_item["ProductNo"]
                    })
                    found = True
                    break

            if not found:
                result.append({
                    "Line": new_item["Line"],
                    "Top": new_item["Top"],
                    "ChargeAddress": new_item["ChargeAddress"],
                    "Items": [{
                        "BlockX": new_item["BlockX"],
                        "BlockY": new_item["BlockY"],
                        "ProductNo": new_item["ProductNo"]
                    }]
                })

        return result
