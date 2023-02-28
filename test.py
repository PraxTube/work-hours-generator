from openpyxl.reader.excel import load_workbook

wb=load_workbook("zeitbogen.xlsx")
ws = wb["Januar 23"]
ws.cell(row=1, column=1).value= 'HARABARAM'
# save the workbook to a new file to finish the editing
# but the style settings has been removed (such like font, color) in the new file
wb.save("out.xlsx")
