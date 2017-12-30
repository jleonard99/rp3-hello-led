"""
Hello world test program
"""
import os
import sys
import time
import logging
import logging.config
import RPi.GPIO as GPIO
import yaml


PIN = 21         # The pin connected to the LED
ITERATIONS = 10  # The number of times to blink
INTERVAL = .25   # The length of time to blink on or off
LOG_LEVEL = logging.INFO
LOG_ENV_KEY = 'LOG_CFG'
LOG_CONF = 'led.log.yaml'

def setup_logging(
        default_path=LOG_CONF,
        default_level=LOG_LEVEL,
        env_key=LOG_ENV_KEY
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as yamlfile:
            config = yaml.safe_load(yamlfile.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)




def main():
    """ Main program
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    if os.path.exists(LOG_CONF):
        logger.info("Using log conf: %s", LOG_CONF)
    else:
        logger.info("%s not found.  Using basic conf.", LOG_CONF)

    GPIO.setmode(GPIO.BCM)    # pylint: disable=maybe-no-member
    GPIO.setwarnings(False)   # pylint: disable=maybe-no-member
    GPIO.setup(PIN, GPIO.OUT) # pylint: disable=maybe-no-member

    # The parameters to "range" are inclusive and exclusive, respectively,
    # so to go from 1 to 10 we have to use 1 and 11 (add 1 to the max)

    for i in range(1, ITERATIONS+1):

        logger.info("Loop %d: LED on", i)
        GPIO.output(PIN, GPIO.HIGH)  # pylint: disable=maybe-no-member
        time.sleep(INTERVAL)

        logger.info("Loop %d: LED off", i)
        GPIO.output(PIN, GPIO.LOW)   # pylint: disable=maybe-no-member
        time.sleep(INTERVAL)

if __name__ == "__main__":
    sys.exit(main() or 0)
