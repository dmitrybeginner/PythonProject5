# run_worker.py
# Этот скрипт является кастомной точкой входа, чтобы убедиться, что eventlet
# патчится в самый ранний возможный момент, перед собственными импортами Celery.

import eventlet
eventlet.monkey_patch()

import sys
from celery.__main__ import main

if __name__ == '__main__':
    sys.argv = [
        'celery',
        '-A',
        'core',
        *sys.argv[1:]
    ]
    main()