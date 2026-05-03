import os
import xml.dom.minidom as minidom
import xml.sax
from typing import List
from model import Athlete  # Импортируем наш класс данных из предыдущего шага

# ==========================================
# 1. ЧТЕНИЕ: SAX Парсер
# ==========================================
class AthleteSAXHandler(xml.sax.ContentHandler):
    """
    Обработчик событий для SAX парсера.
    Читает XML последовательно, тег за тегом.
    """
    def __init__(self):
        super().__init__()
        self.athletes: List[Athlete] = []
        self.current_athlete_data = {}
        self.current_element = ""
        self.current_data = ""

    # Срабатывает при открытии тега (например, <athlete> или <full_name>)
    def startElement(self, tag, attributes):
        self.current_element = tag
        self.current_data = ""
        if tag == "athlete":
            self.current_athlete_data = {}

    # Срабатывает при чтении текста между тегами
    def characters(self, content):
        # SAX может читать текст кусками, поэтому аккумулируем его
        self.current_data += content

    # Срабатывает при закрытии тега (например, </full_name>)
    def endElement(self, tag):
        text = self.current_data.strip()
        if tag == "full_name":
            self.current_athlete_data['full_name'] = text
        elif tag == "roster_status":
            self.current_athlete_data['roster_status'] = text
        elif tag == "position":
            self.current_athlete_data['position'] = text
        elif tag == "titles_count":
            # Строгое требование задания: используем правильные типы (int)
            self.current_athlete_data['titles_count'] = int(text) if text.isdigit() else 0
        elif tag == "sport_type":
            self.current_athlete_data['sport_type'] = text
        elif tag == "rank":
            self.current_athlete_data['rank'] = text
        elif tag == "athlete":
            # Тег спортсмена закрылся, значит мы собрали все его данные
            athlete = Athlete(**self.current_athlete_data)
            self.athletes.append(athlete)
        
        self.current_element = ""


def load_athletes_from_xml(filepath: str) -> List[Athlete]:
    """Функция-обертка для запуска SAX-парсера"""
    if not os.path.exists(filepath):
        return []
    
    handler = AthleteSAXHandler()
    xml.sax.parse(filepath, handler)
    return handler.athletes


# ==========================================
# 2. ЗАПИСЬ: DOM Парсер
# ==========================================
def save_athletes_to_xml(filepath: str, athletes: List[Athlete]):
    """
    Создает XML-дерево в памяти с помощью DOM и сохраняет в файл.
    """
    # Создаем пустой документ
    doc = minidom.Document()
    
    # Создаем корневой элемент
    root = doc.createElement("athletes")
    doc.appendChild(root)
    
    for athlete in athletes:
        # Создаем тег <athlete>
        athlete_elem = doc.createElement("athlete")
        root.appendChild(athlete_elem)
        
        # Вспомогательная функция для добавления дочерних тегов
        def add_child(parent, tag_name, text_value):
            elem = doc.createElement(tag_name)
            text_node = doc.createTextNode(str(text_value))
            elem.appendChild(text_node)
            parent.appendChild(elem)
            
        # Добавляем все поля спортсмена
        add_child(athlete_elem, "full_name", athlete.full_name)
        add_child(athlete_elem, "roster_status", athlete.roster_status)
        add_child(athlete_elem, "position", athlete.position)
        add_child(athlete_elem, "titles_count", athlete.titles_count)
        add_child(athlete_elem, "sport_type", athlete.sport_type)
        add_child(athlete_elem, "rank", athlete.rank)
        
    # Записываем сформированное дерево в файл с красивым форматированием (отступами)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(doc.toprettyxml(indent="    "))