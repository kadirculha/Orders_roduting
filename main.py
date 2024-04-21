import pandas as pd
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", None)

from Concrete.Import.ExcelData import ExcelData
from Concrete.PathCalculator import PathCalculator
from Concrete.Routing.Step import Step

def ReadExcelSheet(filePath, sheetIndex):
    """
    Excel dosyasındaki belirli bir sayfayı okuyarak bir DataFrame döndürür.
    """
    df = pd.read_excel(filePath, sheet_name=sheetIndex)
    return df

def get_excelDatas(productsSheet):
    """
    Ürünler sayfasından gerekli verileri alarak Excel verilerini işler.
    """
    row_address = productsSheet["ADRES"]
    row_product_no = productsSheet["MALNO"]
    row_category = productsSheet["SOKAK"]

    concat_excel_df = pd.concat([row_address, row_product_no, row_category], axis=1)

    excel_data = []
    for index, row in concat_excel_df.iterrows():
        excel_data.append(
            {
                "ProductNo": int(row["MALNO"]),
                "Line": int(row["ADRES"][1:3]),
                "BlockY": row["ADRES"][3:4],
                "ChargeAddress": int(row["ADRES"][4:6]),
                "BlockX": row["ADRES"][6:7],
                "Category": row["SOKAK"],
            }
        )
    return excel_data, concat_excel_df

def get_orders(orderedProductNos, excelDatas):
    """
    Sipariş listesindeki ürünleri Excel verileriyle eşleştirerek siparişleri döndürür.
    """
    orders = []
    for order in orderedProductNos:
        for excelData in excelDatas:
            if order == excelData["ProductNo"]:
                orders.append(excelData)
                break 
    return orders

def get_pickers(pickersSheet):
    """
    Toplayıcıların verilerini okuyarak toplayıcı listesini oluşturur.
    """
    pickers = []
    for index, row in pickersSheet.iterrows():
        pickers.append(
            {
                "Name": row["Personeller"],
                "Categories": row["Toplayacağı Ürün kategorileri"].split(","),
                "TargetLine": row["Teslim Edeceği Koridor"],
                "Steps": {"SShape": [], "MidPoint": [], "LargestGap": []},
                "Distances": {"SShape": [], "MidPoint": [], "LargestGap": []},
            }
        )
    return pickers

if __name__ == '__main__':
    # Excel dosyasından mesafeleri okuyarak değişkenlere atama yapılır.
    metersSheet = ReadExcelSheet("Files/Products_.xlsx", 1)
    physicalDistanceBetweenLinesInMeter = int(metersSheet["len"][0])
    physicalDistanceBetweenStepsInMeter = int(metersSheet["len"][1])
    lineChargeAddressHeight = int(metersSheet["len"][2]) / 4

    # Ürünler ve siparişlerin olduğu sayfaları okur.
    productsSheet = ReadExcelSheet("Files/Products_.xlsx", 0)
    ordersSheet = ReadExcelSheet("Files/Orders.xlsx", 0)
    
    # Sipariş listesini alır.
    orderedProductNos = ordersSheet["MAL NO"].to_list() 
    excelDatas, _  = get_excelDatas(productsSheet=productsSheet)
    orders = get_orders(orderedProductNos,excelDatas)
    
    # Toplayıcı verilerini alır.
    pickersSheet = ReadExcelSheet("Files/Orders.xlsx", 1)
    pickers = get_pickers(pickersSheet)
    
    for picker in pickers:
        pickerOrders = []

        # Toplayıcının toplayacağı ürünleri seçer.
        for order in orders:
            if order.get("Category", str) in picker["Categories"]:
                pickerOrders.append(order)
        
        print(f"{picker['Name']} {len(pickerOrders)} adet ürün toplayacaktır.\n")
        
        print("Ürünler:")
        for i, order in enumerate(pickerOrders, start=1):
            print(f"-> Ürün {i} = {order}")
        
        for algorithm in ["SShape", "MidPoint", "LargestGap"]:
            picker["Steps"][algorithm] = PathCalculator.GetDistance(pickerOrders, lineChargeAddressHeight, 1, 0, picker["TargetLine"], algorithm)["Steps"]
            total_distance = Step.GetTotalDistance(physicalDistanceBetweenStepsInMeter, physicalDistanceBetweenLinesInMeter, picker["Steps"][algorithm])

            print(f"\n{algorithm} algoritmasına göre gitmesi gereken rota:")
            for i, step in enumerate(picker["Steps"][algorithm], start=1):
                print(f"-> Adım {i} = {step}")

            print(f"\n{algorithm} algoritmasına göre gitmesi gereken yolun uzunluğu: {total_distance} metre.\n")
        
        print("# Sonuç")
        shortest_distance = min([Step.GetTotalDistance(physicalDistanceBetweenStepsInMeter, physicalDistanceBetweenLinesInMeter, picker["Steps"][algorithm]) for algorithm in ["SShape", "MidPoint", "LargestGap"]])
        shortest_algorithm = [algorithm for algorithm in ["SShape", "MidPoint", "LargestGap"] if Step.GetTotalDistance(physicalDistanceBetweenStepsInMeter, physicalDistanceBetweenLinesInMeter, picker["Steps"][algorithm]) == shortest_distance][0]
        print(f"{picker['Name']} personeline bulunan en kısa yol için {shortest_algorithm} algoritması kullanılarak {shortest_distance} metre yol tercih edilmiştir.")

        print("-----------------------------------------------------------------")
