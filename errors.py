"""Модуль обработки ошибок"""
import os
import traceback
import logging

import configs


def error_save(error: Exception) -> None:
    """
    Функция создает файл с полными логами по указанному пути, записывает туда ошибку
    :param error: Описание ошибка
    :return: None
    """
    folder_path = os.path.join(configs.error_dir)
    if not os.path.isdir(folder_path):
        os.makedirs(configs.error_dir)

    error_path = os.path.join(configs.error_dir, configs.error_file)

    full_error = traceback.format_exc()
    file = open(error_path, 'w')
    file.write(full_error)
    file.close()

    logging.error(f'Краткая ошибка: {error}')
