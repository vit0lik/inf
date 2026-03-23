import pandas as pd
import sqlite3

file_path = '03.ods'
sheets = pd.read_excel(file_path, sheet_name=None, engine='odf')

conn = sqlite3.connect('data.db')

for sheet_name, df in sheets.items():
    df.columns = [c.replace(' ', '_').replace(',', '').replace('.', '') for c in df.columns]
    df.to_sql(sheet_name.replace(' ', '_'), conn, index=False, if_exists='replace')

query = """
SELECT SUM(д.Количество_упаковок_шт * д."Цена_руб/шт")
FROM Движение_товаров д
JOIN Магазин м ON д.ID_магазина = м.ID_магазина
JOIN Товар т ON д.Артикул = т.Артикул
WHERE м.Район = 'Первомайский'
  AND т.Поставщик = 'Макаронная фабрика'
  AND д.Тип_операции = 'Поступление';
"""

result = conn.execute(query).fetchall()[0][0]
print(f"Ответ: ", result)

conn.close()