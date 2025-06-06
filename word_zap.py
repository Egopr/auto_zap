from docxtpl import DocxTemplate

path = "./shablon/dog_25_NN.docx"
doc = DocxTemplate(path)
#context = {"name": "Pidor", "num": "1", "years": "12"}

context = {
        'day': '12',
        'month': 'май',
        'yer': '2025',
        'fio': 'Иванов Иван Иванович',
        'fio_j': 'Иванова Елена Ивановна',
        'hb_j_day': '22',
        'hb_j_month': 'сентябрь',
        'hb_j_year': '2013',
        'ser_pas': '3611',
        'num_pas': '439131',
        'dp': '09',
        'mp': 'июнь',
        'yp': '2011',
        'kem_pas	adres': 'Василиозерская 7',
        'mest_rab': 'ООО "Карповка"'
    }



doc.render(context)
name_file = input("В введите имя файла")
doc.save(f"opis_{name_file}.docx")