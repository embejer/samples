import logging


logging.basicConfig(level=logging.DEBUG,
                    filename='app.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def logger(module_name: str,level: str, message: str):
    logger = logging.getLogger(module_name)
    if level.lower() == 'debug':
        logger.debug(message)
    elif level.lower() == 'info':
        logger.info(message)
    elif level.lower() == 'warning':
        logger.warning(message)
    elif level.lower() == 'error':
        logger.error(message)
    elif level.lower() == 'exception':
        logger.exception(message)
    elif level.lower() == 'critical':
        logger.critical(message)