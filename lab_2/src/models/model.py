from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Athlete:
    full_name: str
    roster_status: str  # 'основной', 'запасной' или 'n/a'
    position: str
    titles_count: int   # Число завоеванных титулов
    sport_type: str
    rank: str           # '1-й юношеский', '2-й разряд', '3-й разряд', 'кмс', 'мастер спорта'

class AthleteModel:
    def __init__(self):
        # Инкапсулируем массив записей
        self._athletes: List[Athlete] = []

    def add_athlete(self, athlete: Athlete):
        self._athletes.append(athlete)

    def get_all(self) -> List[Athlete]:
        return self._athletes

    def set_all(self, athletes: List[Athlete]):
        self._athletes = athletes

    def clear(self):
        self._athletes.append([])

    def save_to_file(self, filepath: str):
        # Импортируем только тогда, когда метод вызывается
        from models.xml_manager import save_athletes_to_xml
        save_athletes_to_xml(filepath, self._athletes)

    def load_from_file(self, filepath: str):
        # Импортируем только тогда, когда метод вызывается
        from models.xml_manager import load_athletes_from_xml
        self._athletes = load_athletes_from_xml(filepath)

    # --- ЛОГИКА ПОСТРОЧНОГО ВЫВОДА (ПО УМНОМУ ПАГИНАЦИИ) ---
    
    def get_page(self, page_number: int, items_per_page: int, data_source: Optional[List[Athlete]] = None) -> List[Athlete]:
        """Возвращает срез массива для конкретной страницы."""
        data = data_source if data_source is not None else self._athletes
        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        return data[start_index:end_index]

    def get_total_pages(self, items_per_page: int, data_source: Optional[List[Athlete]] = None) -> int:
        """Рассчитывает общее количество страниц."""
        data = data_source if data_source is not None else self._athletes
        if not data:
            return 1
        # Округление вверх при делении
        return (len(data) + items_per_page - 1) // items_per_page

    def get_total_count(self, data_source: Optional[List[Athlete]] = None) -> int:
        """Возвращает общее количество записей."""
        data = data_source if data_source is not None else self._athletes
        return len(data)

    # --- ЛОГИКА ПОИСКА (Вариант 7) ---

    def search(self, 
               full_name: str = "", 
               sport_type: str = "", 
               min_titles: Optional[int] = None, 
               max_titles: Optional[int] = None, 
               rank: str = "") -> List[Athlete]:
        """
        Универсальный метод поиска. Если переданы параметры для конкретного критерия,
        ищет по ним.
        """
        results = []
        for athlete in self._athletes:
            match = False
            
            # Условие 1: по ФИО или виду спорта
            if full_name and sport_type:
                if (full_name.lower() in athlete.full_name.lower()) or (sport_type.lower() == athlete.sport_type.lower()):
                    match = True
            elif full_name and not rank: # Если ищем только по имени (без связи с разрядом)
                if full_name.lower() in athlete.full_name.lower():
                    match = True
            elif sport_type:
                if sport_type.lower() == athlete.sport_type.lower():
                    match = True
                    
            # Условие 2: по количеству завоеваний титула (диапазон)
            if min_titles is not None and max_titles is not None:
                if min_titles <= athlete.titles_count <= max_titles:
                    match = True
                    
            # Условие 3: по ФИО или разряду
            if full_name and rank:
                if (full_name.lower() in athlete.full_name.lower()) or (rank.lower() == athlete.rank.lower()):
                    match = True
            elif rank:
                if rank.lower() == athlete.rank.lower():
                    match = True

            if match:
                results.append(athlete)
                
        # Если ничего не ввели, возвращаем пустой список (или можно возвращать все)
        return results
        
    # --- ЛОГИКА УДАЛЕНИЯ ---
    
    def delete_records(self, records_to_delete: List[Athlete]) -> int:
        """
        Удаляет переданные записи из массива. 
        Возвращает количество удаленных записей.
        """
        initial_count = len(self._athletes)
        # Оставляем только тех спортсменов, которых нет в списке на удаление
        self._athletes = [a for a in self._athletes if a not in records_to_delete]
        
        deleted_count = initial_count - len(self._athletes)
        return deleted_count