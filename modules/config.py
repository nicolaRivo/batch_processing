sr = 44100
store_cache = True
use_artist_name = False
surprise_mode = False
start_index = 0
chunk_size = 20


# Configuration for stem processing
config_stems_drums = {
    "process_stft_and_save": True,
    "process_SSM_and_chr_and_save": True,
    "process_mel_spectrogram_and_save": True,
    "process_harmonic_cqt_and_percussive_sfft_and_save": False,
    "process_harmonic_cqt_and_harmonic_mel_and_save": False
}

config_stems_drumless = {
    "process_stft_and_save": True,
    "process_SSM_and_chr_and_save": True,
    "process_mel_spectrogram_and_save": True,
    "process_harmonic_cqt_and_percussive_sfft_and_save": False,
    "process_harmonic_cqt_and_harmonic_mel_and_save": True
}


# --------------------------------------------------------------
# Configuration for directory options and file paths
# --------------------------------------------------------------

# Path to the configuration file that stores the last used directories
config_file_path = 'last_used_folders.json'

# --------------------------------------------------------------
# Audio files root directory options
# --------------------------------------------------------------
audio_files_root_dir_options = [
    "/Users/nicola/Documents/MSc SOund Design 20-24/Final Project",
    "/Volumes/Nicola Projects SSD1TB/",
    "/Volumes/Arancione"
]

# --------------------------------------------------------------
# Audio files location (subdirectory) options
# --------------------------------------------------------------
audio_files_location_options = [
    "Sound/My_Productions",
    "Sound/My_Productions/Final",
    "Musica Flac",
    "Sound/Audio_Files"
]

# --------------------------------------------------------------
# Graphs root directory options
# --------------------------------------------------------------
graphs_root_dir_options = [
    '/Volumes/Nicola Projects SSD1TB/graphs',
    '/Users/nicola/Documents/Graphs_Alternative_Location'
]

# --------------------------------------------------------------
# Graphs location options (subdirectory within graphs root directory)
# --------------------------------------------------------------
graphs_location_options = [
    "myProductions",
    "anotherLocation",
    "myFaves_new"
]
