import os
import json
from modules.utility_functions import *
from modules.stem_split import make_drumTrack_and_drumLessTrack
from modules.saving_functions import *
from modules import config

# ─────────────────────────────────────────────────────────────────────────────
# MAIN BATCH PROCESSING FUNCTION
# ─────────────────────────────────────────────────────────────────────────────


def main():
    """
    Main function to handle batch processing of audio files.
    """

    welcome_message()

    print("Starting batch processing...")
    sr = config.sr
    store_cache = config.store_cache
    use_artist_name = config.use_artist_name
    surprise_mode = config.surprise_mode
    start_index = config.start_index
    chunk_size = config.chunk_size
    config_stems_drums = config.config_stems_drums
    config_stems_drumless = config.config_stems_drumless

    # Load folder configurations (either from previous run or ask user)
    config_data = configure_folders(config.audio_files_root_dir_options, config.audio_files_location_options,
                                    config.graphs_root_dir_options, config.graphs_location_options)

    # Extract folder paths from the config
    audio_files_root_dir = config_data['audio_files_root_dir']
    audio_files_location = config_data['audio_files_location']
    graphs_root_dir = config_data['graphs_root_dir']
    graphs_location = config_data['graphs_location']

    # Construct paths based on the selected or loaded folders
    graphs_dir = os.path.join(graphs_root_dir, graphs_location)
    cache_dir = os.path.join(graphs_dir, '.feature_cache')
    stems_dir = os.path.join(graphs_dir, '.stems')
    json_file_path = os.path.join(graphs_dir, '.tracking_file.json')
    audio_files_dir = os.path.join(audio_files_root_dir, audio_files_location)

    # Check and create directories as needed
    directories_to_check = [audio_files_dir, graphs_dir, cache_dir, stems_dir]
    for directory in directories_to_check:
        ensure_directory_exists(directory)

    # Ensure the tracking JSON file exists
    ensure_json_file_exists(json_file_path)
    
    # Load the JSON tracking file
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    if surprise_mode:
        store_cache=False
        graphs_dir = os.path.join(graphs_root_dir, 'surprise_mode')
        use_artist_name = True


    while start_index is not None:
        # ─────────────────────────────────────────────────────────────────────
        # LOAD AUDIO FILES CHUNK
        # ─────────────────────────────────────────────────────────────────────
        loaded_audio_files, next_start_index = load_tracks(
            working_directory=audio_files_root_dir,
            audio_files_dir=audio_files_dir,
            json_file_path=json_file_path,
            sr=sr,
            load_all_tracks=True,
            start_index=start_index,
            chunk_size=chunk_size,
            shuffle=True,  # Enable shuffling
            surprise_mode=surprise_mode,
            use_artist_name=use_artist_name,
        )

        # ─────────────────────────────────────────────────────────────────────
        # PROCESS EACH AUDIO FILE IN THE LOADED CHUNK
        # ─────────────────────────────────────────────────────────────────────
        for audio_file in loaded_audio_files:
            


            # Get the name of the song from the audio path
            song_name = audio_file[4]

            # Create the song's directory if it doesn't exist                 
            song_dir = os.path.join(graphs_dir, song_name)
            os.makedirs(song_dir, exist_ok=True)

            # Check if the song needs processing
            if is_processing_needed(song_name, json_data):
                
                #monitor memory leak and CPU usage
                print_resource_usage()
                # Separate the stems and return drum and drumless tracks
                stem_split = make_drumTrack_and_drumLessTrack(audio_file, parent_dir=stems_dir)

                # Process drumless and drum stems
                process_all(stem_split['drumless'], json_file_path, song_dir, cache_dir=cache_dir, config=config_stems_drumless)
                process_all(stem_split['drums'], json_file_path, song_dir, cache_dir=cache_dir, config=config_stems_drums)
                
                # Process the original audio file
                process_all(audio_file, json_file_path, song_dir, cache_dir=cache_dir)

            else:
                print(f"Skipping {song_name}, all graphs are already processed.")

            # ─────────────────────────────────────────────────────────────────
            # CREATE RECAP PDF IF NOT PRESENT
            # ─────────────────────────────────────────────────────────────────

            # Create the 'recaps' directory in the graphs_location folder
            recap_dir = os.path.join(graphs_dir, 'Recaps')
            os.makedirs(recap_dir, exist_ok=True)

            # Path to save the PDF recap in the recaps folder under graphs_location
            pdf_file = os.path.join(recap_dir, f"{song_name} - Recap.pdf")
            if not os.path.exists(pdf_file):
                pngs_to_pdf(song_dir, file_name=song_name, save_path=recap_dir)


            # ─────────────────────────────────────────────────────────────────
            # CLEAN CACHE IF NECESSARY
            # ─────────────────────────────────────────────────────────────────
            if not store_cache:
                delete_cached_features(audio_file, cache_dir=cache_dir)

        # ─────────────────────────────────────────────────────────────────────
        # UPDATE THE START INDEX FOR THE NEXT CHUNK
        # ─────────────────────────────────────────────────────────────────────
        start_index = next_start_index

    print("Batch processing complete.")

# ─────────────────────────────────────────────────────────────────────────────
# PROGRAM ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()