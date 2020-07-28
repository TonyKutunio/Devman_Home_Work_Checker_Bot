import requests
import os
import logging
import telegram
import time
from dotenv import load_dotenv


def get_devman_response(params, headers, logger):
    devman_url = ('https://dvmn.org/api/long_polling/')
    try:
        response = requests.get(devman_url,
                                params=params,
                                headers=headers)
        response.raise_for_status()
        response_content = response.json()
        response_timeout_status = response_content['status'] == 'timeout'
        if response_timeout_status:
            response_timestamp = response_content['timestamp_to_request']
            params = {'timestamp_to_request': response_timestamp}
        else:
            last_attempt_timestamp = response_content['last_attempt_timestamp']
            params = {'timestamp_to_request': last_attempt_timestamp}
        return response_content, response_timeout_status
    except requests.exceptions.ReadTimeout:
        logger.warning('READ TIMEOUT', exc_info=True)
        pass
    except requests.exceptions.ConnectionError:
        logger.warning('CONNECTION ERROR', exc_info=True)
        time.sleep(90)


def get_task_status_message(response_content,
                     response_timeout_status):

    if response_timeout_status == False:
        incomplete_task_response = response_content['new_attempts'][0]['is_negative']
        lesson_title = response_content['new_attempts'][0]['lesson_title']
        lesson_url = response_content['new_attempts'][0]['lesson_url']
        if incomplete_task_response:
            task_status_message = 'Преподаватель проверил работу!:  "{}"\n' \
                           ' Есть что доработать! https://dvmn.org/{} '.format(lesson_title,
                                                                               lesson_url)

        else:
            task_status_message = 'Преподаватель проверил работу!:  "{}"\n ' \
                           'Всё ОК! https://dvmn.org/{} '.format(lesson_title,
                                                                 lesson_url)
        return task_status_message

def send_task_message(task_status_message,
                      telegram_chat_id,
                      bot, response_timeout_status):
    if response_timeout_status == False:
        bot.send_message(chat_id=telegram_chat_id,
                         text=task_status_message)

def main():
    load_dotenv()
    telegram_token = os.getenv('TG_HOMEWORK_BOT')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    devman_token = os.getenv('DEVMAN_TOKEN')
    bot = telegram.Bot(token=telegram_token)

    class MyLogsHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            bot.send_message(chat_id=telegram_chat_id,
                             text=log_entry)

    log_format = '%(asctime)s, Level - %(levelname)s, file %(filename)s, Line %(lineno)d - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format)
    logger = logging.getLogger("HomeWorkChecker")
    logger.addHandler(MyLogsHandler())

    params = {'timestamp_to_request': None}
    headers = {"Authorization": devman_token}
    while True:
        try:
            devman_response, response_timeout_status = get_devman_response(params,
                                                                           headers,
                                                                           logger)
            task_message = get_task_status_message(devman_response,
                                            response_timeout_status)
            send_task_message(task_message,
                              telegram_chat_id,
                              bot,
                              response_timeout_status)
        except:
            logger.warning('ERROR OCCURED', exc_info=True)
            pass


if __name__ == '__main__':
    main()
