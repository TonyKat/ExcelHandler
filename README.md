# ExcelHandler

**1) О excel-файлах:**

- каждый файл имеет одинаковый формат организации и структуры данных
- необходимая информация находится на первом листе
- лист начинается с ячейки A1:
  - первый столбец - 'url',
  - второй столбец - 'label', 
  - третий столбец - 'fetch',
как в файлах-примерах ("url_label_fetch_1.xlsx", "url_label_fetch_2.xlsx").

**2) Если файл БД по указанному в настройках пути существует - считаем, что таблицы там - нужной структуры.**

**3) В файле setting.py имеется возможность настраивать:**
- timeout запроса                   | SETTING['timeout']
- количество потоков                | SETTING['number_threads']
- путь к файлу с дампом ошибок      | SETTING['path_to_error']
- путь к файлу логов                | SETTING['path_to_log']
- путь к файлу SQLite3              | SETTING['path_to_DB_SQLite3']

**4) Путь к входному excel файлу передаётся как аргумент скрипту при запуске, например:** 
- python main.py /data/monitoring/input/urls.xlsx


**5) Python 3.6.5**
- xlrd                               1.1.0 
- requests                           2.19. 

_____________________________________________________________________________
Для запуска введите в консоли (пункт 4): 
**python main.py path_to_excel_file.xlsx**