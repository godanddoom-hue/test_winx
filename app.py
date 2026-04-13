"""Основной модуль запуска сайта"""
import logging

from flask import Flask, render_template, request, send_file

import configs
import databases
import logs
import errors
import certificates

app = Flask(__name__)
logs.setup_logging(log_level=configs.log_level)

@app.route('/')
def index() -> str:
    """
    Функция возвращает стартовую страницу
    :return: html страницу
    """
    user_ip = request.remote_addr
    logging.info(f'Пользователь с ip {user_ip} зашел на сайт')
    return render_template('index.html')


@app.route('/start_test', methods=['POST'])
def start_test() -> str:
    """
    Сюда попадаем при нажатии кнопки начать тест с главной страницы
    Мы получаем только информацию о том что нужно отгрузить страницу с тестом
    Достаем из БД первый вопрос и сопутствующую инфу и передаем в рендер страницы с тестом
    :return: html страницу
    """
    user_ip = request.remote_addr
    user_name = request.form.get('user_name')
    databases.insert_user(user_ip=user_ip, user_name=user_name)
    question_id, question_text, fairy_answer = databases.take_inf_about_question(1)
    logging.info(f'Пользователь с ip {user_ip} начал тест')
    return render_template('quiz.html', question_id=question_id,
                           question_text=question_text,
                           fairy_dict=fairy_answer)


@app.route('/next_question', methods=['POST'])
def next_question() -> str:
    """
    Сюда попадаем после нажатия любой кнопки с вариантом ответа
    Мы получаем из кнопки номер след вопроса и вариант который выбрал пользователь
    Вариант сохраняем в БД, из БД тянем след вопрос и сопутствующую инфу
    Если вопрос последний рендерим финальную страницу
    :return: html страницу следующего вопроса, если пользователь прошел все вопросы, то возвращает страницу результата
    """
    user_ip = request.remote_addr
    fairy_name = request.form.get('fairy_name')
    question_id = int(request.form.get('question_id'))

    if question_id > configs.max_count_question + 1:
        result = databases.quiz_result(user_ip=user_ip)
        fairy_name_result = result[0]
        user_name = result[1]
        description, fairy_name_rus = databases.take_description_info_for_final_result(fairy_name_result)
        logging.info(f'Пользователь с ip {user_ip} завершил тест и его результат это фея: {fairy_name_result}')
        return render_template('result.html',
                               fairy_name_result=fairy_name_result,
                               fairy_name_rus=fairy_name_rus,
                               description=description,
                               user_name=user_name)

    databases.update_user_table_after_questions(fairy_name=fairy_name, user_ip=user_ip)
    question_id, question_text, fairy_answer = databases.take_inf_about_question(question_id)
    logging.info(f'Пользователь с ip {user_ip} выбрал вариант ответа для феи: {fairy_name}')
    return render_template('quiz.html', question_id=question_id,
                           question_text=question_text,
                           fairy_dict=fairy_answer)


@app.route('/download_certificate', methods=['POST'])
def download_certificate():
    """
    Функция отправки данных для формирования нового сертификата и отправки на скачивание этого сертификата пользователю
    :return: отправляем пользователю сформированный файл-сертификат
    """
    user_ip = request.remote_addr
    fairy_rus_name = request.form.get('fairy_name_rus')
    result = databases.quiz_result(user_ip=user_ip)
    user_name = result[1]
    databases.delete_user_after_quiz(user_ip=user_ip)
    certificate_file_name = certificates.create_new_certificate(user_name, fairy_rus_name)
    logging.info(f'Пользователь с ip {user_ip} получил сертификат об окончании теста')
    return send_file(path_or_file=certificate_file_name, as_attachment=True,
                     download_name='Прекрасный сертификатик.png')


if __name__ == '__main__':
    try:
        app.run(
            host=configs.web_host,
            port=configs.web_port,
            debug=configs.web_debug
        )
    except Exception as error:
        logging.critical(f"Критическая ошибка в основном цикле программы: {error}")
        errors.error_save(error=error)

# TODO: поискать тесты в интернете, поворовать идеи
# TODO: как себя вести при одинаковом счетчике ответов на фее (подумать)
# TODO: картинки в тесте должны быть одного соотношения сторон (тупой вариант: обрезать картинки на сервере,
#  умный вариант: обрезать через css) (ГОТОВО!)
# TODO: у каждого сертификата должен быть уникальный номер, начинающийся с 1. Использовать номер как РК в БД, там же
#   хранить все данные по тесту (дата прохождения, выбранная фея, имя) (ГОТОВО!)
# TODO: на шаблон сертификата выводить уникальный номер, добив его нулями слева до 7-ми знаков (ГОТОВО!)
# TODO: поискать библиотеки для генерации qr кода, в него защифровать текст вида: вы прошли тест, данный сертификат
#   подлинность прохождения теста + номер сертификата (ГОТОВО!)
# TODO: нанести qr-код на шаблон сертификата (ГОТОВО!)
# TODO: исправить текст на основании того что написано в блокноте (ГОТОВО!)
# TODO: рамка для фото
# TODO: убрать точки из кнопок (ГОТОВО!)
# TODO: сделать нормальные логи (ГОТОВО!)
# TODO: раскидать картинки по папкам внутри папки медиа (ГОТОВО!)