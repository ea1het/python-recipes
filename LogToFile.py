"""
This piece of code serves to log application data to a log file without using WSGI mechanisms
"""
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

app = Flask(__name__)  # pylint: disable=invalid-name

# Log facility to text file
LOG_FILENAME = 'log_app.log'
LOGFORMATTER = logging.Formatter("[ %(asctime)s ] [ %(pathname)s | %(lineno)d ] \
[ %(levelname)s | %(message)s ]")
LOGHANDLER = RotatingFileHandler(LOG_FILENAME, maxBytes=10000000, backupCount=5)
LOGHANDLER.setFormatter(LOGFORMATTER)
LOGHANDLER.setLevel(logging.DEBUG)
app.logger.addHandler(LOGHANDLER)


@app.route("/", methods=['GET'])
def logtest():
    """
    Function to print log tests
    Depending on the SetLevel feature the log will be more os less populated by the application
    """
    app.logger.debug('DEBUG log')
    app.logger.info('INFO log')
    app.logger.warning('WARNING log')
    app.logger.error('ERROR log')
    app.logger.critical('CRITICAL log')
    return "Log testing..."


if __name__ == '__main__':
    app.run()
