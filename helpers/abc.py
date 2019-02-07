INDEX_IDENTIFIER = "X:"
TITLE_IDENTIFIER = "T:"
COMPOSER_IDENTIFIER = "C:"
TRANSCRIBER_IDENTIFIER = "Z:"
SOURCE_IDENTIFIER = "S:"
ORIGIN_IDENTIFIER = "O:"
NOTES_IDENTIFIER = "N:"
METER_IDENTIFIER = "M:"
NOTE_LENGTH_IDENTIFIER = "L:"
KEY_IDENTIFIER = "K:"

BLANK_LINE_IDENTIFIER = "%"
RECENT_BLANK_LINE_IDENTIFIER = "[%"
WORD_LINE_IDENTIFIER = "W:"
RECENT_WORD_LINE_IDENTIFIER = "[W:"


class Abc:
    index = "1"
    title = ""
    composer = ""
    transcriber = ""
    source = ""
    origin = ""
    notes = []
    meter = "C"
    note_length = "1/8"
    key = ""
    music = ""

    def header(self):
        header = ""
        if self.index:
            header = INDEX_IDENTIFIER + " " + self.index + "\n"
        if self.title:
            header = header + TITLE_IDENTIFIER + " " + self.title + "\n"
        if self.composer:
            header = header + COMPOSER_IDENTIFIER + " " + self.composer + "\n"
        if self.transcriber:
            header = header + TRANSCRIBER_IDENTIFIER + " " + self.transcriber + "\n"
        if self.source:
            header = header + SOURCE_IDENTIFIER + " " + self.source + "\n"
        if self.origin:
            header = header + ORIGIN_IDENTIFIER + " " + self.origin + "\n"
        for note in self.notes:
            header = header + NOTES_IDENTIFIER + " " + note + "\n"
        if self.meter:
            header = header + METER_IDENTIFIER + " " + self.meter + "\n"
        if self.note_length:
            header = header + NOTE_LENGTH_IDENTIFIER + " " + self.note_length + "\n"
        if self.key:
            header = header + KEY_IDENTIFIER + " " + self.key + "\n"

        return header

