# -*- coding: utf-8 -*-

import logging

l = logging.getLogger()
l.setLevel(logging.INFO)

logging.info(__name__)

if __name__ == '__main__':

    logging.info('Se esta ejecutando un info')
