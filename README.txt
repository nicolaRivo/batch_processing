
░▒▓████████▓▒░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓██████████████▓▒░ ░▒▓██████▓▒░  
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓███████▓▒░░▒▓████████▓▒░▒▓██████▓▒░░▒▓████████▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                                                
                                                                                                                
                        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓███████▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░                        
                        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                       
                         ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                       
                         ░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                       
                          ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                       
                          ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░                       
                           ░▒▓██▓▒░  ░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░                       
                                                                                                                
                                                                                                                



=============================================================
                TrafalmaVision - Batch Processing Utility
=============================================================

This script automates batch processing of files in a directory, with customizable configurations defined in `config.py`.

=============================================================
                    How to Launch the Program
=============================================================

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Set up the environment:

    ```bash
    python -m venv env
    source env/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the batch processing script:

    ```bash
    python batch_processing.py
    ```

=============================================================
                     Main Settings
=============================================================

- **sr**: Sampling rate for audio (e.g., `44100` for CD quality).
    ```python
    sr = 44100
    ```

- **store_cache**: Whether to cache results for faster reprocessing.
    ```python
    store_cache = True
    ```

- **use_artist_name**: Include artist name in output file names.
    ```python
    use_artist_name = False
    ```

- **surprise_mode**: Randomly selects a file from the selected folder, converts the name to HEX, generates all graphs, and stores the secret name mapping in `.encrypted-name.txt`.
    ```python
    surprise_mode = False
    ```

- **start_index**: Index from which to start processing in batch jobs.
    ```python
    start_index = 0
    ```

- **chunk_size**: Number of files to process in each batch.
    ```python
    chunk_size = 20
    ```

=============================================================
                      Saving Settings
=============================================================

You can specify custom directories for audio files and graphs by editing the following settings in `config.py`:

### Audio Files Root Directories:
```python
audio_files_root_dir_options = [
    "/Users/nicola/Documents/MSc SOund Design 20-24/Final Project",
    "/Volumes/Nicola Projects SSD1TB/",
    "/Volumes/Arancione"
]
```

### Audio Files Location Subdirectories:
```python
audio_files_location_options = [
    "Sound/My_Productions",
    "Sound/My_Productions/Final",
    "Musica Flac",
    "Sound/Audio_Files"
]
```

### Graphs Root Directories:
```python
graphs_root_dir_options = [
    '/Volumes/Nicola Projects SSD1TB/graphs',
    '/Users/nicola/Documents/Graphs_Alternative_Location'
]
```

### Graphs Location Subdirectories:
```python
graphs_location_options = [
    "myProductions",
    "anotherLocation",
    "myFaves_new"
]
```

**How to Edit the Directories:**
- Simply modify the paths in `config.py` to point to your desired folders.
- The **location subdirectories** will be concatenated with the selected root directory, allowing you to manage multiple locations or external drives. You can easily navigate between different folders within your chosen root directory during file processing.

=============================================================
                      Graphs Settings
=============================================================

### **Configuring which graphs to output:**
You can control which graphs are generated for the stems by tweaking the following configurations in `config.py`. Set the flags for each graph type to `True` or `False` depending on whether you want it processed and saved.

Example configuration for processing stems with drums:

```python
# Configuration for stem processing with drums
config_stems_drums = {
    "process_stft_and_save": True,  # Generate and save STFT graph
    "process_SSM_and_chr_and_save": True,  # Generate and save SSM and Chromagram
    "process_mel_spectrogram_and_save": True,  # Generate and save Mel Spectrogram
    "process_harmonic_cqt_and_percussive_sfft_and_save": False,  # Disable Harmonic CQT and Percussive STFT
    "process_harmonic_cqt_and_harmonic_mel_and_save": False  # Disable Harmonic CQT and Harmonic Mel Spectrogram
}
```

For stems without drums:

```python
# Configuration for stem processing without drums
config_stems_drumless = {
    "process_stft_and_save": True,  # Generate and save STFT graph
    "process_SSM_and_chr_and_save": True,  # Generate and save SSM and Chromagram
    "process_mel_spectrogram_and_save": True,  # Generate and save Mel Spectrogram
    "process_harmonic_cqt_and_percussive_sfft_and_save": False,  # Disable Harmonic CQT and Percussive STFT
    "process_harmonic_cqt_and_harmonic_mel_and_save": True  # Enable Harmonic CQT and Harmonic Mel Spectrogram
}
```

=============================================================
                        Dependencies
=============================================================

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

