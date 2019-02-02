from Helpers import abc


def read_abc(filename):
    with open(filename) as f:
        content = f.read().splitlines()

    tune = abc.Abc()

    for line in content:
        if line.startswith(abc.INDEX_IDENTIFIER):
            tune.index = line.split(abc.INDEX_IDENTIFIER)[1]
        elif line.startswith(abc.TITLE_IDENTIFIER):
            tune.title = line.split(abc.TITLE_IDENTIFIER)[1]
        elif line.startswith(abc.COMPOSER_IDENTIFIER):
            tune.composer = line.split(abc.COMPOSER_IDENTIFIER)[1]
        elif line.startswith(abc.TRANSCRIBER_IDENTIFIER):
            tune.transcriber = line.split(abc.TRANSCRIBER_IDENTIFIER)[1]
        elif line.startswith(abc.SOURCE_IDENTIFIER):
            tune.source = line.split(abc.SOURCE_IDENTIFIER)[1]
        elif line.startswith(abc.ORIGIN_IDENTIFIER):
            tune.origin = line.split(abc.ORIGIN_IDENTIFIER)[1]
        elif line.startswith(abc.NOTES_IDENTIFIER):
            tune.notes.append(line.split(abc.NOTES_IDENTIFIER)[1])
        elif line.startswith(abc.METER_IDENTIFIER):
            tune.meter = line.split(abc.METER_IDENTIFIER)[1].replace(" ", "")
        elif line.startswith(abc.NOTE_LENGTH_IDENTIFIER):
            tune.note_length = line.split(abc.NOTE_LENGTH_IDENTIFIER)[1].replace(" ", "")
        elif line.startswith(abc.KEY_IDENTIFIER):
            tune.key = line.split(abc.KEY_IDENTIFIER)[1].replace(" ", "")
        elif (not line.upper().startswith(abc.BLANK_LINE_IDENTIFIER) and
              not line.upper().startswith(abc.RECENT_BLANK_LINE_IDENTIFIER) and
              not line.upper().startswith(abc.WORD_LINE_IDENTIFIER) and
              not line.upper().startswith(abc.RECENT_BLANK_LINE_IDENTIFIER)):
            tune.music = tune.music + line + "\n"

    return tune


def write_abc(filename, tune):
    f = open(filename, "w")
    f.write(tune.header())
    f.write(tune.music)
