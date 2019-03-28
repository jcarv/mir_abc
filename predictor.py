import tempfile
from helpers import librosa_helper
from tensorflow import keras
import numpy as np
from helpers import abc_helper

SONG = 'predict/prelude.mp3'

checkpoint_path = "tfdata"
model = keras.models.load_model(checkpoint_path + '/my_model.h5')

#checkpoint = tf.train.latest_checkpoint(os.path.dirname(checkpoint_path))
#print(checkpoint)

result = list()
images = list()
with tempfile.TemporaryDirectory() as tmp_dir:
    x, sr, onset_times = librosa_helper.load(SONG, tmp_dir)
    tempo = librosa_helper.get_tempo(x, sr)

    images = librosa_helper.compute_cqt_features_memory(x, sr, tmp_dir)

    predictions = model.predict(np.array(images))
    label, notes = abc_helper.notes_builder(0)
    # print(notes)
    notes_without_dups = {}

    for key, value in notes.items():
        if value not in notes_without_dups.values():
            notes_without_dups[key] = value
    # print(notes_without_dups)

    inv_map = {v: k for k, v in notes_without_dups.items()}
    # print(inv_map)
    for val in predictions:
        # print(test_labels)
        result.append(inv_map.get(np.argmax(val)))
        # print(inv_map.get(np.argmax(val)))
        # print(np.argmax(val))

    i = 0
    f = open("demofile.abc", "w")
    f.write("X: 1\n")
    f.write("T: Song predicted\n")
    f.write("Q: " + str(tempo) + "\n")
    f.write("K: none\n")
    for note in result:
        i += 1
        f.write(note)
        if i == 8:
            i = 0
            f.write(" | ")
