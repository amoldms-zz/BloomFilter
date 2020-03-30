import middletier.logger as logger
import configparser
import sys


def get_data(filepath):
    try:
        with open(filepath, 'r') as file:
            document = file.read().replace('\n', ' ')
        return document
    except NameError as e:
        logger.log("File not found:{}".format(str(e)))
        sys.exit(1)
    except IOError as e:
        logger.log("Error in file reading:{}".format(str(e)))
        sys.exit(1)


def read_config(filepath):
    try:
        config = configparser.ConfigParser()
        config.read(filepath)
        return config
    except NameError as e:
        logger.log("File not found:{}".format(str(e)))
        sys.exit(1)
    except IOError as e:
        logger.log("Error in file reading:{}".format(str(e)))
        sys.exit(1)
