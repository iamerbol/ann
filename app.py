from flask import Flask, request, jsonify, render_template
import xlwings as xw
import time
import logging

# Открываем Excel-файл без отображения окна
wb = xw.Book('calculator.xlsm', visible=False)

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    try:
        # Открываем Excel-файл
        wb = xw.Book('calculator.xlsm')
        sheet = wb.sheets['Калькулятор']  # Убедитесь, что имя листа правильное

        # Логируем входные данные
        logging.debug(f"Входные данные: {data}")

        # Вводим данные в Excel (все в столбец "C")
        sheet.range('C9').value = data['birth_date']  # Дата рождения (C9)
        sheet.range('C10').value = data['gender']  # Пол (C10)
        sheet.range('C11').value = data['guaranteed_period']  # Гарантированный период (C11)
        sheet.range('C12').value = data['amount']  # Сумма переводимая из ЕНПФ (C12) - не используется
        sheet.range('C16').value = data['disability']  # Инвалидность (C16)
        sheet.range('C17').value = data['oppv']  # Наличие ОППВ (C17)

        # Сохраняем файл, чтобы формулы пересчитались
        wb.save()

        # Даем время на пересчет формул
        time.sleep(2)  # Задержка в 2 секунды

        # Считываем только Минимальную сумму страховой премии из столбца "C"
        minimal_premium = sheet.range('C55').value  # Минимальная сумма страховой премии (C55)

        # Логируем результат
        logging.debug(f"Минимальная сумма страховой премии: {minimal_premium}")

        # Закрываем файл
        wb.close()

        # Возвращаем результат
        return jsonify({'minimal_premium': minimal_premium})

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)