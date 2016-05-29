import threading
import time
import wiringpi
import sys
from log import LOGGER
import subprocess


NUM_COLS = 3
NUM_ROWS = 4

COL_PINS = [3, 2, 0]
ROW_PINS = [15, 14, 13, 12]

MATRIX_MAPPING = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

KEY_UP = 'UP'
KEY_DOWN = 'DOWN'


class _KeyboardScanner(threading.Thread):

    def __init__(self, event_handler=None):
        threading.Thread.__init__(self)
        self._setup_pins()
        self._keystate = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self._event_handler = event_handler

    def _setup_pins(self):
        wiringpi.wiringPiSetup()
        for i in xrange(0, NUM_COLS):
            wiringpi.pinMode(COL_PINS[i], 1)
        for i in xrange(0, NUM_ROWS):
            wiringpi.pinMode(ROW_PINS[i], 0)
            wiringpi.pullUpDnControl(ROW_PINS[i], 1)  # PULL DOWN

    def _eval_key_states(self, col_pin_index):
        for i in xrange(0, NUM_ROWS):
            curr_state = wiringpi.digitalRead(ROW_PINS[i])
            old_state = self._keystate[i][col_pin_index]
            if curr_state == old_state:
                continue
            self._keystate[i][col_pin_index] = curr_state
            key = MATRIX_MAPPING[i][col_pin_index]
            if self._event_handler:
                self._event_handler(key, KEY_UP if curr_state == 0 else KEY_DOWN)

    def set_listener_fn(self, listener_fn):
        self._event_handler = listener_fn
   
    def run(self):
        curr_col_pin_index = 0
        while True:
            curr_col_pin = COL_PINS[curr_col_pin_index]
            wiringpi.digitalWrite(curr_col_pin, 1)
            self._eval_key_states(curr_col_pin_index)
            time.sleep(0.001)
            wiringpi.digitalWrite(curr_col_pin, 0)
            time.sleep(0.0001)
            curr_col_pin_index += 1
            curr_col_pin_index = curr_col_pin_index % NUM_COLS
            
_KB_SCANNER = _KeyboardScanner(None)
_KB_SCANNER.start()

def set_kb_listener(listener_fn):
    _KB_SCANNER.set_listener_fn(listener_fn)

def flash_ok():
    pass

def flash_busy():
    pass

def flash_error():
    pass

def wait_for_other_event():
    time.sleep(5)
    return

def stop_all_audio():
    pass

def play_file_async(filename):
    LOGGER.info('Playing %s. . .', filename)
