from docxtpl import DocxTemplate

# Загрузка шаблона
doc = DocxTemplate(".\shablon\dog_25_NN.docx")

# Контекст с данными для подстановки
context = {
    'company_name': "ООО 'Рога и копыта'",

}



# Подстановка данных в шаблон
doc.render(context)

# Сохранение результата
doc.save("generated_document.docx")