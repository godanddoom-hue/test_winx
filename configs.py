"""Модуль конфигурации"""
import configparser
import logging


config = configparser.ConfigParser()
config.read('configs/config.ini', 'utf-8')

sql_database = {
    'database_name': config['sql']['database_name'],
    'user': config['sql']['user'],
    'password': config['sql']['password'],
    'host': config['sql']['host'],
    'port': config['sql']['port']
}

web_host = config.get('web', 'host')
web_port = config.get('web', 'port')
web_debug = config.get('web', 'debug')

log_dir = config['dir_and_file']['log_dir']
log_file = config['dir_and_file']['log_file']

error_dir = config['dir_and_file']['error_dir']
error_file = config['dir_and_file']['error_file']

certificate_templates = config['dir_and_file']['certificate_templates']
certificates_dir = config['dir_and_file']['certificates_dir']
certificate_base = config['dir_and_file']['certificate_base']

max_count_question = config.getint('admin', 'max_count_question')

main_text = config.get('text_for_certificate', 'main_text')
fairy_text = config.get('text_for_certificate', 'fairy_text')
date_text = config.get('text_for_certificate', 'date_text')
serial_number_text = config.get('text_for_certificate', 'serial_number_text')

color_for_text = '#000000'
position_for_user_name_text_size = (435, 381)
user_name_text_size = config.getint('text_for_certificate', 'user_name_text_size')
position_for_main_text_size = (435, 734)
position_fot_fairy_text = (435, 1134)
main_text_size = config.getint('text_for_certificate', 'main_text_size')
position_for_date = (435, 1598)
date_and_serial_number_text_size = config.getint('text_for_certificate', 'date_text_size')
position_for_serial_number = (435, 1698)
position_for_qr_code = (2650, 70)
qr_code_scale = 5
qr_code_border = 0

date_and_time_format_for_cert = '%d.%m.%Y %H-%M-%S'

qr_code_text = ('Сертификат действителен.\n'
                'Данный документ подтверждает, что его владелец успешно прошел тест: \n'
                'Кто ты из фей Winx?')

log_level: int = logging.INFO