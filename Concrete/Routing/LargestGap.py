from Concrete.Routing.Line import Line
from Concrete.Routing.ShortestPath import ShortestPath
from Concrete.Routing.Step import Step

class LargestGapRouting:
    @staticmethod
    def GetRoute(orderPicker, lines, lineHeight, targetLineOrder, targetPositionY):
        steps = []

        # Dolu blokları içeren çizgileri sırala
        lines = sorted([line for line in lines if line.FilledBlocks], key=lambda x: x.Order)

        if not lines:
            return []

        # Başlangıç çizgisini seç
        beginLine = lines[0]
        # Başlangıç çizgisinden hedefe kadar olan rotayı hesapla ve adım listesine ekle
        steps.extend(ShortestPath.GetRoute(orderPicker, beginLine.Order, lineHeight + 1, lineHeight))
        # OrderPicker'ın LineOrder özelliğini başlangıç çizgisinin siparişine ayarla
        orderPicker.LineOrder = beginLine.Order
        # OrderPicker'ın PositionY özelliğini hedef yüksekliğine ayarla
        orderPicker.PositionY = lineHeight + 1

        # Başlangıçtan sonraki çizgiler arasındaki adımları belirle
        steps.append(Step(beginLine.Order, -1 * lineHeight - 1))

        linesInBetween = lines[1:len(lines) - 1]  # Baştaki ve sondaki satırları dahil et
        splitPositionYs = []

        # Her çizgi arasındaki en büyük boşluğun olduğu yüksekliği belirle
        for lineInBetween in linesInBetween:
            distances = []
            previousY = 1
            for block in lineInBetween.FilledBlocks:
                distances.append(block - previousY)
                previousY = block + 1

            distances.append(lineHeight - lineInBetween.FilledBlocks[-1])
            largestGapIndex = distances.index(max(distances))
            if largestGapIndex == 0:
                splitPositionYs.append(lineInBetween.FilledBlocks[0] - 1)
            else:
                splitPositionYs.append(lineInBetween.FilledBlocks[largestGapIndex - 1])

        linesHalvesByTop = []
        for i, lineInBetween in enumerate(linesInBetween):
            filteredBlocks = [b for b in lineInBetween.FilledBlocks if b <= splitPositionYs[i]]
            if len(filteredBlocks) == 0:
                continue

            newLine = Line(lineInBetween.Order, filteredBlocks)
            linesHalvesByTop.append(newLine)

        # En üst yarıya geçiş adımlarını ekle
        for lineHalfByTop in linesHalvesByTop:
            lastBottomBlock = max(lineHalfByTop.FilledBlocks)
            steps.append(Step(lineHalfByTop.Order, lastBottomBlock))
            steps.append(Step(lineHalfByTop.Order, -1 * lastBottomBlock))

        lastLine = lines[-1]
        orderPicker.LineOrder = lastLine.Order

        if lastLine.Order != lines[0].Order:
            steps.append(Step(lastLine.Order, lineHeight + 1))
            orderPicker.PositionY = lineHeight + 1
        else:
            orderPicker.PositionY = 0

        linesHalvesByBottom = []
        for i, lineInBetween in enumerate(linesInBetween):
            filteredBlocks = [b for b in lineInBetween.FilledBlocks if b > splitPositionYs[i]]
            if len(filteredBlocks) == 0:
                continue

            newLine = Line(lineInBetween.Order, filteredBlocks)
            linesHalvesByBottom.append(newLine)

        linesHalvesByBottom.reverse()

        # En alt yarıya geçiş adımlarını ekle
        for i, lineHalfByBottom in enumerate(linesHalvesByBottom):
            lastTopBlock = min(lineHalfByBottom.FilledBlocks)
            steps.append(Step(lineHalfByBottom.Order, -1 * (lineHeight - lastTopBlock + 1)))
            if i != len(linesHalvesByBottom) - 1:
                steps.append(Step(lineHalfByBottom.Order, lineHeight - lastTopBlock + 1))
            else:
                orderPicker.LineOrder = lineHalfByBottom.Order
                orderPicker.PositionY = lastTopBlock

        if targetLineOrder == -1:
            targetLineOrder = orderPicker.LineOrder
        if targetPositionY == -1:
            targetPositionY = lineHeight + 1
        steps.extend(ShortestPath.GetRoute(orderPicker, targetLineOrder, targetPositionY, lineHeight))

        # Sonuç adım listesini döndür
        return steps
