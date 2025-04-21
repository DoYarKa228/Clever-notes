#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QInputDialog, QLineEdit

import json

app = QApplication([])
window = QWidget()
window.setWindowTitle('Умные заметки')
window.resize(500,300)
list_notes = QListWidget()
lb1 = QLabel('Список заметок')
b_create = QPushButton('Создать заметку')
b_delete = QPushButton('Удалить заметку')
b_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
b_tag_add = QPushButton('Добавить к заметке')
b_tag_del = QPushButton('Открепить от заметки')
b_tag_search = QPushButton('Искать заметки по тегу')
list_tag = QListWidget()
lb2 = QLabel('Список тегов')

layout_n = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
col_2 = QVBoxLayout()
col_2.addWidget(lb1)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(b_create)
row_1.addWidget(b_delete)
row_2 = QHBoxLayout()
row_2.addWidget(b_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(lb2)
col_2.addWidget(list_tag)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(b_tag_add)
row_3.addWidget(b_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(b_tag_search)
col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_n.addLayout(col_1, stretch = 2)
layout_n.addLayout(col_2, stretch = 1)
window.setLayout(layout_n)

def show_note():
    name = list_notes.selectedItems()[0].text()
    field_text.setText(notes[name]['текст'])
    list_tag.clear()
    list_tag.addItems(notes[name]['теги'])

list_notes.itemClicked.connect(show_note)

window.show()

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)



def add_note():
    note_name, ok = QInputDialog.getText(window, 'Добавить заметку', 'Название заметки: ')
    if ok and note_name != '':
        notes[note_name] = {'текст' : '', 'теги' :[]}
        list_notes.addItem(note_name)
        list_tag.addItems(notes[note_name]['теги'])
        print(notes)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для сохранения не выбрана!')

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        field_text.clear()
        field_tag.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для удаления не выбрана!')

def search_note():
    tag = field_tag.text()
    if b_tag_search.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        b_tag_search.setText('Сбросить поиск: ')
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes_filtered)
    elif b_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes)
        b_tag_search.setText('Искать заметки по тегу')
    else:
        pass

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]["теги"].append(tag)
            list_tag.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print('Заметка для добавления тега не выбрана!')

def search_tag():
    tag = field_tag.text()
    if b_tag_search.text() == 'Искать заметки по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        b_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes_filtered)
    elif b_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tag.clear()
        list_notes.addItems(notes)
        b_tag_search.setText('Искать заметки по тегу')
    else:
        pass

def del_tag():
    if list_tag.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tag.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tag.clear()
        list_tag.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print('Тег для удаления не выбран!')


list_notes.itemClicked.connect(show_note)
b_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
b_save.clicked.connect(save_note)
b_delete.clicked.connect(del_note)
b_tag_add.clicked.connect(add_tag)
b_tag_del.clicked.connect(del_tag)
b_tag_search.clicked.connect(search_tag)

app.exec_()
