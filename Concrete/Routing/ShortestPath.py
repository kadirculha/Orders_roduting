from Concrete.Routing.Step import Step

class ShortestPath:
    @staticmethod
    def GetRoute(orderPicker, targetLineOrder, targetPositionY, lineHeight):
        steps = []

        # Hedef çizginin mevcut çizgiyle aynı olup olmadığını kontrol et
        if targetLineOrder == orderPicker.LineOrder:
            # Eğer aynıysa, hedef pozisyon ile mevcut pozisyon arasındaki farkı adımlara ekle
            steps.append(Step(targetLineOrder, targetPositionY - orderPicker.PositionY))
        else:
            # Eğer farklıysa, iki farklı yol oluştur ve en kısa olanı seç
            path1Steps = [
                Step(orderPicker.LineOrder, -1 * orderPicker.PositionY),
                Step(targetLineOrder, targetPositionY)
            ]

            path2Steps = [
                Step(orderPicker.LineOrder, max(0, lineHeight - orderPicker.PositionY + 1)),
                Step(targetLineOrder, (lineHeight - targetPositionY + 1) * -1)
            ]

            # İki yol arasındaki adım sayılarını karşılaştırarak en kısa yolu seç
            if sum(abs(step.PositionYMovement) for step in path1Steps) <= sum(
                    abs(step.PositionYMovement) for step in path2Steps):
                steps.extend(path1Steps)
            else:
                steps.extend(path2Steps)

        # OrderPicker'ın LineOrder ve PositionY özelliklerini güncelle
        orderPicker.LineOrder = targetLineOrder
        orderPicker.PositionY = targetPositionY

        # Hareket etmeyen adımları (LineOrderMovement != 0) dışarıda bırak
        return [step for step in steps if step.LineOrderMovement != 0]
