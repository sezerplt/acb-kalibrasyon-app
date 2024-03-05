import io
import xlsxwriter
from django.http import HttpResponse


def export_data(file_name,ex_data,header):
    print(file_name)
    output = io.BytesIO()
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    for header_num,head in  enumerate(header):
        worksheet.write(0, header_num, head)
    for row_num, columns in enumerate(ex_data):
        for col_num, cell_data in enumerate(columns):

            worksheet.write(row_num+1, col_num, cell_data)

    workbook.close()
    output.seek(0)
    filename = f'{file_name}.xlsx'
    print(filename)
    response = HttpResponse(
    output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response    
    
  
