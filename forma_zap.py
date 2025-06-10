import sys
import csv
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QDateEdit, QTextEdit, QPushButton, QVBoxLayout,
                             QFormLayout, QMessageBox, QFileDialog, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QDialog, QTabWidget,
                             QTextBrowser)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Поиск родителя")
        self.setGeometry(200, 200, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Поле поиска
        self.search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Введите ФИО родителя или телефон...")
        self.search_btn = QPushButton("Поиск")
        self.search_btn.clicked.connect(self.search_data)

        self.search_layout.addWidget(self.search_field)
        self.search_layout.addWidget(self.search_btn)

        # Таблица с результатами
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(
            ["ФИО родителя", "Телефон", "ФИО ребенка", "Дата рождения ребенка", "Выбрать"])
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Кнопки
        self.btn_layout = QHBoxLayout()
        self.select_btn = QPushButton("Выбрать")
        self.select_btn.clicked.connect(self.select_record)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        self.btn_layout.addWidget(self.select_btn)
        self.btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(self.search_layout)
        layout.addWidget(self.results_table)
        layout.addLayout(self.btn_layout)

        self.setLayout(layout)

    def search_data(self):
        search_text = self.search_field.text().lower()
        if not search_text:
            QMessageBox.warning(self, "Ошибка", "Введите текст для поиска")
            return

        try:
            with open(self.parent.filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = [row for row in reader if
                        (search_text in row['parent_fio'].lower() or
                         search_text in row['phone'].lower())]

                if not rows:
                    QMessageBox.information(self, "Результаты", "Ничего не найдено")
                    return

                self.results_table.setRowCount(len(rows))
                for i, row in enumerate(rows):
                    self.results_table.setItem(i, 0, QTableWidgetItem(row['parent_fio']))
                    self.results_table.setItem(i, 1, QTableWidgetItem(row['phone']))
                    self.results_table.setItem(i, 2, QTableWidgetItem(row['child_fio']))
                    self.results_table.setItem(i, 3, QTableWidgetItem(row['child_birth']))

                    select_btn = QPushButton("Выбрать")
                    select_btn.clicked.connect(lambda _, r=row: self.select_specific_record(r))
                    self.results_table.setCellWidget(i, 4, select_btn)

                self.results_table.resizeColumnsToContents()

        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл с данными не найден")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при поиске: {str(e)}")

    def select_record(self):
        selected_row = self.results_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите запись из таблицы")
            return

        data = {
            'parent_fio': self.results_table.item(selected_row, 0).text(),
            'phone': self.results_table.item(selected_row, 1).text(),
            'child_fio': self.results_table.item(selected_row, 2).text(),
            'child_birth': self.results_table.item(selected_row, 3).text()
        }

        # Получаем полные данные из файла
        try:
            with open(self.parent.filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if (row['parent_fio'] == data['parent_fio'] and
                            row['phone'] == data['phone']):
                        self.parent.set_form_data(row)
                        break

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def select_specific_record(self, record):
        self.parent.set_form_data(record)
        self.accept()


class PrintPreviewDialog(QPrintPreviewDialog):
    def __init__(self, printer, parent=None):
        super().__init__(printer, parent)
        self.parent = parent

    def paintRequested(self, printer):
        document = self.parent.create_print_document()
        document.print_(printer)


class ParentChildForm(QWidget):
    def __init__(self):
        super().__init__()
        self.filename = 'parent_child_data.csv'
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Анкета родителя и ребенка')
        self.setGeometry(100, 100, 700, 900)

        # Создаем элементы формы
        self.create_form_elements()

        # Кнопки управления данными
        self.manage_buttons = QHBoxLayout()

        self.search_btn = QPushButton('Поиск родителя')
        self.search_btn.clicked.connect(self.show_search_dialog)

        self.load_btn = QPushButton('Загрузить данные')
        self.load_btn.clicked.connect(self.load_data)

        self.save_btn = QPushButton('Сохранить данные')
        self.save_btn.clicked.connect(self.save_data)

        self.export_btn = QPushButton('Экспорт в файл')
        self.export_btn.clicked.connect(self.export_data)

        self.print_btn = QPushButton('Печать формы')
        self.print_btn.clicked.connect(self.print_form)

        self.manage_buttons.addWidget(self.search_btn)
        self.manage_buttons.addWidget(self.load_btn)
        self.manage_buttons.addWidget(self.save_btn)
        self.manage_buttons.addWidget(self.export_btn)
        self.manage_buttons.addWidget(self.print_btn)

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.form_layout)
        main_layout.addLayout(self.manage_buttons)
        main_layout.addWidget(self.submit_btn)

        self.setLayout(main_layout)

    def create_form_elements(self):
        """Создает все элементы формы"""
        self.form_layout = QFormLayout()

        # Данные родителя
        self.parent_fio = QLineEdit()
        self.form_layout.addRow(QLabel("ФИО родителя:"), self.parent_fio)

        # Данные ребенка
        self.child_fio = QLineEdit()
        self.child_birth = QDateEdit()
        self.child_birth.setDisplayFormat("dd.MM.yyyy")
        self.child_birth.setDate(QDate.currentDate())

        self.form_layout.addRow(QLabel("ФИО ребенка:"), self.child_fio)
        self.form_layout.addRow(QLabel("Дата рождения ребенка:"), self.child_birth)

        # Паспортные данные
        self.passport_series_number = QLineEdit()
        self.passport_issue_date = QDateEdit()
        self.passport_issue_date.setDisplayFormat("dd.MM.yyyy")
        self.passport_issue_date.setDate(QDate.currentDate())
        self.passport_issued_by = QTextEdit()
        self.passport_issued_by.setMaximumHeight(60)

        self.form_layout.addRow(QLabel("Серия и номер паспорта:"), self.passport_series_number)
        self.form_layout.addRow(QLabel("Дата выдачи паспорта:"), self.passport_issue_date)
        self.form_layout.addRow(QLabel("Кем выдан паспорт:"), self.passport_issued_by)

        # Контактные данные
        self.phone = QLineEdit()
        self.email = QLineEdit()

        self.form_layout.addRow(QLabel("Телефон:"), self.phone)
        self.form_layout.addRow(QLabel("E-mail:"), self.email)

        # Свидетельство о рождении
        self.birth_cert_number = QLineEdit()
        self.birth_cert_series = QLineEdit()
        self.birth_cert_issued_by = QTextEdit()
        self.birth_cert_issued_by.setMaximumHeight(60)

        self.form_layout.addRow(QLabel("Номер свидетельства о рождении:"), self.birth_cert_number)
        self.form_layout.addRow(QLabel("Серия свидетельства:"), self.birth_cert_series)
        self.form_layout.addRow(QLabel("Кем выдано свидетельство:"), self.birth_cert_issued_by)

        # Адреса
        self.reg_address = QTextEdit()
        self.reg_address.setMaximumHeight(60)
        self.live_address = QTextEdit()
        self.live_address.setMaximumHeight(60)
        self.copy_address_btn = QPushButton("Скопировать адрес регистрации")
        self.copy_address_btn.clicked.connect(self.copy_address)

        self.form_layout.addRow(QLabel("Адрес регистрации:"), self.reg_address)
        self.form_layout.addRow(QLabel("Адрес проживания:"), self.live_address)
        self.form_layout.addRow(self.copy_address_btn)

        # Кнопка отправки
        self.submit_btn = QPushButton('Сохранить данные')
        self.submit_btn.clicked.connect(self.save_data)

    def copy_address(self):
        """Копирует адрес регистрации в адрес проживания"""
        self.live_address.setPlainText(self.reg_address.toPlainText())

    def set_form_data(self, data):
        """Заполняет форму данными из словаря"""
        self.parent_fio.setText(data.get('parent_fio', ''))
        self.child_fio.setText(data.get('child_fio', ''))

        if 'child_birth' in data:
            date = QDate.fromString(data['child_birth'], "dd.MM.yyyy")
            self.child_birth.setDate(date)

        self.passport_series_number.setText(data.get('passport_series_number', ''))

        if 'passport_issue_date' in data:
            date = QDate.fromString(data['passport_issue_date'], "dd.MM.yyyy")
            self.passport_issue_date.setDate(date)

        self.passport_issued_by.setPlainText(data.get('passport_issued_by', ''))
        self.phone.setText(data.get('phone', ''))
        self.email.setText(data.get('email', ''))
        self.birth_cert_number.setText(data.get('birth_cert_number', ''))
        self.birth_cert_series.setText(data.get('birth_cert_series', ''))
        self.birth_cert_issued_by.setPlainText(data.get('birth_cert_issued_by', ''))
        self.reg_address.setPlainText(data.get('reg_address', ''))
        self.live_address.setPlainText(data.get('live_address', ''))

    def get_form_data(self):
        """Возвращает данные формы в виде словаря"""
        return {
            'parent_fio': self.parent_fio.text(),
            'child_fio': self.child_fio.text(),
            'child_birth': self.child_birth.date().toString("dd.MM.yyyy"),
            'passport_series_number': self.passport_series_number.text(),
            'passport_issue_date': self.passport_issue_date.date().toString("dd.MM.yyyy"),
            'passport_issued_by': self.passport_issued_by.toPlainText(),
            'phone': self.phone.text(),
            'email': self.email.text(),
            'birth_cert_number': self.birth_cert_number.text(),
            'birth_cert_series': self.birth_cert_series.text(),
            'birth_cert_issued_by': self.birth_cert_issued_by.toPlainText(),
            'reg_address': self.reg_address.toPlainText(),
            'live_address': self.live_address.toPlainText()
        }

    def load_data(self):
        """Загружает данные из CSV файла"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл с данными", "",
            "CSV Files (*.csv);;All Files (*)",
            options=options
        )

        if not filename:
            return  # Пользователь отменил выбор

        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)

                if not rows:
                    QMessageBox.warning(self, 'Предупреждение', 'Файл не содержит данных')
                    return

                # Загружаем последнюю запись из файла
                self.set_form_data(rows[-1])

            QMessageBox.information(self, 'Успех', 'Данные успешно загружены')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {str(e)}')

    def save_data(self):
        """Сохраняет данные формы в CSV файл"""
        data = self.get_form_data()

        try:
            # Проверяем, существует ли файл
            file_exists = False
            try:
                with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                    file_exists = True
            except FileNotFoundError:
                pass

            # Записываем данные в файл
            with open(self.filename, 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = data.keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()  # Записываем заголовки, если файл новый

                writer.writerow(data)

            QMessageBox.information(self, 'Успех', f'Данные сохранены в файл {self.filename}')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить данные: {str(e)}')

    def export_data(self):
        """Экспортирует данные в выбранный файл"""
        data = self.get_form_data()

        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Экспорт данных", "",
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)",
            options=options
        )

        if not filename:
            return  # Пользователь отменил выбор

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                if filename.endswith('.csv'):
                    writer = csv.DictWriter(file, fieldnames=data.keys())
                    writer.writeheader()
                    writer.writerow(data)
                else:
                    for key, value in data.items():
                        file.write(f"{key}: {value}\n")

            QMessageBox.information(self, 'Успех', f'Данные успешно экспортированы в {filename}')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось экспортировать данные: {str(e)}')

    def show_search_dialog(self):
        dialog = SearchDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Успех", "Данные загружены в форму")

    def create_print_document(self):
        """Создает HTML документ для печати"""
        data = self.get_form_data()

        # Выносим замену в переменные
        passport_issued_by = data['passport_issued_by'].replace('\n', '<br>')
        birth_cert_issued_by = data['birth_cert_issued_by'].replace('\n', '<br>')
        reg_address = data['reg_address'].replace('\n', '<br>')
        live_address = data['live_address'].replace('\n', '<br>')

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Анкета родителя и ребенка</title>
            <style>
                body {{ font-family: Arial; margin: 20px; }}
                h1 {{ text-align: center; }}
                .section {{ margin-bottom: 20px; }}
                .section-title {{ font-weight: bold; font-size: 16px; 
                                border-bottom: 1px solid #000; 
                                margin-bottom: 10px; }}
                .row {{ margin-bottom: 5px; }}
                .label {{ font-weight: bold; display: inline-block; width: 250px; }}
                .value {{ display: inline-block; }}
            </style>
        </head>
        <body>
            <h1>Анкета родителя и ребенка</h1>

            <!-- Данные родителя -->
            <div class="section">
                <div class="section-title">1. Данные родителя</div>
                <div class="row">
                    <span class="label">ФИО родителя:</span>
                    <span class="value">{data['parent_fio']}</span>
                </div>
                <div class="row">
                    <span class="label">Телефон:</span>
                    <span class="value">{data['phone']}</span>
                </div>
                <div class="row">
                    <span class="label">E-mail:</span>
                    <span class="value">{data['email']}</span>
                </div>
            </div>

            <!-- Данные ребенка -->
            <div class="section">
                <div class="section-title">2. Данные ребенка</div>
                <div class="row">
                    <span class="label">ФИО ребенка:</span>
                    <span class="value">{data['child_fio']}</span>
                </div>
                <div class="row">
                    <span class="label">Дата рождения:</span>
                    <span class="value">{data['child_birth']}</span>
                </div>
            </div>

            <!-- Паспортные данные -->
            <div class="section">
                <div class="section-title">3. Паспортные данные родителя</div>
                <div class="row">
                    <span class="label">Серия и номер паспорта:</span>
                    <span class="value">{data['passport_series_number']}</span>
                </div>
                <div class="row">
                    <span class="label">Дата выдачи:</span>
                    <span class="value">{data['passport_issue_date']}</span>
                </div>
                <div class="row">
                    <span class="label">Кем выдан:</span>
                    <span class="value">{passport_issued_by}</span>
                </div>
            </div>

            <!-- Свидетельство о рождении -->
            <div class="section">
                <div class="section-title">4. Свидетельство о рождении ребенка</div>
                <div class="row">
                    <span class="label">Номер свидетельства:</span>
                    <span class="value">{data['birth_cert_number']}</span>
                </div>
                <div class="row">
                    <span class="label">Серия свидетельства:</span>
                    <span class="value">{data['birth_cert_series']}</span>
                </div>
                <div class="row">
                    <span class="label">Кем выдано:</span>
                    <span class="value">{birth_cert_issued_by}</span>
                </div>
            </div>

            <!-- Адреса -->
            <div class="section">
                <div class="section-title">5. Адреса</div>
                <div class="row">
                    <span class="label">Адрес регистрации:</span>
                    <span class="value">{reg_address}</span>
                </div>
                <div class="row">
                    <span class="label">Адрес проживания:</span>
                    <span class="value">{live_address}</span>
                </div>
            </div>

            <!-- Дата заполнения -->
            <div style="margin-top: 50px; text-align: right;">
                <p>Дата заполнения: {QDate.currentDate().toString("dd.MM.yyyy")}</p>
            </div>
        </body>
        </html>
        """

        document = QTextBrowser()
        document.setHtml(html)
        return document

    def print_form(self):
        """Печать формы"""
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Portrait)

        preview = PrintPreviewDialog(printer, self)
        preview.setWindowTitle("Предпросмотр печати")
        preview.resize(800, 600)
        preview.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ParentChildForm()
    form.show()
    sys.exit(app.exec_())