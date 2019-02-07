from helpers import abc
from helpers import sjkabc

# 4 Octaves of notes in abc notation
NOTES = ("C,", "D,", "E,", "F,", "G,", "A,", "B,",
         "C", "D", "E", "F", "G", "A", "B",
         "c", "d", "e", "f", "g", "a", "b",
         "c'", "d'", "e'", "f'", "g'", "a'", "b'")

NOTES_WITH_SHARPS = ("C,", "D,", "F,", "G,", "A,",
                     "C", "D", "F", "G", "A",
                     "c", "d", "f", "g", "a",
                     "c'", "d'", "f'", "g'", "a'")

NOTES_WITH_FLATS = ("D,", "E,", "G,", "A,", "B,",
                    "D", "E", "G", "A", "B",
                    "d", "e", "g", "a", "b",
                    "d'", "e'", "g'", "a'", "b'")

# ^^: double sharp, __: double flat
NOTES_ACCIDENTALS = ('^', '=', '_', '^^', '__')

ROOTS = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
CHORD_ACCIDENTALS = ('b', '#')
# m = min, aug = +
CHORD_TYPES = ('m', 'min', 'maj', 'dim', 'aug', '+', 'sus')
CHORD_INTERVALS = ('3', '5', '7', '9')

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

def chords_builder(label):
    chords = {}
    #label = 0

    # m, min and aug, + will share labels
    # Roots + Chord_types
    for root in ROOTS:
        for chord_type in CHORD_TYPES:
            if chord_type == 'min':
                chord = '"' + root + 'm' + '"'
                if chord in chords:
                    previous_label = chords.get(chord)
                    chords['"' + root + chord_type + '"'] = previous_label
                else:
                    chords['"' + root + chord_type + '"'] = label
                    label += 1
            elif chord_type == '+':
                chord = '"' + root + 'aug' + '"'
                if chord in chords:
                    previous_label = chords.get(chord)
                    chords['"' + root + chord_type + '"'] = previous_label
                else:
                    chords['"' + root + chord_type + '"'] = label
                    label += 1
            else:
                chords['"' + root + chord_type + '"'] = label
                label += 1

    # m, min and aug, + will share labels
    # Roots + Chord_types + Chord_intervals
    for root in ROOTS:
        for chord_type in CHORD_TYPES:
            for chord_interval in CHORD_INTERVALS:
                if chord_type == 'min':
                    chord = '"' + root + 'm' + chord_interval + '"'
                    if chord in chords:
                        previous_label = chords.get(chord)
                        chords['"' + root + chord_type + chord_interval + '"'] = previous_label
                    else:
                        chords['"' + root + chord_type + chord_interval + '"'] = label
                        label += 1
                elif chord_type == '+':
                    chord = '"' + root + 'aug' + chord_interval + '"'
                    if chord in chords:
                        previous_label = chords.get(chord)
                        chords['"' + root + chord_type + chord_interval + '"'] = previous_label
                    else:
                        chords['"' + root + chord_type + chord_interval + '"'] = label
                        label += 1
                else:
                    chords['"' + root + chord_type + chord_interval + '"'] = label
                    label += 1

    # m, min and aug, + will share labels
    # Roots + Chord_Accidentals + Chord_types
    for root in ROOTS:
        for chord_accidental in CHORD_ACCIDENTALS:
            for chord_type in CHORD_TYPES:
                if chord_type == 'min':
                    chord = '"' + root + chord_accidental + 'm' + '"'
                    if chord in chords:
                        previous_label = chords.get(chord)
                        chords['"' + root + chord_accidental + chord_type + '"'] = previous_label
                    else:
                        chords['"' + root + chord_accidental + chord_type + '"'] = label
                        label += 1
                elif chord_type == '+':
                    chord = '"' + root + chord_accidental + 'aug' + '"'
                    if chord in chords:
                        previous_label = chords.get(chord)
                        chords['"' + root + chord_accidental + chord_type + '"'] = previous_label
                    else:
                        chords['"' + root + chord_accidental + chord_type + '"'] = label
                        label += 1
                else:
                    chords['"' + root + chord_accidental + chord_type + '"'] = label
                    label += 1

    # m, min and aug, + will share labels
    # Roots + Chord_Accidentals + Chord_types + Chord_intervals
    for root in ROOTS:
        for chord_accidental in CHORD_ACCIDENTALS:
            for chord_type in CHORD_TYPES:
                for chord_interval in CHORD_INTERVALS:
                    if chord_type == 'min':
                        chord = '"' + root + chord_accidental + 'm' + chord_interval + '"'
                        if chord in chords:
                            previous_label = chords.get(chord)
                            chords['"' + root + chord_accidental + chord_type + chord_interval + '"'] = previous_label
                        else:
                            chords['"' + root + chord_accidental + chord_type + chord_interval + '"'] = label
                            label += 1
                    elif chord_type == '+':
                        chord = '"' + root + chord_accidental + 'aug' + chord_interval + '"'
                        if chord in chords:
                            previous_label = chords.get(chord)
                            chords['"' + root + chord_accidental + chord_type + chord_interval + '"'] = previous_label
                        else:
                            chords['"' + root + chord_accidental + chord_type + chord_interval + '"'] = label
                            label += 1
                    else:
                        chords['"' + root + chord_accidental + chord_type + chord_interval + '"'] = label
                        label += 1

    # print(chords)
    return label, chords
    # When predicting the notes of a song, if we can calculate in some way the offset, it's possible to add duration to the output

def notes_builder(label):
    notes = {}
    #label = 0

    # Combine notes with accidentals, making sure we skip the notes that only have naturals,
    # that corresponding flats and sharps share the same labels and that notes and their corresponding naturals
    # also share the same labels

    # Notes
    for note in NOTES:
        notes[note] = label
        label += 1

    # Combine notes with naturals
    for note in NOTES:
        previous_label = notes[note]
        notes[NOTES_ACCIDENTALS[1] + note] = previous_label

    # Combine notes with sharps
    for note in NOTES_WITH_SHARPS:
        notes[NOTES_ACCIDENTALS[0] + note] = label
        label += 1

    # Combine notes with flats
    # Every flat has a sharp and we already added all the sharps so the labels will not increase
    # ^A = _B, ^C = _D, ^D = _E, F# = _G, G# = _A
    sharp = 0
    for note in NOTES_WITH_FLATS:
        previous_label = notes[NOTES_ACCIDENTALS[0] + NOTES_WITH_SHARPS[sharp]]
        notes[NOTES_ACCIDENTALS[2] + note] = previous_label
        sharp += 1

    # Due to lack of knowledge we will ignore double sharps and double flats for now

    # print(notes)
    return label, notes

def notes_and_chords_builder():
    label = 0

    label, notes = notes_builder(label)
    label, chords = chords_builder(label)

    notes_and_chords = notes
    notes_and_chords.update(chords)

    print(notes_and_chords)
    return notes_and_chords