import os
import glob
import tempfile
from helpers import abc_helper
from helpers import librosa_helper

dataset_source = 'dataset_source/'

notes_and_chords = abc_helper.notes_and_chords_builder()

for name in os.listdir(dataset_source):
    midi_files = glob.glob(os.path.join(dataset_source + name + '/', '*.mid'))
    abc_files = glob.glob(os.path.join(dataset_source + name + '/', '*.abc'))

    if len(midi_files) > 1:
        print("Error - More then 1 midi file present in folder: " + dataset_source + name + '/')
        continue

    if len(abc_files) > 1:
        print("Error - More then 1 abc file present in folder: " + dataset_source + name + '/')
        continue

    with tempfile.TemporaryDirectory() as tmp_dir:
        x, sr, onset_times = librosa_helper.load(midi_files[0], tmp_dir)
        print("Tune: " + abc_files[0])
        print("Onsets detected: " + str(len(onset_times)))
        tune = abc_helper.read_abc(abc_files[0])
        tune_notes_and_chords = abc_helper.get_notes_chords(tune.music)
        print("Notes parsed from abc file: " + str(len(tune_notes_and_chords.values())))
        if len(tune_notes_and_chords.values()) != len(onset_times):
            print("Mismatch between notes parsed and onsets detected.")
        else:
            librosa_helper.compute_cqt_features(tune_notes_and_chords, x, sr, 'dataset_cqt')
