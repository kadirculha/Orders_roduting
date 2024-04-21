from Concrete.Routing.Line import Line
from Concrete.Routing.ShortestPath import ShortestPath
from Concrete.Routing.Step import Step

class MidPointRouting:
    @staticmethod
    def GetRoute(orderPicker, lines, lineHeight, targetLineOrder, targetPositionY):
        # Boş bir adım listesi oluştur
        steps = []

        # Dolu blokları içermeyen çizgileri filtrele ve sırala
        lines = sorted(filter(lambda o: any(o.FilledBlocks), lines), key=lambda o: o.Order)

        # Eğer çizgi yoksa boş adım listesini döndür
        if len(lines) == 0:
            return steps

        # Başlangıç çizgisini seç
        beginLine = lines[0]
        # Başlangıç çizgisinden hedefe kadar olan rotayı hesapla ve adım listesine ekle
        steps.extend(ShortestPath.GetRoute(orderPicker, beginLine.Order, lineHeight + 1, lineHeight))
        # OrderPicker'ın LineOrder özelliğini başlangıç çizgisinin siparişine ayarla
        orderPicker.LineOrder = beginLine.Order
        # OrderPicker'ın PositionY özelliğini hedef yüksekliğine ayarla
        orderPicker.PositionY = lineHeight + 1

        # Başlangıç çizgisinden sonra gelen çizgiler arasındaki adımları belirle
        steps.append(Step(beginLine.Order, -1 * lineHeight - 1))

        linesInBetween = lines[1:-1]

        linesHalvesByTop = []
        for line in linesInBetween:
            blocks = [b for b in line.FilledBlocks if b <= lineHeight / 2]
            if blocks:
                linesHalvesByTop.append(Line())
                linesHalvesByTop[-1].Order = line.Order
                linesHalvesByTop[-1].FilledBlocks = blocks

        # En üst yarıya geçiş adımlarını ekle
        for lineHalfByTop in linesHalvesByTop:
            lastBottomBlock = max(lineHalfByTop.FilledBlocks)
            steps.append(Step(lineHalfByTop.Order, lastBottomBlock))
            steps.append(Step(lineHalfByTop.Order, -1 * lastBottomBlock))

        lastLine = lines[-1]
        orderPicker.LineOrder = lastLine.Order

        # Son çizgi başlangıç çizgisinden farklı ise
        if lastLine.Order != lines[0].Order:
            steps.append(Step(lastLine.Order, lineHeight + 1))
            orderPicker.PositionY = lineHeight + 1
        else:
            orderPicker.PositionY = 0

        linesHalvesByBottom = []
        for line in linesInBetween:
            blocks = [b for b in line.FilledBlocks if b > lineHeight / 2]
            if blocks:
                linesHalvesByBottom.append(Line())
                linesHalvesByBottom[-1].Order = line.Order
                linesHalvesByBottom[-1].FilledBlocks = blocks
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

        # Hedef çizgi sipariş numarası ve pozisyonunu kontrol et
        if targetLineOrder == -1:
            targetLineOrder = orderPicker.LineOrder
        if targetPositionY == -1:
            targetPositionY = lineHeight + 1

        # Hedefe kadar olan rotayı hesapla ve adım listesine ekle
        steps.extend(ShortestPath.GetRoute(orderPicker, targetLineOrder, targetPositionY, lineHeight))

        # Adım listesini döndür
        return steps
