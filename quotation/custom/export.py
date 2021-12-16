from openpyxl import load_workbook
from openpyxl.styles import Alignment, Protection
from openpyxl.worksheet.datavalidation import DataValidation
import datetime as dt
from pathlib import Path
import os
from openpyxl.worksheet.cell_range import CellRange
from copy import copy

data_ex = {
    'inquiryid': '20211202001',
    'date': '2021-12-02',
    'author': 'EdwardHsu',
    'author_tel': '02-2796-1122 ext:223',
    'company': '寶晶能源',
    'comp_contact': '徐郁鈞',
    'contact_tel': '02-2345-6789 ext:223',
    'category': 'PV_module',
    'quotas': [{
        'item_name': 'PV-Module',
        'item_spec': '335W',
    }, {
        'item_name': 'PV-Module',
        'item_spec': '340W',
    }, {
        'item_name': 'PV-Module',
        'item_spec': '350W',
    }, {
        'item_name': 'PV-Module',
        'item_spec': '500W',
    }, {
        'item_name': 'PV-Module',
        'item_spec': '1000W',
    }, {
        'item_name': 'PV-Module',
        'item_spec': '1200W',
    }, {
        'item_name': 'PV-Module',
        'item_spec': '2000W',
    }, {
        'item_name': 'PV-Module',
        'item_spec': '3000W',
    }]
}
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def to_excel(data):
    wb_filedir = os.path.join(BASE_DIR, 'quotation', 'files', 'inquiry_example.xlsx')
    wb = load_workbook(wb_filedir)
    ws = wb['詢價單']

    ws.protection.password = '50791838'
    ws.protection.sheet = True
    ws['B3'] = data['date']  # 詢價時間

    ws['B5'] = "{}\n({})".format(data['author'], data['author_tel'])  # 詢價人 = 詢價單建立人
    ws['B5'].alignment = Alignment(wrap_text=True)  # 換行
    ws['E4'] = data['company']  # 報價公司
    ws['E5'] = "{}\n({})".format(data['comp_contact'], data['contact_tel'])  # 報價人 = 報價單建立人
    ws['E5'].alignment = Alignment(wrap_text=True)  # 換行
    ws['E3'].protection = Protection(locked=False)  # 報價時間解鎖可填寫
    rh = ws.row_dimensions[5]  # get dimension for row 3
    rh.height = 35  # value in points, there is no "auto"

    # 設定幣別只能用選項
    crrn_code = ['新台幣', '美元', '歐元', '人民幣', '日圓']
    list_option = '"{}"'.format(','.join(crrn_code))
    data_val = DataValidation(type="list", formula1=list_option)
    ws.add_data_validation(data_val)

    data_cnt = len(data['quotas'])  # 確定詢價品項數量

    # 資料大於10筆時，將既有品項向下移
    if data_cnt > 10:
        row_shift = data_cnt - 10
        ws.unmerge_cells(start_row=19, start_column=1, end_row=19, end_column=7)
        ws.move_range('A19:G30', rows=row_shift, translate=False)
        ws.merge_cells('A{0}:G{0}'.format(19 + row_shift))
        row_h = ws.row_dimensions[7].height
        ws.row_dimensions[19 + row_shift].height = row_h


    # 詢價品項填入表格內
    maxl_b = 0
    maxl_c = 0
    for idx, row in enumerate(data['quotas'], start=0):
        rowcnt = 9 + idx

        # 複製上一列表格格式
        for colcnt in range(7):
            from_style = ws.cell(row=rowcnt - 1, column=colcnt + 1)._style
            ws.cell(row=rowcnt, column=colcnt + 1)._style = from_style
            ws.cell(row=rowcnt, column=colcnt + 1).number_format = ws.cell(row=rowcnt - 1,
                                                                           column=colcnt + 1).number_format
        # 填入項次
        ws.cell(row=rowcnt, column=1, value=idx + 1)

        # 填入資料
        ws.cell(row=rowcnt, column=2, value=row['item_name'])
        ws.cell(row=rowcnt, column=3, value=row['item_spec'])

        # 紀錄欄寬，待調整成最適大小
        len_b = len(str(ws.cell(row=rowcnt, column=2).value))
        len_c = len(str(ws.cell(row=rowcnt, column=3).value))
        if len_b > maxl_b:
            maxl_b = len_b
        if len_c > maxl_c:
            maxl_c = len_c

        ws.cell(row=rowcnt, column=4, value=1)  # 填入數量1
        data_val.add(ws['E{}'.format(rowcnt)])

        ws.cell(row=rowcnt, column=5).protection = Protection(locked=False)  # 解鎖可填寫區域
        print(ws.cell(row=rowcnt, column=5), ws.cell(row=rowcnt, column=5).protection)
        ws.cell(row=rowcnt, column=6).protection = Protection(locked=False)  # 解鎖可填寫區域
        print(ws.cell(row=rowcnt, column=6), ws.cell(row=rowcnt, column=5).protection)
        ws.cell(row=rowcnt, column=7).value = "=D{}*F{}".format(rowcnt, rowcnt)


    # 調整欄寬
    ws.column_dimensions['B'].width = maxl_b * 1.5
    ws.column_dimensions['C'].width = maxl_c * 1.5
    # 設定幣別欄位只能用選項
    #data_val.add('E21:E30')

    # 設定新增品項區塊範圍
    new_cell_area = 'B21:G30'

    # bj6
    if data_cnt > 10:
        row_shift = data_cnt - 10
        new_cell_area = 'B{}:G{}'.format(21+row_shift, 30+row_shift)

    # 新增品項區塊
    for row in ws[new_cell_area]:
        for idx, col in enumerate(row, start=1):
            col.protection = Protection(locked=False)
            # 數量固定1
            if idx == 3:
                col.value = '=IF(B{}="","",1)'.format(col.row)
                col.protection = Protection(locked=True)

            elif idx == 4:
                data_val.add(col)
            # 總價加公式
            elif idx == 6:
                col.value = '=IF(F{0}="","",D{0}*F{0})'.format(col.row)
                col.protection = Protection(locked=True)
    [year, month] = dt.datetime.now().strftime('%Y-%m').split('-')

    file_path = os.path.join(BASE_DIR, 'static', 'files', 'inquiry', 'output', year, month)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    print(file_path)
    file_name = "{}_{}_詢價單{}_{}.xlsx".format(
        data['company'], data['category'], data['inquiryid'], dt.datetime.now().strftime("%Y%m%d%H%M%S"))
    wb.save(os.path.join(BASE_DIR, file_path, file_name))
    return file_name
