#!/usr/bin/python
import threading
import hardware
import codes
from log import LOGGER

def eval_code(code):
    prefix, suffix = code[0], code[1:]
    if prefix not in codes.ALL_CODE_PREFIXES:
        return False
    if suffix not in codes.ALL_CODE_PREFIXES[prefix]:
        return False
    hardware.flash_ok()
    hardware.play_file_async(codes.ALL_CODE_PREFIXES[prefix][suffix])
    return True

class CodeProcessor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_ = False
        self.codebuffer = ''
        LOGGER.info('Starting code processor.')
        hardware.set_kb_listener(self._kb_listener)

    def _kb_listener(self, key, state):
        if state == hardware.KEY_UP:
            return  # Not interested for now
        hardware.flash_busy()
        self.codebuffer += key
        LOGGER.debug('Entered key: %s', key)
        if codes.is_complete(self.codebuffer):
            if eval_code(self.codebuffer):
                LOGGER.debug('Successfully processed code: %s', self.codebuffer)
                hardware.flash_ok()
            else:
                LOGGER.debug('Error processing code: %s', self.codebuffer)
                hardware.flash_error()
            self.codebuffer = ''


class OtherEventsListener(threading.Thread):
    def __init__(self, code_processor_thread):
        threading.Thread.__init__(self)
        self.code_processor_thread = code_processor_thread
        LOGGER.info('Starting other events thread.')

    def run(self):
        while True:
            key = hardware.wait_for_other_event()
            LOGGER.info('Got other event: %s', key)
            hardware.flash_busy()            
            

def init():
    LOGGER.info('Starting up...')
    hardware.flash_busy()
    hardware.flash_ok()
    codebuffer = []

    code_processor_thread = CodeProcessor()
    code_processor_thread.start()

    other_events_thread = OtherEventsListener(code_processor_thread)
    other_events_thread.start()

    LOGGER.info('Now just looping.')
    other_events_thread.join()  # Never happens


init()
