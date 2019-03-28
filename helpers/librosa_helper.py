import librosa
import pylab
import numpy as np
import magic
import tempfile
import helpers.abc_helper
import os
import uuid
from pydub import AudioSegment
from skimage.transform import resize
import matplotlib.image as mpimg
from librosa import display
from midi2audio import FluidSynth


def load(file_origin, file_destination):
    one_second_delay = AudioSegment.silent(duration=1000)

    mime = magic.Magic(mime=True)
    if mime.from_file(file_origin) == 'audio/midi':
        with tempfile.TemporaryDirectory() as tmp_dir:
            converted_file_destination = tmp_dir + '/converted.wav'
            converted_file = convert_midi_to_wav(file_origin, converted_file_destination)
            song = AudioSegment.from_file(converted_file)
    else:
        song = AudioSegment.from_file(file_origin)

    padded_song = one_second_delay + song
    padded_song.export(file_destination + '/dump.mp3', format="mp3")

    x, sr = librosa.load(file_destination + '/dump.mp3')

    onset_frames = librosa.onset.onset_detect(x, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames)

    return x, sr, onset_times


def convert_midi_to_wav(file_origin, file_destination):
    fs = FluidSynth('soundfonts/FluidR3_GM.sf2')
    fs.midi_to_audio(file_origin, file_destination)

    return file_destination


def compute_cqt_features(tune_notes_and_chords, x, sr, folder_path):
    onset_frames = librosa.onset.onset_detect(x, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames)

    cqt = np.abs(librosa.cqt(x, sr=sr))

    for i in range(0, onset_frames.size):
        if i == onset_frames.size - 1:
            idx = [slice(None), slice(*list(librosa.time_to_frames([onset_times[i] - 0.5, onset_times[i] + 0.5])))]
        else:
            idx = [slice(None), slice(*list(librosa.time_to_frames([onset_times[i] - 0.5, onset_times[i + 1]])))]
        pylab.axis('off')
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
        librosa.display.specshow(librosa.amplitude_to_db(cqt, ref=np.max)[idx], sr=sr, x_axis='time', y_axis='cqt_note',
                                 cmap='jet')

        label, notes_labels = helpers.abc_helper.notes_builder(0)

        directory = folder_path + "/" + str(notes_labels.get(tune_notes_and_chords[i]))
        if not os.path.exists(directory):
            os.makedirs(directory)

        pylab.savefig(directory + "/" + uuid.uuid4().hex + ".png", bbox_inches=None, pad_inches=0)
        pylab.close()


def compute_cqt_features_memory(x, sr, folder_path):
    images = list()
    onset_frames = librosa.onset.onset_detect(x, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames)

    cqt = np.abs(librosa.cqt(x, sr=sr))

    for i in range(0, onset_frames.size):
        if i == onset_frames.size - 1:
            idx = [slice(None), slice(*list(librosa.time_to_frames([onset_times[i] - 0.5, onset_times[i] + 0.5])))]
        else:
            idx = [slice(None), slice(*list(librosa.time_to_frames([onset_times[i] - 0.5, onset_times[i + 1]])))]
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
        librosa.display.specshow(librosa.amplitude_to_db(cqt, ref=np.max)[idx], sr=sr, x_axis='time', y_axis='cqt_note',
                                 cmap='jet')

        directory = folder_path
        if not os.path.exists(directory):
            os.makedirs(directory)

        unique_identifier = directory + "/" + uuid.uuid4().hex + ".png"

        pylab.savefig(unique_identifier, bbox_inches=None, pad_inches=0)
        image = resize(mpimg.imread(unique_identifier), (28, 28), anti_aliasing=True, mode='constant')
        images.append(image)
        pylab.close()

    return images


def get_tempo(x, sr):
    onset_env = librosa.onset.onset_strength(x, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)

    return int(tempo)
