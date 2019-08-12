import json
import logging
import pathlib
import re
import subprocess
import urllib.request


class ConfigNotFound(Exception):
    pass


log_levels = {
    "DEBUG": logging.DEBUG,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
}

try:
    with open("config.json", "r") as cf_fh:
        config = json.load(cf_fh)
except FileNotFoundError:
    raise ConfigNotFound("No Configuration File was found.")

# Setup logging
log_file = pathlib.Path(config["log_dir"]) / "log.txt"
log_level = log_levels[config.get("log_level", "DEBUG").upper()]
logging.basicConfig(
    filename=log_file, level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

for i in config["sites"]:

    fail_bit = False

    logging.debug(f"Checking {i['target_uri']}")

    with urllib.request.urlopen(i["target_uri"]) as response:
        status = response.getcode()
        if status != 200:
            logging.warning(f"Site returned status code {status}")
            fail_bit = True

        rbytes = response.read()
        html = rbytes.decode("utf8")

    pos = i["positive_test_regex"]
    logging.debug(f"Ensuring positive test is found: {pos}")
    pmatches = re.findall(pos, html)
    if len(pmatches) == 0:
        logging.warning(f"Positive test regex did not match page html.")
        fail_bit = True

    neg = i["negative_test_regex"]
    logging.debug(f"Ensuring negative test is not found: {neg}")
    nmatches = re.findall(neg, html)
    if len(nmatches) > 0:
        logging.warning(f"Negative test regex matched page html.")
        fail_bit = True

    if fail_bit is True:
        fcommand = i["command_on_fail"]
        logging.warning(f"Conditions failed, running command: {fcommand}")
        subprocess.call(fcommand)
