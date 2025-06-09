from docxtpl import DocxTemplate
import time

path = "./shablon/dog_25_NN.docx"
doc = DocxTemplate(path)

months_ru = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}
current_time = time.localtime()
year = current_time.tm_year
month = months_ru[current_time.tm_mon]
day = current_time.tm_mday


date_str = f"«{day}» {month} {year} года"

context = {
        'date_now': date_str,
        'fio': 'Иванов Иван Иванович',
        'fio_j': ' Иванова Елена Ивановна',
        'hb_j_day': '22',
        'hb_j_month': ' сентябрь',
        'hb_j_year': ' 2013',
        'svi_rog_date':'',
        'svi_rog_ser':'',
        'svi_rog_num':'',
        'svi_rog_kem':'',
        'ser_pas': ' 3611 ',
        'num_pas': ' 439131 ',
        'dp': '09',
        'mp': ' июнь',
        'yp': ' 2011',
        'kem_pas': ' Отделом УФМС России по Самарской области и городу Тольятти в Автозоводском районе ',
        'adres': ' Василиозерская 7 ',
        'mest_rab': 'ООО "Карповка"',
        'tel_num': '8 (911)759-51-16',
        'e_mail':'Egor_mail_no@mail.ru',
        'adres_reg': 'Ленинградская лбласть, г. Всеволожск, ул. Шишканя 12 кв. 423',
        'adres_fukt': 'Ленинградская лбласть, г. Всеволожск, ул. Василиозерская 7 кв. 54'
    }

def date_hb_j():  #Дата рождения ребёнка (return str)
        pass

def pas_one_str(): #Паспорт в одну строку (return str)
        pass


doc.render(context)
name_file = input("В введите имя файла > ")
doc.save(f"opis_{name_file}.docx")
