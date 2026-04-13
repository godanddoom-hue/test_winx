"""Модуль для создания сертификатов для пользователей"""
from PIL import Image, ImageDraw, ImageFont
import segno

import os
from datetime import datetime

import configs
import databases


def create_new_certificate(user_name: str, fairy_rus_name: str) -> str:
    """
    Функция для создания нового сертификата для пользователя
    :param fairy_rus_name:
    :param user_name: имя пользователя которое он ввел в начале теста
    :return: имя нового сертификата для дальнейшей отправки
    """
    img_base_path = os.path.join('static', configs.certificate_templates, configs.certificate_base)
    img = Image.open(img_base_path)

    font_path = os.path.join('static', 'css', 'fonts', 'Preciosa.ttf')
    font_for_name = ImageFont.truetype(font=font_path, size=configs.user_name_text_size)
    font_for_main_text = ImageFont.truetype(font=font_path, size=configs.main_text_size)
    font_for_date_text = ImageFont.truetype(font=font_path, size=configs.date_and_serial_number_text_size)

    draw = ImageDraw.Draw(img)

    date_and_time_format_for_cert = datetime.now().strftime(configs.date_and_time_format_for_cert)
    date_and_time_for_db = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    color = configs.color_for_text

    certificate_id = databases.insert_inf_to_certificates_db(user_name=user_name, fairy_name=fairy_rus_name,
                                                             date_and_time=date_and_time_for_db)

    # добавление имени пользователя на сертификат
    draw.text(configs.position_for_user_name_text_size, text=f'{user_name}!', fill=color, font=font_for_name)

    # добавление основного текста на сертификат
    draw.text(configs.position_for_main_text_size, text=configs.main_text, fill=color, font=font_for_main_text)

    # добавление текста с результатом феи на сертификат
    draw.text(configs.position_fot_fairy_text, text=f'{configs.fairy_text} {fairy_rus_name}!', fill=color,
              font=font_for_main_text)

    # добавление даты и времени на сертификат
    draw.text(configs.position_for_date, text=f'{configs.date_text} {date_and_time_format_for_cert}', fill=color,
              font=font_for_date_text)

    # добавление номера сертификата
    draw.text(configs.position_for_serial_number, text=f'{configs.serial_number_text} {certificate_id}',
              fill=color,
              font=font_for_date_text)

    # создание и добавление на сертификат QR кода
    qrcode = segno.make(content=f'{configs.qr_code_text}\n'
                                f'По итогу теста вы фея: {fairy_rus_name}\n'
                                f'Номер сертификата: {certificate_id}\n'
                                f'Дата прохождения: {date_and_time_for_db}')
    new_qr_code_path = os.path.join('static', 'media', 'qr_cods', f'qr_code_for_{certificate_id}.png')
    qrcode.save(new_qr_code_path, scale=configs.qr_code_scale, border=configs.qr_code_border)
    qr_code_img = Image.open(new_qr_code_path)
    img.paste(im=qr_code_img, box=configs.position_for_qr_code)
    qr_code_img.close()

    path_for_new_img = os.path.join('static', configs.certificates_dir,
                                    f'certificate_{date_and_time_format_for_cert}.png')

    img.save(path_for_new_img)
    img.close()
    return path_for_new_img
