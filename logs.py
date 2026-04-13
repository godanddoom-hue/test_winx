"""Модуль логирования"""
from loguru import logger

import os
import logging

import configs


def logging_app(log: str, user_ip: str) -> None:
    """
    Функция создает сообщение о действии пользователя и записывает ее лог-файл
    :param log: Сообщение о действии пользователя
    :param user_ip: ip пользователя который зашел на сайт
    :return: Записывает в лог сообщение о действии
    """
    log_path = os.path.join(configs.log_dir, configs.log_file)

    logger.add(sink=f'{log_path}',
               level='INFO',
               format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | {message}')
    logger.info(f'Пользователь с IP: {user_ip}, {log}')


def setup_logging(log_level: int = logging.DEBUG,
                  log_dir: str = 'logs',
                  log_file: str = 'file.log') -> None:
    """
    Функция настраивает глобальное логирование для всего приложения
    :param log_level: Уровень логирования (по умолчанию DEBUG)
    :param log_dir: Директория для логов (по умолчанию 'logs')
    :param log_file: Имя лог-файла (по умолчанию 'file.log')
    :return:
    """
    try:
        os.makedirs(log_dir, exist_ok=True)

        full_log_path = os.path.join(log_dir, log_file)

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(full_log_path, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )

        logging.info('Логирование успешно настроено')
    except PermissionError as error:
        logging.error(f'Ошибка прав доступа при настройке логирования: {error}')
        raise
    except Exception as error:
        logging.error(f"Неожиданная ошибка при настройке логирования: {error}")
        raise
