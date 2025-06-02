from docxtpl import DocxTemplate
import csv

path_csv = './excel/base.csv'

def read_csv(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            str_data = row[0]
            result = str_data.split(';')
            print(result)

def write_csv(path, date):
    with open(path, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(date)

line_1 = ['125', 'май6', 'Кашаев Егор Сергеевич6', 'Кашаев Борис Еорович7', '356', 'меркурия7', '90228']
read_csv(path_csv)
write_csv(path_csv, line_1)