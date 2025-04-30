#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# filename: main.py
#
# 项目运行主程序
#

from optparse import OptionParser
from util import (
    Config, Logger,
    pretty_json,
    json,
    APPTypeError,
)

config = Config()
logger = Logger("main")


app = config.get('Base', 'APP')


if app == "Joyrun":
    from Joyrun import JoyrunClient as Client, __date__
else:
    raise APPTypeError("unsupported running APP -- %s !" % app)


parser = OptionParser(description="PKU running helper! Check your config first, then enjoy yourself!")
parser.add_option("-c", "--check", help="show 'config.ini' file", action="store_false")
parser.add_option("-s", "--start", help="start uploading job with %s Client" % app, action="store_false")

options, args = parser.parse_args()


if options.check is not None:

    print("# -- Using %s Client [%s] -- #" % (app, __date__))

    for section in config.sections():
        if section in ["Base", app]:
            print("# -- Section [%s] -- #" % section)
            print(pretty_json(dict(config[section])))

elif options.start is not None:

    try:
        logger.info("Running %s Client [%s]" % (app, __date__))
        client = Client()
        client.run()
    except Exception as err:
        logger.error("upload record failed !")
        raise err
    else:
        logger.info("upload record success !")
