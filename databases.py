"""Модуль с базой данных"""
import psycopg
from psycopg.types.json import Jsonb

from typing import Any, Tuple
import logging

import configs
import questions


def postgres_init(db_name: str) -> Tuple[Any, Any]:
    """
    Функция для инициализации подключения к Базе Данных
    :param db_name: имя базы данных
    :return: при успешном подключении возвращает кортеж с данными подключения, в противном случае кортеж с None
    """
    try:
        conn = psycopg.connect(
            f"dbname={db_name} user={configs.sql_database['user']} "
            f"password={configs.sql_database['password']} host={configs.sql_database['host']} "
            f"port={configs.sql_database['port']}"
        )
        cursor = conn.cursor()
        logging.info('Успешное подключение к Postgresql')
        return conn, cursor
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка подключения к Postgresql: {error}')
        return None, None


def insert_question_in_bd() -> None:
    """
    Функция для заполнения таблицы с вопросами в БД
    :return: None
    """
    conn, cursor = postgres_init(configs.sql_database['database_name'])
    try:
        questions_list = questions.questions_list()
        for question in questions_list:
            cursor.execute('INSERT INTO questions (question_id, question_text, fairy_answer) '
                           'VALUES (%s, %s, %s) '
                           'ON CONFLICT (question_id) '
                           'DO UPDATE SET '
                           'question_id = EXCLUDED.question_id, '
                           'question_text = EXCLUDED.question_text, '
                           'fairy_answer = EXCLUDED.fairy_answer;',
                           (question['id'], question['question'], Jsonb(question['answers'])))
        conn.commit()
        logging.info('Успешная запись вопросов в БД с вопросами')
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка заполнения базы с вопросами: {error}')
    finally:
        conn.close()
        cursor.close()


# insert_question_in_bd()


def insert_user(user_ip: str, user_name: str = 'Участник') -> None:
    """
    Функция для заполнения таблицы с пользователями в БД
    user_ip: ip с которого пользователь зашел на сайт
    :return: None
    """
    conn, cursor = postgres_init(configs.sql_database['database_name'])
    try:
        cursor.execute('INSERT INTO users (user_ip, blum, stella, flora, muza, tekna, leyla, user_name) '
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
                       'ON CONFLICT (user_ip) '
                       'DO UPDATE SET '
                       'user_ip = EXCLUDED.user_ip, '
                       'blum = EXCLUDED.blum, '
                       'stella = EXCLUDED.stella, '
                       'flora = EXCLUDED.flora, '
                       'muza = EXCLUDED.muza, '
                       'tekna = EXCLUDED.tekna, '
                       'leyla = EXCLUDED.leyla, '
                       'user_name = EXCLUDED.user_name;',
                       (user_ip, 0, 0, 0, 0, 0, 0, user_name))
        conn.commit()
        logging.info('Успешная запись пользователя в таблицу с пользователями')
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка заполнения базы с пользователями: {error}')
    finally:
        conn.close()
        cursor.close()


def take_inf_about_question(question_id: int) -> tuple[int, str, dict]:
    """
    Функция для получения информации о вопросе по его id
    :param question_id: id вопроса
    :return:
    """
    conn, cursor = postgres_init(configs.sql_database['database_name'])
    try:
        cursor.execute('SELECT * FROM questions WHERE question_id = %s', (question_id,))
        question_id, question_text, fairy_answer = cursor.fetchone()
        conn.commit()
        logging.info(f'Успешно получена информация о вопросе {question_id} из базы данных: questions')
        return question_id, question_text, fairy_answer
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка получения информации о вопросе с question_id = {question_id}: {error}')
    finally:
        conn.close()
        cursor.close()


def update_user_table_after_questions(fairy_name: str, user_ip: str) -> None:
    """
    Функция для записи ответов пользователя в таблицу users
    :param fairy_name: имя феи которую выбрал пользователь
    :param user_ip: ip пользователя
    :return: None
    """
    conn, cursor = postgres_init(configs.sql_database['database_name'])
    try:
        cursor.execute(f'UPDATE users SET {fairy_name} = {fairy_name}+1 WHERE user_ip = %s', (user_ip,))
        conn.commit()
        logging.info('Успешно обновлена таблица users после того как пользователь нажал ответ')
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка записи выбранного ответа пользователем в таблицу users: {error}')
    finally:
        conn.close()
        cursor.close()


