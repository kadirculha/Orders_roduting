using System;
using System.Linq;

namespace BlaBla
{
    class Test
    {
        public static void Abc()
        {
            int lineChargeAddressHeight = 10;
            excelDatas
                .Select(o => new
                {
                    Line = o.Line,
                    Top = o.ChargeAddress <= lineChargeAddressHeight,
                    ChargeAddress = o.ChargeAddress % lineChargeAddressHeight,
                    BlockX = o.BlockX,
                    BlockY = o.BlockY,
                    ProductNo = o.ProductNo
                })
                .GroupBy(o => new
                {
                    o.Line,
                    o.Top,
                    o.ChargeAddress
                })
                .Select(o => new
                {
                    o.Key.Line,
                    o.Key.Top,
                    o.Key.ChargeAddress,
                    Items = o.Select(g => new
                    {
                        g.BlockX,
                        g.BlockY,
                        g.ProductNo
                    }).ToArray()
                }).ToArray();

            string[] productNos = new string[10];
            var filteredResult = excelDatas
                                        .Where(o => o.Items.Any(g => productNos.Any(p => o == g.ProductNo))).ToArray();

            Line[] lines = filteredResult
                                        .Where(o => o.Top == true)
                                        .GroupBy(o => o.Line)
                                        .Select(o => new Line(o.Key, o.Select(g => (int)g.ChargeAddress).ToArray())).ToArray();
        }
    }
}