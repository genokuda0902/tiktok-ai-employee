"""Synthetic-only LibreOffice Calc proof source, no personal data."""
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile
def make_workbook(path):
    wb=Workbook.create(); ws=wb.worksheets.add('検算')
    ws.get_range('A1:D1').values=[['月','営業A','営業B','備考']]
    ws.get_range('A2:D4').values=[['4月',12,8,'架空データ'],['5月',16,9,'架空データ'],['6月',18,12,'架空データ']]
    ws.get_range('A5').values=[['合計（SUM）']]
    ws.get_range('B5').formulas=[['=SUM(B2:B4)']]
    ws.get_range('C5').formulas=[['=SUM(C2:C4)']]
    ws.get_range('A7').values=[['仮の下書き']];ws.get_range('B7').values=[[45]]
    ws.get_range('A8').values=[['検算後の値']];ws.get_range('B8').formulas=[['=B5']]
    ws.get_range('A10').values=[['注：数値は説明用の架空データです']]
    ws.get_range('A1:D1').format={'fill':'#0E7490','font':{'bold':True,'color':'#FFFFFF'},'row_height':32}
    ws.get_range('A5:D5').format={'fill':'#CCFBF1','font':{'bold':True,'color':'#134E4A'},'row_height':32}
    ws.get_range('A8:B8').format={'fill':'#DCFCE7','font':{'bold':True,'color':'#14532D'},'row_height':32}
    ws.get_range('A1:A10').format.column_width=24
    ws.get_range('B1:C10').format.column_width=18
    ws.get_range('D1:D10').format.column_width=20
    ws.get_range('A1:D10').format.row_height=29
    SpreadsheetFile.export_xlsx(wb).save(str(path))
    return wb.inspect({'kind':'table','range':'検算!A1:D10','include':'values,formulas','table_max_rows':10,'table_max_cols':4}).ndjson
if __name__=='__main__':
    import sys
    print(make_workbook(Path(sys.argv[1])))
