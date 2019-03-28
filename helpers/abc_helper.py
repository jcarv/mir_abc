import re
from helpers import abc

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
        elif line.startswith(abc.TEMPO_IDENTIFIER):
            pass
        elif line.startswith(abc.INFORMATION_IDENTIFIER):
            pass
        elif line.startswith(abc.RHYTHM_IDENTIFIER):
            pass
        elif line.startswith(abc.BOOK_IDENTIFIER):
            pass
        elif line.startswith(abc.FILE_NAME_IDENTIFIER):
            pass
        elif line.startswith(abc.AREA_IDENTIFIER):
            pass
        elif (not line.upper().startswith(abc.BLANK_LINE_IDENTIFIER) and
              not line.upper().startswith(abc.RECENT_BLANK_LINE_IDENTIFIER) and
              not line.upper().startswith(abc.WORD_LINE_IDENTIFIER) and
              not line.upper().startswith(abc.RECENT_BLANK_LINE_IDENTIFIER)):
            tune.music = tune.music + line

    return tune


def write_abc(filename, tune):
    f = open(filename, "w")
    f.write(tune.header())
    f.write(tune.music)


# chords_builder will not be used for now
def chords_builder(label):
    chords = {}

    # Need to fix this, major chords should share labels with these chords
    for root in NOTES:
        chords['"' + root + '"'] = label
        label += 1

    # Need to fix this, major chords should share labels with these chords
    for root in NOTES:
        for chord_interval in CHORD_INTERVALS:
            chords['"' + root + chord_interval + '"'] = label
            label += 1

    # m, min and aug, + will share labels
    # Roots + Chord_types
    for root in NOTES:
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
    for root in NOTES:
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
    for root in NOTES:
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
    for root in NOTES:
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
    return label, chords


def notes_builder(label):
    notes = {}

    # Combine notes with accidentals, making sure we skip the notes that only have naturals,
    # that corresponding flats and sharps share the same labels and that notes and their corresponding naturals
    # also share the same labels

    # Notes
    for note in NOTES:
        notes[note] = label
        label += 1

    # Combine notes with naturals
    # The naturals annotation is being ignored
    # for note in NOTES:
    #    previous_label = notes[note]
    #    notes[NOTES_ACCIDENTALS[1] + note] = previous_label

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
    return label, notes


def notes_and_chords_builder():
    label = 0

    label, notes = notes_builder(label)
    label, chords = chords_builder(label)

    notes_and_chords = notes
    notes_and_chords.update(chords)
    return notes_and_chords


def expand_parts(abc):
    parsed_abc = abc
    start = 0

    parsed_abc = parsed_abc.replace('::', ':||:')

    while True:
        end = parsed_abc.find(':|', start)
        if end == -1:
            break

        new_start = parsed_abc.rfind('|:', 0, end)
        if new_start != -1:
            start = new_start+2

        tmp = []
        if end + 2 < len(parsed_abc) and parsed_abc[end+2].isdigit():
            first_ending_start = parsed_abc.rfind('|', 0, end)
            num_bars = 1
            if not parsed_abc[first_ending_start+1].isdigit():
                first_ending_start = parsed_abc.rfind('|', 0,
                                                      first_ending_start)
                num_bars = 2

            tmp.append(parsed_abc[start:first_ending_start])
            tmp.append('|')
            tmp.append(parsed_abc[first_ending_start+2:end])
            tmp.append('|')

            second_ending_start = end+2
            second_ending_end = None
            for i in range(num_bars):
                second_ending_end = parsed_abc.find('|', second_ending_start)

            tmp.append(parsed_abc[start:first_ending_start])
            tmp.append('|')
            tmp.append(parsed_abc[second_ending_start+1:second_ending_end])
            parsed_abc = parsed_abc.replace(
                parsed_abc[start:second_ending_end],
                ''.join(tmp), 1)
            start += len(tmp)
        else:
            tmp.append(parsed_abc[start:end])
            tmp.append('|')
            tmp.append(parsed_abc[start:end])
            tmp.append('|')
            parsed_abc = parsed_abc.replace(parsed_abc[start:end+2],
                                            ''.join(tmp), 1)
            start += len(tmp)

    for rep in ['|:', ':', ']']:
        parsed_abc = parsed_abc.replace(rep, '')
    parsed_abc = parsed_abc.replace('||', '|')

    return parsed_abc


def get_notes_chords(song):
    tune_notes_and_chords = {}
    tune = abc.Abc()
    tune.music = song
    # Remove grace naturalizations
    tune.music = ''.join(c for c in tune.music if c not in "=")
    # Remove grace annotations
    tune.music = ''.join(c for c in tune.music if c not in "{}")
    # Remove slurs (still not sure on how to handle ties: -)
    tune.music = ''.join(c for c in tune.music if c not in "()")
    # Remove ornaments
    tune.music = ''.join(c for c in tune.music if c not in ".~HKkMOPSTuv")
    # Remove rests
    tune.music = ''.join(c for c in tune.music if c not in "z")
    # Remove broken rhythms
    tune.music = ''.join(c for c in tune.music if c not in "<>")
    #
    tune.music = ''.join(c for c in tune.music if c not in "\\")
    # Extend repetitions
    tune.music = expand_parts(tune.music)
    # Remove bars
    tune.music = ''.join(c for c in tune.music if c not in "| ")
    # Remove note duration
    tune.music = ''.join(c for c in tune.music if c not in "0123456789")
    # Remove unknown annotations
    #atencao aos sharps e ao resto
    tune.music = ''.join(c for c in tune.music if c not in "/^_-![")

    counter = 0

    # Remove chords
    tune.music = re.sub('\"([^"]*)\"*', '', tune.music)

    i = 0
    print(tune.music)
    for c in tune.music:
        if c != "'" and c != ",":
            if i+1 < len(tune.music):
                if tune.music[i+1] == "'" or tune.music[i+1] == ",":
                    tune_notes_and_chords[counter] = c + tune.music[i+1]
                    counter += 1
                else:
                    tune_notes_and_chords[counter] = c
                    counter += 1
            else:
                tune_notes_and_chords[counter] = c
                counter += 1
        i += 1

    return tune_notes_and_chords
