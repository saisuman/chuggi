CODE_PREFIX_MUSIC = '4'

ALL_MUSIC_CODES = {
    # Load from file names
}

ALL_CODE_PREFIXES = {
    CODE_PREFIX_MUSIC: ALL_MUSIC_CODES
}

def is_complete(code):
    return len(code) >= 4
