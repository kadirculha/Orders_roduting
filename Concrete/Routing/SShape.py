from Concrete.Routing.ShortestPath import ShortestPath
from Concrete.Routing.Step import Step

class SShapeRouting:
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

        # Diğer çizgilere geçiş adımlarını ekle
        for i, line in enumerate(lines[:-1]):
            if i % 2 == 0:
                steps.append(Step(line.Order, -1 * lineHeight - 1))
            else:
                steps.append(Step(line.Order, lineHeight + 1))

        # Son çizgiyi seç
        lastLine = lines[-1]
        # OrderPicker'ın LineOrder özelliğini son çizginin siparişine ayarla
        orderPicker.LineOrder = lastLine.Order

        # Eğer son çizgi başlangıç çizgisinden farklı ise
        if lastLine.Order != lines[0].Order:
            if len(lines) % 2 == 0:  # En üstten en alta
                lastTopBlock = max(lastLine.FilledBlocks)
                steps.append(Step(lastLine.Order, lastTopBlock))
                orderPicker.PositionY = lastTopBlock
            else:  # En alttan en üste
                lastBottomBlock = min(lastLine.FilledBlocks)
                steps.append(Step(lastLine.Order, -1 * (lineHeight - lastBottomBlock + 1)))
                orderPicker.PositionY = lastBottomBlock
        else:
            orderPicker.PositionY = lineHeight + 1

        # Hedef çizgi sipariş numarası ve pozisyonunu kontrol et
        if targetLineOrder == -1:
            targetLineOrder = orderPicker.LineOrder
        if targetPositionY == -1:
            targetPositionY = lineHeight + 1

        # Hedefe kadar olan rotayı hesapla ve adım listesine ekle
        steps.extend(ShortestPath.GetRoute(orderPicker, targetLineOrder, targetPositionY, lineHeight))

        # Adım listesini döndür
        return steps