def quiz_result(user_ip: str) -> tuple[str, str]:
    """
    Функция для расчета финального результата. Функция получает о значениях всех ответов от пользователя, чтобы выбрать
    нужную фею по максимальному значению
    :param user_ip: ip пользователя
    :return: кортеж с именем феи, по которой получилось максимальное значение, и с именем пользователя, которое он ввел
    на стартовой странице
    """
    conn, cursor = postgres_init(configs.sql_database['database_name'])
    try:
        cursor.execute('SELECT * FROM users WHERE user_ip = %s', (user_ip,))
        fairy_data = cursor.fetchone()
        user_name = fairy_data[7]
        fairy_dict_result = {
            'blum': fairy_data[1],
            'stella': fairy_data[2],
            'flora': fairy_data[3],
            'muza': fairy_data[4],
            'tekna': fairy_data[5],
            'leyla': fairy_data[6]
        }
        result = max(fairy_dict_result, key=fairy_dict_result.get)
        conn.commit()
        logging.info('Успешно получена информация о пользователе из базы данных для финального подсчета результатов')
        return result, user_name
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка: {error}')
    finally:
        conn.close()
        cursor.close()


def take_description_info_for_final_result(fairy_name_result: str) -> tuple[str, str]:
    """
    Функция для получения описания феи из БД для вывода информации на странице результата
    :param fairy_name_result: имя феи
    :return: кортеж состоящий из описания феи и ее имени на русском
    """
    conn, cursor = postgres_init(configs.sql_database['database_name'])
    try:
        cursor.execute('SELECT description, fairy_name_rus FROM winx_results WHERE fairy_name = %s',
                       (fairy_name_result,))
        description, fairy_name_rus = cursor.fetchone()
        conn.commit()
        logging.info('Успешно получено описания феи из БД и ее имя на Русском')
        return description, fairy_name_rus
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка: {error}')
    finally:
        conn.close()
        cursor.close()


def delete_user_after_quiz(user_ip: str) -> None:
    """
    Функция для удаления пользователя после завершения теста
    :param user_ip: ip пользователя
    :return: None
    """
    conn, cursor = postgres_init(configs.sql_database['database_name'])
    try:
        cursor.execute('DELETE FROM users WHERE user_ip = %s', (user_ip,))
        conn.commit()
        logging.info(f'Успешное удаление пользователя {user_ip} из таблицы users')
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка удаления пользователя из таблицы users: {error}')
    finally:
        conn.close()
        cursor.close()


def insert_inf_to_certificates_db(user_name: str, fairy_name: str, date_and_time: str) -> str:
    """
    Функция для записи нового сертификата о прохождении теста в БД
    :param user_name: имя пользователя, которое он ввел на главной странице
    :param fairy_name: имя феи которая получилась у пользователя в результате прохождения теста
    :param date_and_time: дата и время прохождения теста
    :return: Номер нового сертификата
    """
    conn, cursor = postgres_init(configs.sql_database['database_name'])
    try:
        # получаем из таблицы certificates последнюю запись по столбцу certificate_id
        cursor.execute('SELECT certificate_id FROM certificates ORDER BY certificate_id DESC LIMIT 1')
        certificate_id = cursor.fetchone()
        # если значение None, то записываем в переменную certificates строчку 1 + нули до 7-ми знаков
        if certificate_id is None:
            certificate_id = str(1).zfill(7)
        else:
            # если значение не None, преобразовываем значение в int, прибавляем к нему единицу, конвертируем обратно в
            # строчку и дописываем нули до 7-ми знаков
            certificate_id = int(certificate_id[0]) + 1
            certificate_id = str(certificate_id).zfill(7)

        # записываем новый сертификат в таблицу certificates
        cursor.execute('INSERT INTO certificates (certificate_id, user_name, fairy_result, date) '
                       'VALUES (%s, %s, %s, %s) '
                       'ON CONFLICT (certificate_id) '
                       'DO NOTHING;', (certificate_id, user_name, fairy_name, date_and_time))
        conn.commit()
        logging.info('Успешная запись нового сертификата в таблицу certificates')
        return certificate_id
    except (Exception, BaseException) as error:
        logging.error(f'Ошибка в добавлении нового сертификата в таблицу certificates: {error}')
    finally:
        conn.close()
        cursor.close()
