import logging


logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')


def log_error(message: str) -> None:
    """Добавляет в лог сообщение типа ERROR"""
    logging.error(message)


def log_info(message: str) -> None:
    """Добавляет в лог сообщение типа INFO"""
    logging.info(message)
