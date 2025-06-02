from docxtpl import DocxTemplate

path = "./shablon/Doc1.docx"
doc = DocxTemplate(path)
context = {"name": "Pidor", "num": "1", "years": "12"}

doc.render(context)
name_file = input("В введите имя файла")
doc.save(f"opis_{name_file}.docx")