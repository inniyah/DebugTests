#!/usr/bin/env python3

import os
import sys

import json
import logging
import os
import queue
import signal
import sys
import time
import traceback

from datetime import datetime
from pprint import pprint
from glob import glob

#~ LOG_FORMAT = "[%(levelname)s] [%(pathname)s:%(lineno)d] [%(asctime)s] [%(name)s]: '%(message)s'"
LOG_FORMAT = "[%(pathname)s:%(lineno)d] [%(asctime)s]: '%(message)s'"
#~ LOG_FORMAT = "[%(levelname)s] %(message)s"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

import faulthandler
faulthandler.enable()

MY_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.join(MY_PATH, '..'))

from pygdbmi.gdbcontroller import GdbController

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def dump_json(data):
    from pygments import highlight, lexers, formatters
    formatted_json = json.dumps(data, sort_keys=True, indent=None, separators=(',', ':'))
    return highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())

def run(args):
    # Initialize object that manages gdb subprocess
    gdbmi = GdbController()

    # Load the file
    responses = gdbmi.write("-file-exec-and-symbols 'test.bin'")
    logging.info(dump_json(responses))
    # Get list of source files used to compile the binary
    responses = gdbmi.write("-file-list-exec-source-files")
    logging.info(dump_json(responses))
    # Add breakpoint
    responses = gdbmi.write("-break-insert main")
    logging.info(dump_json(responses))
    # Run
    responses = gdbmi.write("-exec-run")
    logging.info(dump_json(responses))
    responses = gdbmi.write("-exec-next")
    logging.info(dump_json(responses))
    responses = gdbmi.write("-exec-next")
    logging.info(dump_json(responses))
    responses = gdbmi.write("-exec-continue")
    logging.info(dump_json(responses))

    # gdbmi.gdb_process will be None because the gdb subprocess (and its inferior program) will be terminated
    gdbmi.exit()

    return 0

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class ColorStderr(logging.StreamHandler):
    def __init__(self, fmt=None):
        class AddColor(logging.Formatter):
            def __init__(self):
                super().__init__(fmt)
            def format(self, record: logging.LogRecord):
                msg = super().format(record)
                # Green/Cyan/Yellow/Red/Redder based on log level:
                color = '\033[1;' + ('32m', '36m', '33m', '31m', '41m')[min(4,int(4 * record.levelno / logging.FATAL))]
                return color + record.levelname + '\033[1;0m: ' + msg
        super().__init__(sys.stderr)
        self.setFormatter(AddColor())

class GracefulKiller:
    def __init__(self, objects=None):
        self.objects = objects
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
    def exit_gracefully(self, *args):
        logging.warning(" /!\\ Program Killed! /!\\")
        if self.objects:
            for obj in self.objects:
                try:
                    obj.kill()
                except Exception as e:
                    logging.error(f"{type(e).__name__}: {e}")
                    logging.error(traceback.format_exc())
                    #~ logging.error(sys.exc_info()[2])
        sys.exit(-1)

def main():
    import argparse

    res = -1

    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quiet', help='set logging to ERROR',
                        action='store_const', dest='loglevel',
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument('-d', '--debug', help='set logging to DEBUG',
                        action='store_const', dest='loglevel',
                        const=logging.DEBUG, default=logging.INFO)
    parser.add_argument('--hw', '--hardware', help='Hardware Configuration to use',
                        type=str, dest='hw', default='')
    #~ parser.add_argument('rest', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers = []

    log_console_handler = ColorStderr(LOG_FORMAT)
    log_console_handler.setLevel(args.loglevel)
    logger.addHandler(log_console_handler)

    try:
        killer = GracefulKiller()
        res = run(args)

    except Exception as e:
        res = -1
        logging.error(f"{type(e).__name__}: {e}")
        logging.error(traceback.format_exc())
        #~ logging.error(sys.exc_info()[2])

    return res

if __name__ == "__main__":
    sys.exit(main())
