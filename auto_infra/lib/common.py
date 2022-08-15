import json
import os
import requests
import subprocess
import sys
import typer
import webbrowser
from .setup_logger import logger


def run_command(
    command,
    env="",
    stream_output=False,
    treat_error_as_warning=False,
    sensitive_command=False,
):
    results = None
    try:
        if sensitive_command:
            logger.info("running a command flagged as sensitive: CENSORED")
        else:
            logger.info(f"running: {command}")
        myEnv = os.environ.copy()
        if env:
            myEnv.update(env)
        if stream_output:
            p = subprocess.Popen(
                command,
                shell=True,
                text=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=myEnv,
            )
            while True:
                nextline = p.stdout.readline()
                if nextline == "" and p.poll() is not None:
                    break
                sys.stdout.write(nextline)
            results, errors = p.communicate()
            if errors:
                if sensitive_command:
                    logger.exception("failed to run a sensitive command: CENSORED")
                else:
                    logger.exception(f"failed to run: {p.args}")
                logger.error(errors)
                sys.exit(1)
        else:
            p = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=myEnv,
            )
            results = p.stdout

        return results
    except subprocess.CalledProcessError as e:
        error_msg = f"failed to run {e.cmd}"
        if treat_error_as_warning and not sensitive_command:
            logger.warning(error_msg)
        elif treat_error_as_warning:
            logger.warning(e.stderr)
        else:
            if not sensitive_command:
                logger.exception(error_msg)
            logger.error(e.stderr)
            sys.exit(1)

