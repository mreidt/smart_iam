import logging
from os import environ
from time import sleep, time

import pymysql

check_timeout = 60
check_interval = 2
interval_unit = "second" if check_interval == 1 else "seconds"

host = environ.get("DB_HOST")
user = environ.get("DB_USERNAME")
password = environ.get("DB_PASSWORD")
port = 3306
database = "smart_iam"

config = {"host": host, "user": user, "password": password, "port": port}

start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

start_message = """\n\n
################################
>>> Database to Connect
host = {host}
user = {user}
password = {password}
port = {port}
database = {database}
################################\n\n
""".format(
    host=host, user=user, password=password, port=port, database=database
)

fail_message = """\n\n
################################
>>> Couldn't connect to MYSQL within {} seconds.
################################\n\n"""

success_message = """\n\n
################################
>>> MYSQL is ready!
################################\n\n"""

logger.info(start_message)


def is_database_ready(host, user, password, port):
    while time() - start_time < check_timeout:
        try:
            conn = pymysql.connect(host=host, user=user, password=password, port=port)
            logger.info(success_message)
            conn.close()
            return True
        except Exception as exc:
            print(
                "MYSQL isn't ready {}. \nWaiting for {} {}...".format(
                    exc, check_interval, interval_unit
                )
            )
            sleep(check_interval)

    logger.error(fail_message.format(check_timeout))
    return False


is_database_ready(**config)
