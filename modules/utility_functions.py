import os
import math
import json
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import logging
import time
import threading
import hashlib
from pathlib import Path
import random
from cryptography.fernet import Fernet
from .graph_extraction_func import *
from .timing_utils import *
import base64
import os
from PIL import Image
import os

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s \n')

def welcome_message():
    print(r"""
          

88P'888'Y88                 dP,e,         888                     Y8b Y88888P ,e,       ,e,                   
P'  888  'Y 888,8,  ,"Y88b  8b "   ,"Y88b 888 888 888 8e   ,"Y88b  Y8b Y888P   "   dP"Y  "   e88 88e  888 8e  
    888     888 "  "8" 888 888888 "8" 888 888 888 888 88b "8" 888   Y8b Y8P   888 C88b  888 d888 888b 888 88b 
    888     888    ,ee 888  888   ,ee 888 888 888 888 888 ,ee 888    Y8b Y    888  Y88D 888 Y888 888P 888 888 
    888     888    "88 888  888   "88 888 888 888 888 888 "88 888     Y8P     888 d,dP  888  "88 88"  888 888 
                                                                                                              
                                                                                                              
                                                                                 
       Welcome to the TralfamaVision Batch Processing Script!
   ──────────────────────────────────────────────────────────────
         This script will help you process audio files in bulk.
         Get ready for a smooth and efficient audio workflow!

     🚀 Features:
     • Separate stems and process audio
     • Create Recap PDFs for your projects
     • Manage your cache and track progress

       Ready to start? Let's get those audio files processed! 🎶
   ──────────────────────────────────────────────────────────────
    """)

# --------------------------------------------------------------
# Function: pngs_to_pdf
# --------------------------------------------------------------
# Takes all PNG files in a folder, sorts them alphabetically, 
# and compiles them into a single PDF file saved in the specified folder. 
# If no file name is provided, the PDF will be named after the folder.
#
# Parameters:
# - folder_path (str): Path to the folder containing PNG files.
# - file_name (str, optional): Desired name for the output PDF file.
# - save_path (str, optional): Directory where the PDF will be saved.
#   If not provided, it will be saved in the same folder as the PNG files.
#
# Raises:
# - FileNotFoundError: If the folder does not exist.
# - ValueError: If no PNG files are found in the folder.
#
# Example usage:
# pngs_to_pdf('/path/to/folder', 'output_file_name')
# pngs_to_pdf('/path/to/folder', 'output_file_name', '/path/to/save_folder')
# --------------------------------------------------------------
def pngs_to_pdf(folder_path, file_name=None, save_path=None):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder {folder_path} does not exist")
    
    # Get the name of the folder for default PDF file name
    if file_name is None:
        file_name = os.path.basename(os.path.normpath(folder_path))
    
    # Fetch all PNG files in the folder and sort them alphabetically
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    png_files.sort()  # Alphabetical sorting
    
    if not png_files:
        raise ValueError(f"No PNG files found in {folder_path}")
    
    # Prepare the list of Image objects to convert to PDF
    image_list = []
    for png_file in png_files:
        image_path = os.path.join(folder_path, png_file)
        img = Image.open(image_path)
        # Convert image to RGB mode (required for saving as PDF)
        img_rgb = img.convert('RGB')
        image_list.append(img_rgb)
    
    # If no save_path is provided, save in the same folder as PNG files
    if save_path is None:
        save_path = folder_path
    
    # Ensure save_path directory exists
    os.makedirs(save_path, exist_ok=True)

    # Create the output PDF path
    output_pdf_path = os.path.join(save_path, f"{file_name} - Recap.pdf")
    
    # Save images as a single PDF
    if image_list:
        # Save all images into one PDF
        image_list[0].save(output_pdf_path, save_all=True, append_images=image_list[1:])
    
    print(f"PDF saved at: {output_pdf_path}")



# Generate a key for encryption/decryption (this should be securely stored)
#key = Fernet.generate_key()
#cipher_suite = Fernet(key)



# --------------------------------------------------------------
# Function: decrypt_text
# --------------------------------------------------------------
# Decrypts an encrypted text using a provided decryption key.
#
# Parameters:
# - encrypted_text (str): The base64-encoded encrypted text.
# - decryption_key (str): Base64-encoded decryption key.
#
# Returns:
# - str: The decrypted text.
#
# Example usage:
# decrypted = decrypt_text(encrypted_text, decryption_key)
# print(decrypted)
# --------------------------------------------------------------
def decrypt_text(encrypted_text, decryption_key):
    """
    Decrypts the encrypted text using the provided decryption key.
    
    Parameters:
    - encrypted_text: str, the encrypted text to be decrypted.
    - decryption_key: str, the key to be used for decryption.
    
    Returns:
    - str, the decrypted text (original track name).
    """
    # Decode the key and the encrypted text from base64
    key = base64.urlsafe_b64decode(decryption_key.encode())
    cipher_suite = Fernet(key)
    
    # Decode the encrypted text from base64 and then decrypt it
    decrypted_text = cipher_suite.decrypt(base64.urlsafe_b64decode(encrypted_text.encode()))
    
    return decrypted_text.decode()


# --------------------------------------------------------------
# Function: get_encrypted_data
# --------------------------------------------------------------
# Reads the encrypted name and decryption key from a file.
#
# Parameters:
# - file_path (str): The path to the file containing encrypted data.
#
# Returns:
# - tuple: (encrypted_name, decryption_key), both as strings.
#
# Example usage:
# encrypted_name, decryption_key = get_encrypted_data('/path/to/file.txt')
# print(encrypted_name, decryption_key)
# --------------------------------------------------------------
def get_encrypted_data(file_path):
    """
    Reads the encrypted name and decryption key from the specified file.
    
    Parameters:
    - file_path: str, the path to the file containing the encrypted data.
    
    Returns:
    - tuple of (encrypted_name, decryption_key), both as strings.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
        encrypted_name = lines[0].split(": ")[1].strip()
        decryption_key = lines[1].split(": ")[1].strip()
    
    return encrypted_name, decryption_key

# --------------------------------------------------------------
# Function: ensure_json_file_exists
# --------------------------------------------------------------
# Ensures that the JSON file exists at the specified path.
# If the file doesn't exist, an empty JSON file is created.
#
# Parameters:
# - json_path (str): Path to the JSON file.
#
# Raises:
# - Exception: If there is an error creating or verifying the JSON file.
#
# Example usage:
# ensure_json_file_exists('/path/to/data.json')
# --------------------------------------------------------------
def ensure_json_file_exists(json_path):
    """
    Checks if the JSON file exists at the specified path.
    If it doesn't exist, an empty JSON file with a valid JSON object is created.
    """
    if not os.path.exists(json_path):
        try:
            with open(json_path, 'w') as json_file:
                json.dump({}, json_file)
            print(f"JSON file created at: {json_path}")
        except Exception as e:
            print(f"Error creating JSON file at {json_path}: {e}")
    else:
        try:
            with open(json_path, 'r') as json_file:
                json.load(json_file)
            print(f"JSON file already exists and is valid at: {json_path}")
        except json.JSONDecodeError:
            with open(json_path, 'w') as json_file:
                json.dump({}, json_file)
            print(f"Invalid JSON file at {json_path} was overwritten with a valid empty JSON object.")
        except Exception as e:
            print(f"Error verifying JSON file at {json_path}: {e}")

# --------------------------------------------------------------
# Function: ensure_directory_exists
# --------------------------------------------------------------
# Ensures that the specified directory exists. If it doesn't exist,
# the user is prompted to create it.
#
# Parameters:
# - directory (str): The directory path to check or create.
#
# Raises:
# - FileNotFoundError: If the directory is not created and doesn't exist.
#
# Example usage:
# ensure_directory_exists('/path/to/directory')
# --------------------------------------------------------------
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        create_dir = input(f"The directory '{directory}' does not exist. Do you want to create it? (y/n): ")
        if create_dir.lower() == 'y':
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            raise FileNotFoundError(f"Directory '{directory}' not found and was not created.")

# --------------------------------------------------------------
# Function: encrypt
# --------------------------------------------------------------
# Encrypts a given text using a simple Caesar cipher based on the provided key.
#
# Parameters:
# - text (str): The text to encrypt.
# - key (str): The key to use for the encryption (determines shift).
#
# Returns:
# - str: The encrypted text.
#
# Example usage:
# encrypted = encrypt('hello world', 'key')
# print(encrypted)
# --------------------------------------------------------------
def encrypt(text, key):
    encrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(text):
        shift = ord(key[i % key_length].lower()) - ord('a')
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
        else:
            encrypted_char = char
        encrypted_text.append(encrypted_char)
    
    return ''.join(encrypted_text)

# --------------------------------------------------------------
# Function: decrypt
# --------------------------------------------------------------
# Decrypts a text encrypted using a simple Caesar cipher based on the provided key.
#
# Parameters:
# - encrypted_text (str): The encrypted text.
# - key (str): The key used for decryption.
#
# Returns:
# - str: The decrypted text.
#
# Example usage:
# decrypted = decrypt('encrypted_text', 'key')
# print(decrypted)
# --------------------------------------------------------------
def decrypt(encrypted_text, key):
    decrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(encrypted_text):
        shift = ord(key[i % key_length].lower()) - ord('a')
        if char.isalpha():
            base = ord('a') if char.islower() else ord('A')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
        else:
            decrypted_char = char
        decrypted_text.append(decrypted_char)
    
    return ''.join(decrypted_text)

# --------------------------------------------------------------
# Function: explore_audio_files
# --------------------------------------------------------------
# Explores the given directory and subdirectories to collect all audio files.
#
# Parameters:
# - audio_files_dir (str): The root directory to search for audio files.
#
# Returns:
# - list: A list of file paths for the found audio files.
#
# Example usage:
# audio_files = explore_audio_files('/path/to/audio/files')
# print(audio_files)
# --------------------------------------------------------------
def explore_audio_files(audio_files_dir):
    """
    Explore the directory and its subdirectories to gather all audio files.
    Returns a list of file paths.
    """
    audio_files_paths = []
    for root, _, files in os.walk(audio_files_dir):
        for file in files:
            if file.endswith((".flac", ".wav", ".mp3", ".aiff")):
                file_path = os.path.join(root, file)
                audio_files_paths.append(file_path)
    return audio_files_paths

# --------------------------------------------------------------
# Function: string_to_5_letter_hash
# --------------------------------------------------------------
# Converts a given input string into a 5-letter hash using a SHA-256 hash,
# followed by base-26 conversion (A-Z).
#
# Parameters:
# - input_string (str): The input string to hash.
#
# Returns:
# - str: A 5-letter hash representation of the input string.
#
# Example usage:
# hash_code = string_to_5_letter_hash('example string')
# print(hash_code)
# --------------------------------------------------------------
def string_to_5_letter_hash(input_string):
    # Step 1: Generate a SHA-256 hash of the input string
    hash_object = hashlib.sha256(input_string.encode())
    hex_digest = hash_object.hexdigest()
    
    # Step 2: Take the first 5 bytes (10 hex digits) of the hash
    hash_substring = hex_digest[:10]
    
    # Step 3: Convert the hex substring to an integer
    hash_integer = int(hash_substring, 16)
    
    # Step 4: Convert the integer to base-26 (A-Z)
    letters = []
    for _ in range(5):
        letters.append(chr((hash_integer % 26) + ord('A')))
        hash_integer //= 26
    
    # Step 5: Return the 5-letter hash
    return ''.join(letters)

# --------------------------------------------------------------
# Function: load_tracks
# --------------------------------------------------------------
# Loads audio tracks from a directory and manages them for playback, debugging, or
# surprise mode. Supports chunk-based loading and file shuffling.
#
# Parameters:
# - working_directory (str): The base working directory.
# - audio_files_dir (str): Directory containing audio files.
# - json_file_path (str): Path to the JSON file used for tracking.
# - sr (int): Sample rate for loading audio files (default is 44100).
# - debug (int): Flag to enable or disable debugging mode.
# - playback (int): Flag for enabling track playback.
# - file_names (str): Specific track names to load.
# - load_all_tracks (bool): Whether to load all tracks in the directory.
# - start_index (int): Start index for chunk-based loading.
# - chunk_size (int): Number of tracks to load in one chunk.
# - shuffle (bool): Whether to shuffle the track order.
# - use_artist_name (bool): Whether to use the artist's name in the track list.
# - surprise_mode (bool): Whether to load tracks in "surprise mode."
#
# Returns:
# - tuple: A list of loaded tracks and the index of the next chunk to process.
#
# Example usage:
# tracks, next_index = load_tracks('/working/dir', '/audio/files', '/path/to/json')
# --------------------------------------------------------------
def load_tracks(working_directory, audio_files_dir='', json_file_path='', sr=44100, debug=0, playback=0, file_names='', load_all_tracks=False, start_index=0, chunk_size=20, shuffle=False, use_artist_name=True, surprise_mode=False):
    """
    Initializes the working environment by setting paths, loading audio files,
    and printing relevant information in chunks. Handles surprise mode by selecting
    a single track, encrypting its name, and saving related information.
    """
    os.chdir(working_directory)
    print("Current Working Directory:", os.getcwd())

    if load_all_tracks and not audio_files_dir:
        audio_files_dir = input("Please provide the directory path containing the audio files: ")

    if not os.path.exists(audio_files_dir):
        print(f"Directory {audio_files_dir} does not exist.")
        return [], None


    if surprise_mode:
        # Seed with the current time to ensure different results each time
        random.seed(time.time())

        # Explore all files and select one randomly
        audio_files_paths = explore_audio_files(audio_files_dir)
        if not audio_files_paths:
            print("No audio files found.")
            return [], None
        
        # Select a random track
        selected_file = random.choice(audio_files_paths)
        
        # Encrypt the track name
        track_name = os.path.splitext(os.path.basename(selected_file))[0]


        # Loop until you find the folder named last_folder or reach the root directory
        if use_artist_name:
            file_path_to_process = os.path.dirname(selected_file)
            artist_name = ""
            prev_folder = os.path.basename(file_path_to_process)
            last_folder = os.path.basename(audio_files_dir)

            # Loop until you find the folder named last_folder or reach the root directory
            while prev_folder != last_folder and file_path_to_process != "/":
                if artist_name:  # If artist_name is not empty, append a separator
                    artist_name = os.path.basename(file_path_to_process) + " / " + artist_name
                else:  # If artist_name is empty, just assign the current folder name
                    artist_name = os.path.basename(file_path_to_process)

                # Move one level up in the directory tree
                file_path_to_process = os.path.dirname(file_path_to_process)
                prev_folder = os.path.basename(file_path_to_process)

            # If we stopped at last_folder, include it in the artist_name

            #print("Final artist name:", artist_name)

            track_name = f"{artist_name} - {track_name}"
        else:
            track_name = os.path.splitext(os.path.basename(selected_file))[0]

        encrypted_name_hash = string_to_5_letter_hash(track_name)

        
        # Create /surprise_file/ directory if it doesn't exist
        surprise_dir = os.path.join(working_directory, "surprise_file")
        os.makedirs(surprise_dir, exist_ok=True)
        
        # Save the encrypted name and decryption key
        encrypted_file_path = os.path.join(surprise_dir, ".encrypted-name.txt")

                # Get the current time as a timestamp
        timestamp = time.strftime("%d %B %Y - %I:%M:%S%p")


        # Prepare the new content to be added
        new_content = (
            f"{timestamp}\n"
            f"Encrypted HASH: {encrypted_name_hash}\n"
            f"Track name: {track_name}\n"

            "\n"  # Add an extra newline for separation
        )

        # Read the current content and prepend the new content
        with open(encrypted_file_path, 'r+') as f:
            current_content = f.read()  # Read the current content
            f.seek(0)  # Move the cursor to the start of the file
            f.write(new_content + current_content)  # Write the new content first, then the old content
                
        
        # Substitute file name with 'secret - {first 5 digits of the encrypted name}'
        secret_name = f"secret - {encrypted_name_hash}"
        secret_file_path = selected_file
        print(f"Surprise mode activated. Track: {secret_name}")
        
        # Only this track will be processed
        audio_files_paths = [secret_file_path]
        save_dir = surprise_dir  # All outputs will be saved here

    else:
        # Regular mode, loading all tracks or specific files
        if load_all_tracks:
            print("Exploring all audio files in the directory and subdirectories...")
            audio_files_paths = explore_audio_files(audio_files_dir)
        else:
            audio_files_paths = []
            not_found = 0
            print("Starting file search...")

            if file_names == '':
                file_names = [
                    # Default file names list as provided earlier
                ]

            for file_name in file_names:
                found_something = False

                for root, _, files in os.walk(audio_files_dir):
                    file_paths = {
                        "flac": os.path.join(root, f"{file_name}.flac"),
                        "wav": os.path.join(root, f"{file_name}.wav"),
                        "mp3": os.path.join(root, f"{file_name}.mp3"),
                        "aiff": os.path.join(root, f"{file_name}.aiff")
                    }

                    for ext, path in file_paths.items():
                        if os.path.exists(path):
                            audio_files_paths.append(path)
                            print(f"{file_name}.{ext} found at {path}!\n")
                            found_something = True
                            break

                    if found_something:
                        break

                if not found_something:
                    not_found += 1
                    print(f"{file_name} wasn't found in any supported format.\n")

            if not_found == 0:
                print("All Tracks Found \n\n(: \n")
            else:
                print(f"{not_found} tracks were not found!\n\n): \n")
        
        # Shuffle the list if requested
        if shuffle:
            random.shuffle(audio_files_paths)

        save_dir = os.path.join(working_directory, "output_files")

    # Process files in chunks
    total_files = len(audio_files_paths)
    end_index = min(start_index + chunk_size, total_files)

    if start_index >= total_files:
        print("All files have been processed.")
        return [], None

    chunk_files_paths = audio_files_paths[start_index:end_index]
    loaded_audio_files = []

    print(f"Processing files from {start_index + 1} to {end_index} of {total_files}...")

    for path in chunk_files_paths:
        try:
            y, sr = librosa.load(path, sr=sr)
            duration = librosa.get_duration(y=y, sr=sr)
            # Extract artist name from the parent folder if use_artist_name is True
            if surprise_mode:
                song_name = encrypted_name_hash
            else:
                song_name = os.path.splitext(os.path.basename(path))[0]
                
            loaded_audio_files.append((y, sr, path, duration, song_name))
            

            if surprise_mode:
                print(f"Audio file correctly loaded: \nsr = {sr} \n duration = {duration} seconds \n\n")           
            else:
                print(f"Audio file correctly loaded from {path}: \nsr = {sr} \n duration = {duration} seconds \n\n")
        except Exception as e:
            print(f"Failed to load audio file from {path}: {e}")

    print("================================")
    print(f"Processed {len(loaded_audio_files)} files in this chunk.\n")

    loaded_audio_files.sort(key=lambda x: x[3])

    print("Tracks sorted by duration (shortest to longest):")
    for i, (y, sr, path, duration, song_name) in enumerate(loaded_audio_files, start_index + 1):
        if surprise_mode:
            print(f"{i}. {encrypted_name_hash} - {duration:.2f} seconds")
        else:
            print(f"{i}. {song_name} - {duration:.2f} seconds")
    print("================================\n")

    if playback == 1 and loaded_audio_files:
        for _, _, path, _, _ in loaded_audio_files:
            print(f"Listen to {path}")

    # Determine if there are more files to process
    next_start_index = end_index if end_index < total_files else None

    return loaded_audio_files, next_start_index

# --------------------------------------------------------------
# Function: is_processing_needed
# --------------------------------------------------------------
# Checks if any audio processing is needed for a track based on its status in a JSON file.
#
# Parameters:
# - track_name (str): The name of the track to check.
# - json_data (dict): The loaded JSON data that tracks processing states.
#
# Returns:
# - bool: True if processing is needed, False otherwise.
#
# Example usage:
# process_needed = is_processing_needed('track_name', json_data)
# print(process_needed)
# --------------------------------------------------------------
def is_processing_needed(track_name, json_data):
    """Check if any processing is needed for the track."""
    required_keys = [
        "STFT_processed",
        "Mel_Spectrogram_processed",
        "Harmonic_CQT_Percussive_SFFT_processed",
        "Harmonic_CQT_Harmonic_Mel_processed",
        "SSM_processed"
    ]
    if track_name in json_data:
        for key in required_keys:
            if not json_data[track_name].get(key, False):
                return True
        return False
    return True  # If track not found in JSON, assume processing is needed

# --------------------------------------------------------------
# Function: delete_cached_features
# --------------------------------------------------------------
# Deletes the cached feature file for a given audio file, if it exists.
#
# Parameters:
# - audio_file (tuple): A tuple containing (y, sr, path, duration).
# - cache_dir (str): The directory where cached feature files are stored (default: "feature_cache").
#
# Returns:
# - bool: True if the cache file was successfully deleted, False otherwise.
#
# Example usage:
# cache_deleted = delete_cached_features(audio_file)
# print(cache_deleted)
# --------------------------------------------------------------
def delete_cached_features(audio_file, cache_dir="feature_cache"):



    """
    Deletes the cached feature file for the given audio file.

    Parameters:
    - audio_file: tuple containing (y, sr, path, duration)
    - cache_dir: str, directory where cached feature files are stored

    Returns:
    - bool: True if the cache file was successfully deleted, False if the file was not found.
    """
    _, _, path, _, _ = audio_file
    song_name =audio_file[4]
    feature_cache_path = os.path.join(cache_dir, f"{song_name}_features.pkl")

    if os.path.exists(feature_cache_path):
        os.remove(feature_cache_path)
        print(f"Cached features for {song_name} have been deleted")
        return True
    else:
        print(f"No cached features found for {song_name}")
        return False
    
# --------------------------------------------------------------
# Function: process_all
# --------------------------------------------------------------
# Processes all spectrograms and related features for an audio file. Uses caching for efficiency.
# The function calls individual processing methods based on configuration.
#
# Parameters:
# - audio_file (str): Path to the audio file.
# - json_path (str): Path to the JSON file for processing status.
# - save_path (str): Directory for saving the processed output files.
# - cache_dir (str): Directory for storing and retrieving cached features.
# - config (dict): Configuration specifying which processing functions to run or skip.
#
# Example usage:
# process_all(audio_file, '/path/to/json', '/path/to/save')
# --------------------------------------------------------------
def process_all(audio_file, json_path, save_path, cache_dir="feature_cache", config=None):
    """
    Unified function to process all the spectrograms and related features for an audio file.
    Uses caching to save and retrieve extracted features.
    
    Parameters:
    audio_file (str): Path to the audio file.
    json_path (str): Path to save the JSON output.
    save_path (str): Path to save the processed files.
    cache_dir (str): Directory to store and retrieve cached features.
    config (dict): A dictionary specifying which functions to skip. 
                   The key is the function name as a string, and the value is a boolean.
                   If True, the function will be skipped.
    """
    
    # Default configuration if none is provided
    if config is None:
        config = {
            "process_stft_and_save": True,
            "process_SSM_and_chr_and_save": True,
            "process_mel_spectrogram_and_save": True,
            "process_harmonic_cqt_and_percussive_sfft_and_save": True,
            "process_harmonic_cqt_and_harmonic_mel_and_save": True
        }
    
    # Extract features
    features = extract_audio_features(audio_file, cache_dir)
    
    # Process and save spectrograms and related features based on config
    if  config.get("process_stft_and_save", False):
        process_stft_and_save(features, json_path, save_path)
    
    if  config.get("process_SSM_and_chr_and_save", False):
        process_SSM_and_chr_and_save(features, json_path, save_path)
    
    if  config.get("process_mel_spectrogram_and_save", False):
        process_mel_spectrogram_and_save(features, json_path, save_path)
    
    if  config.get("process_harmonic_cqt_and_percussive_sfft_and_save", False):
        process_harmonic_cqt_and_percussive_sfft_and_save(features, json_path, save_path)
    
    if  config.get("process_harmonic_cqt_and_harmonic_mel_and_save", False):
        process_harmonic_cqt_and_harmonic_mel_and_save(features, json_path, save_path)



'''

def process_all(audio_file, json_path, save_path, cache_dir="feature_cache"):
    """
    Unified function to process all the spectrograms and related features for an audio file.
    Uses caching to save and retrieve extracted features.
    """
    features = extract_audio_features(audio_file, cache_dir)
    process_stft_and_save(features, json_path, save_path, jignore = False ) #YES!
    process_SSM_and_chr_and_save(features, json_path, save_path, jignore = False) #YES!
    process_mel_spectrogram_and_save(features, json_path, save_path, jignore = False) #YES!
    process_harmonic_cqt_and_percussive_sfft_and_save(features, json_path, save_path, jignore = False) #YES!
    process_harmonic_cqt_and_harmonic_mel_and_save(features, json_path, save_path, jignore = False) #NO!
   
''' 


'''
@log_elapsed_time(lambda *args, **kwargs: f"Self-Similarity Matrix and Chromagram - {Path(args[0][2]).name}")
def process_SSM_and_chr_and_save(features, json_path, save_path, plot_width=12, plot_height=12, jignore=False):
    """
    Processes the self-similarity matrix (SSM) and Chromagram of the given audio file, applies diagonal enhancement, and saves the plots.
    Updates the processing status in the JSON file.
    
    Parameters:
    - audio_file: tuple containing (y, sr, path, duration)
    - json_path: str, path to the JSON tracking file
    - save_path: str, directory where plots will be saved
    - plot_width: int, width of the plot
    - plot_height: int, height of the plot
    - jignore: bool, whether to ignore updating the JSON file
    """
    
    def get_ssm(C):
        CNorm = np.sqrt(np.sum(C**2, axis=0))
        C = C / CNorm[None, :]
        return np.dot(C.T, C)

    def chunk_average(C, f):
        C2 = np.zeros((C.shape[0], C.shape[1] // f))
        for j in range(C2.shape[1]):
            C2[:, j] = np.mean(C[:, j * f:(j + 1) * f], axis=1)
        return C2

    def diagonally_enhance(D, K):
        M = D.shape[0] - K + 1
        S = np.zeros((M, M))
        for i in range(M):
            for j in range(M):
                avg = 0
                for k in range(K):
                    avg += D[i + k, j + k]
                S[i, j] = avg / K
        return S

    # Load the tracking JSON file
    if os.path.exists(json_path) and not jignore:
        with open(json_path, 'r') as f:
            tracking_data = json.load(f)
    else:
        tracking_data = {}

    # Initialize variables
    y = features['y']
    sr = features['sr']
    audio_path = features['path']


    # Set parameters for CQT and Chromagram
    hop_length = math.ceil(sr / 5)  # Adjust hop_length for time resolution
    compression_ratio = 0.4  # Compression ratio for dynamic range compression
    
    # Get the name of the song from the audio path
    song_name = os.path.splitext(os.path.basename(audio_path))[0]

    # Check if this step has already been processed
    if tracking_data.get(song_name, {}).get("SSM_processed", False):
        print(f"Self-Similarity Matrix already processed for {song_name}. Skipping...")
        return

    #---COMPUTING CHROMA---#


    # Compute Chromagram directly from the harmonic component of the audio
    chroma = features['chroma'] 
    # Perform global normalization on the chromagram
    chroma_max = chroma.max()
    if (chroma_max > 0):
        chroma /= chroma_max

    # Apply dynamic range compression
    chroma = chroma ** compression_ratio

    #---COMPUTING SSM---#

    # Compute Mel spectrogram
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_to_db = librosa.power_to_db(mel, ref=np.max)

    # Compute Self-Similarity Matrix
    D = get_ssm(chunk_average(mel_to_db, 43))

    # Diagonally enhance the matrix
    DDiag = diagonally_enhance(D, 4)

    # Plotting SSM and Chromagram
    plt.figure(figsize=(plot_width, plot_height))

    # Plot Self-Similarity Matrix
    plt.subplot(2, 1, 1)
    ax = plt.gca()
    im = ax.imshow(DDiag, cmap='magma')
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    plt.title(f'Self-Similarity Matrix: {song_name}')
    plt.colorbar(im, ax=ax)

    # Convert frames to seconds for x and y axis labels
    hop = 512
    frames_per_second = sr / hop
    num_frames = DDiag.shape[0]
    integer_ticks = np.arange(0, int(num_frames // frames_per_second) + 1)
    ax.set_xticks(integer_ticks * frames_per_second)
    ax.set_xticklabels(integer_ticks)
    ax.set_yticks(integer_ticks * frames_per_second)
    ax.set_yticklabels(integer_ticks)

    # Plotting Chromagram
    plt.subplot(2, 1, 2)
    librosa.display.specshow(chroma, sr=sr, hop_length=hop_length, x_axis='time', y_axis='chroma')
    plt.title(f'Chromagram for {song_name}')
    plt.colorbar()
    plt.tight_layout()

    plot_path = os.path.join(save_path, f"SSM_Chromagram_{song_name}.png")
    plt.savefig(plot_path)
    plt.close()

    # Update the JSON tracking
    if song_name not in tracking_data:
        tracking_data[song_name] = {}
    tracking_data[song_name]["SSM_processed"] = True
    if not jignore:
        with open(json_path, 'w') as f:
            json.dump(tracking_data, f, indent=4)

    print(f"Self-Similarity Matrix and Chromagram processing complete for {song_name}.\n Saved to {plot_path}.")
'''


'''
# @log_elapsed_time(lambda *args, **kwargs: f"Chromagram and CQT Spectrogram - {Path(args[0]['path']).name}")
# def process_chromagram_and_save(features, json_path, save_path, plot_width=50, plot_height=20, jignore=False):
#     """
#     Processes the Chromagram and CQT spectrogram of the given audio file and saves the plots.
#     Updates the processing status in the JSON file.
#     """
#     y_harmonic = features['y_harmonic']
#     sr = features['sr']
#     audio_path = features['path']
#     CQT = features['CQT']
#     chroma = features['chroma']
#     song_name = os.path.splitext(os.path.basename(audio_path))[0]

#     if os.path.exists(json_path) and not jignore:
#         with open(json_path, 'r') as f:
#             tracking_data = json.load(f)
#     else:
#         tracking_data = {}

#     if tracking_data.get(song_name, {}).get("Chromagram_CQT_processed", False):
#         print(f"Chromagram and CQT Spectrogram already processed for {song_name}. Skipping...")
#         return

#     song_dir = os.path.join(os.path.dirname(save_path), song_name)
#     os.makedirs(song_dir, exist_ok=True)

#     plt.figure(figsize=(plot_width, plot_height))
#     plt.subplot(2, 1, 1)
#     librosa.display.specshow(librosa.amplitude_to_db(np.abs(CQT), ref=np.max), sr=sr, x_axis='time', y_axis='cqt_note')
#     plt.title(f'High-Resolution CQT Spectrogram for {song_name}')
#     plt.colorbar(format='%+2.0f dB')
#     plt.tight_layout()

#     output_file = os.path.join(song_dir, f"Chromagram_CQT_{song_name}.png")
#     plt.savefig(output_file)
#     plt.close()

#     tracking_data.setdefault(song_name, {})["Chromagram_CQT_processed"] = True
#     if not jignore:
#         with open(json_path, 'w') as f:
#             json.dump(tracking_data, f, indent=4)

#     print(f"Chromagram and CQT Spectrogram processing complete for {song_name}.\n Saved to {output_file}.")
'''


'''
@log_elapsed_time(lambda *args, **kwargs: f"Self-Similarity Matrix and Chromagram - {Path(args[0]['path']).name}")
def process_SSM_and_chr_and_save(features, json_path, save_path, plot_width=30, plot_height=30, jignore=False):
    """
    Processes the self-similarity matrix (SSM) and Chromagram of the given audio file, applies diagonal enhancement, and saves the plots.
    Updates the processing status in the JSON file.
    """
    def get_ssm(C):
        CNorm = np.sqrt(np.sum(C**2, axis=0))
        C = C / CNorm[None, :]
        return np.dot(C.T, C)

    def chunk_average(C, f):
        C2 = np.zeros((C.shape[0], C.shape[1] // f))
        for j in range(C2.shape[1]):
            C2[:, j] = np.mean(C[:, j * f:(j + 1) * f], axis=1)
        return C2

    def diagonally_enhance(D, K):
        M = D.shape[0] - K + 1
        S = np.zeros((M, M))
        for i in range(M):
            for j in range(M):
                avg = 0
                for k in range(K):
                    avg += D[i + k, j + k]
                S[i, j] = avg / K
        return S

    y = features['y']
    sr = features['sr']
    chroma = features['chroma']
    audio_path = features['path']
    mel_to_db = ['mel_to_db']
    song_name = os.path.splitext(os.path.basename(audio_path))[0]

    if os.path.exists(json_path) and not jignore:
        with open(json_path, 'r') as f:
            tracking_data = json.load(f)
    else:
        tracking_data = {}

    if tracking_data.get(song_name, {}).get("SSM_processed", False):
        print(f"Self-Similarity Matrix already processed for {song_name}. Skipping...")
        return

    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_to_db = librosa.power_to_db(mel, ref=np.max)

    D = get_ssm(chunk_average(mel_to_db, 43))
    DDiag = diagonally_enhance(D, 4)

    plt.figure(figsize=(plot_width, plot_height))
    plt.subplot(2, 1, 1)
    ax = plt.gca()
    im = ax.imshow(DDiag, cmap='magma')
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    plt.title(f'Self-Similarity Matrix: {song_name}')
    plt.colorbar(im, ax=ax)

    plt.subplot(2, 1, 2)
    librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma')
    plt.title(f'Chromagram for {song_name}')
    plt.colorbar()
    plt.tight_layout()

    plot_path = os.path.join(save_path, f"SSM_Chromagram_{song_name}.png")
    plt.savefig(plot_path)
    plt.close()

    tracking_data.setdefault(song_name, {})["SSM_processed"] = True
    if not jignore:
        with open(json_path, 'w') as f:
            json.dump(tracking_data, f, indent=4)

    print(f"Self-Similarity Matrix and Chromagram processing complete for {song_name}.\n Saved to {plot_path}.")

@log_elapsed_time(lambda *args, **kwargs: f"Self-Similarity Matrix and Chromagram - {Path(args[0]['path']).name}")
def process_SSM_and_chr_and_save(features, json_path, save_path, plot_width=12, plot_height=12, jignore=False):
    """
    Processes the self-similarity matrix (SSM) and Chromagram of the given audio file, applies diagonal enhancement, and saves the plots.
    Updates the processing status in the JSON file.
    
    Parameters:
    - audio_file: tuple containing (y, sr, path, duration)
    - json_path: str, path to the JSON tracking file
    - save_path: str, directory where plots will be saved
    - plot_width: int, width of the plot
    - plot_height: int, height of the plot
    - jignore: bool, whether to ignore updating the JSON file
    """
    
    def get_ssm(C):
        CNorm = np.sqrt(np.sum(C**2, axis=0))
        C = C / CNorm[None, :]
        return np.dot(C.T, C)

    def chunk_average(C, f):
        C2 = np.zeros((C.shape[0], C.shape[1] // f))
        for j in range(C2.shape[1]):
            C2[:, j] = np.mean(C[:, j * f:(j + 1) * f], axis=1)
        return C2

    def diagonally_enhance(D, K):
        M = D.shape[0] - K + 1
        S = np.zeros((M, M))
        for i in range(M):
            for j in range(M):
                avg = 0
                for k in range(K):
                    avg += D[i + k, j + k]
                S[i, j] = avg / K
        return S

    # Load the tracking JSON file
    if os.path.exists(json_path) and not jignore:
        with open(json_path, 'r') as f:
            tracking_data = json.load(f)
    else:
        tracking_data = {}

    # Initialize variables
    y = features['y']
    sr = features['sr']
    audio_path = features['path']


    # Set parameters for CQT and Chromagram
    hop_length = math.ceil(sr / 5)  # Adjust hop_length for time resolution
    compression_ratio = 0.4  # Compression ratio for dynamic range compression
    
    # Get the name of the song from the audio path
    song_name = os.path.splitext(os.path.basename(audio_path))[0]

    # Check if this step has already been processed
    if tracking_data.get(song_name, {}).get("SSM_processed", False):
        print(f"Self-Similarity Matrix already processed for {song_name}. Skipping...")
        return

    #---COMPUTING CHROMA---#


    # Compute Chromagram directly from the harmonic component of the audio
    chroma = features['chroma'] 
    # Perform global normalization on the chromagram
    chroma_max = chroma.max()
    if (chroma_max > 0):
        chroma /= chroma_max

    # Apply dynamic range compression
    chroma = chroma ** compression_ratio

    #---COMPUTING SSM---#

    # Compute Mel spectrogram
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_to_db = librosa.power_to_db(mel, ref=np.max)

    # Compute Self-Similarity Matrix
    D = get_ssm(chunk_average(mel_to_db, 43))

    # Diagonally enhance the matrix
    DDiag = diagonally_enhance(D, 4)

    # Plotting SSM and Chromagram
    plt.figure(figsize=(plot_width, plot_height))

    # Plot Self-Similarity Matrix
    plt.subplot(2, 1, 1)
    ax = plt.gca()
    im = ax.imshow(DDiag, cmap='magma')

    # Set the aspect ratio to stretch the plot horizontally
    chroma_width = chroma.shape[1] * hop_length / sr
    num_frames = DDiag.shape[0]
    aspect_ratio = chroma_width / num_frames
    ax.set_aspect(aspect_ratio)
    
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    plt.title(f'Self-Similarity Matrix: {song_name}')
    plt.colorbar(im, ax=ax)

    # Convert frames to seconds for x and y axis labels
    hop = 512
    frames_per_second = sr / hop
    integer_ticks = np.arange(0, int(num_frames // frames_per_second) + 1)
    ax.set_xticks(integer_ticks * frames_per_second)
    ax.set_xticklabels(integer_ticks)
    ax.set_yticks(integer_ticks * frames_per_second)
    ax.set_yticklabels(integer_ticks)

    # Plotting Chromagram
    plt.subplot(2, 1, 2)
    librosa.display.specshow(chroma, sr=sr, hop_length=hop_length, x_axis='time', y_axis='chroma')
    plt.title(f'Chromagram for {song_name}')
    plt.colorbar()
    plt.tight_layout()

    plot_path = os.path.join(save_path, f"SSM_Chromagram_{song_name}.png")
    plt.savefig(plot_path)
    plt.close()

    # Update the JSON tracking
    if song_name not in tracking_data:
        tracking_data[song_name] = {}
    tracking_data[song_name]["SSM_processed"] = True
    if not jignore:
        with open(json_path, 'w') as f:
            json.dump(tracking_data, f, indent=4)

    print(f"Self-Similarity Matrix and Chromagram processing complete for {song_name}.\n Saved to {plot_path}.")

@log_elapsed_time(lambda *args, **kwargs: f"Self-Similarity Matrix and Chromagram - {Path(args[0]['path']).name}")
def process_SSM_and_chr_and_save(features, json_path, save_path, plot_width=12, plot_height=12, jignore=False):
    """
    Processes the self-similarity matrix (SSM) and Chromagram of the given audio file, applies diagonal enhancement, and saves the plots.
    Updates the processing status in the JSON file.
    
    Parameters:
    - audio_file: tuple containing (y, sr, path, duration)
    - json_path: str, path to the JSON tracking file
    - save_path: str, directory where plots will be saved
    - plot_width: int, width of the plot
    - plot_height: int, height of the plot
    - jignore: bool, whether to ignore updating the JSON file
    """
    
    def get_ssm(C):
        CNorm = np.sqrt(np.sum(C**2, axis=0))
        C = C / CNorm[None, :]
        return np.dot(C.T, C)

    def chunk_average(C, f):
        C2 = np.zeros((C.shape[0], C.shape[1] // f))
        for j in range(C2.shape[1]):
            C2[:, j] = np.mean(C[:, j * f:(j + 1) * f], axis=1)
        return C2

    def diagonally_enhance(D, K):
        M = D.shape[0] - K + 1
        S = np.zeros((M, M))
        for i in range(M):
            for j in range(M):
                avg = 0
                for k in range(K):
                    avg += D[i + k, j + k]
                S[i, j] = avg / K
        return S

    # Load the tracking JSON file
    if os.path.exists(json_path) and not jignore:
        with open(json_path, 'r') as f:
            tracking_data = json.load(f)
    else:
        tracking_data = {}

    # Initialize variables
    y = features['y']
    sr = features['sr']
    audio_path = features['path']

    # Set parameters for CQT and Chromagram
    hop_length = math.ceil(sr / 5)  # Adjust hop_length for time resolution
    compression_ratio = 0.4  # Compression ratio for dynamic range compression
    
    # Get the name of the song from the audio path
    song_name = os.path.splitext(os.path.basename(audio_path))[0]

    # Check if this step has already been processed
    if tracking_data.get(song_name, {}).get("SSM_processed", False):
        print(f"Self-Similarity Matrix already processed for {song_name}. Skipping...")
        return

    #---COMPUTING CHROMA---#

    # Compute Chromagram directly from the harmonic component of the audio
    chroma = features['chroma'] 
    # Perform global normalization on the chromagram
    chroma_max = chroma.max()
    if (chroma_max > 0):
        chroma /= chroma_max

    # Apply dynamic range compression
    chroma = chroma ** compression_ratio

    #---COMPUTING SSM---#

    # Compute Mel spectrogram
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_to_db = librosa.power_to_db(mel, ref=np.max)

    # Compute Self-Similarity Matrix
    D = get_ssm(chunk_average(mel_to_db, 43))

    # Diagonally enhance the matrix
    DDiag = diagonally_enhance(D, 4)

    # Plotting SSM and Chromagram
    # Adjust the height to maintain the square aspect ratio for the SSM
    num_frames = DDiag.shape[0]
    chroma_width_seconds = chroma.shape[1] * hop_length / sr
    aspect_ratio = chroma_width_seconds / num_frames

    adjusted_height = plot_width * aspect_ratio  # Adjust the height to maintain the square aspect ratio

    plt.figure(figsize=(plot_width, adjusted_height + plot_height))  # Combine adjusted height with Chromagram plot height

    # Plot Self-Similarity Matrix
    plt.subplot(2, 1, 1)
    ax = plt.gca()
    im = ax.imshow(DDiag, cmap='magma')
    ax.set_aspect('equal')  # Force the aspect ratio to be 1:1 to make the plot square
    ax.xaxis.set_ticks_position('top')
    ax.xaxis.set_label_position('top')
    plt.title(f'Self-Similarity Matrix: {song_name}')
    plt.colorbar(im, ax=ax)

    # Convert frames to seconds for x and y axis labels
    hop = 512
    frames_per_second = sr / hop
    integer_ticks = np.arange(0, int(num_frames // frames_per_second) + 1)
    ax.set_xticks(integer_ticks * frames_per_second)
    ax.set_xticklabels(integer_ticks)
    ax.set_yticks(integer_ticks * frames_per_second)
    ax.set_yticklabels(integer_ticks)

    # Plotting Chromagram
    plt.subplot(2, 1, 2)
    librosa.display.specshow(chroma, sr=sr, hop_length=hop_length, x_axis='time', y_axis='chroma')
    plt.title(f'Chromagram for {song_name}')
    plt.colorbar()
    plt.tight_layout()

    plot_path = os.path.join(save_path, f"SSM_Chromagram_{song_name}.png")
    plt.savefig(plot_path)
    plt.close()

    # Update the JSON tracking
    if song_name not in tracking_data:
        tracking_data[song_name] = {}
    tracking_data[song_name]["SSM_processed"] = True
    if not jignore:
        with open(json_path, 'w') as f:
            json.dump(tracking_data, f, indent=4)

    print(f"Self-Similarity Matrix and Chromagram processing complete for {song_name}.\n Saved to {plot_path}.")
'''


'''
def extract_audio_features(audio_file, cache_dir="feature_cache"):
    """
    Extract common features from the audio file to be reused across multiple functions.
    Features are cached to disk to avoid recomputation.
    """
    y, sr, path, duration = audio_file
    song_name = os.path.splitext(os.path.basename(path))[0]
    feature_cache_path = os.path.join(cache_dir, f"{song_name}_features.pkl")

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

    # Check if features are already cached
    if os.path.exists(feature_cache_path):
        print(f"\n\nLoading cached features for {song_name} from {feature_cache_path}\n\n")
        with open(feature_cache_path, 'rb') as f:
            features = pickle.load(f)
        return features

    # Compute features (perform only once)

    # Set the STFT parameters
    STFT_n_fft = 22000 * 10
    STFT_hop_length = math.ceil(sr / 5)


    # Parameters for Mel spectrogram
    mel_n_fft = 2048 * 10
    mel_hop_length = 44100 // 100
    n_mels = 256 * 10

    # Set parameters for Chromagram
    chr_hop_length = math.ceil(sr / 5)  # Adjust hop_length for time resolution

    # Set parameters for CQT
    cqt_hop_length = math.ceil(sr / 5)  # Adjust hop_length for time
    cqt_bins_per_octave = 36  # Increase bins per octave for higher frequency resolution in CQT
    cqt_n_bins = 7 * cqt_bins_per_octave  # Total number of bins (7 octaves as an example)
    
    
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    S = librosa.stft(y, n_fft = STFT_n_fft, hop_length = STFT_hop_length)
    D = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, hop_length=chr_hop_length, norm=None)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_fft = mel_n_fft, hop_length= mel_hop_length, n_mels = n_mels)
    mel_to_db = librosa.power_to_db(mel, ref=np.max)
    CQT = librosa.cqt(y=y_harmonic, sr=sr, hop_length=cqt_hop_length, bins_per_octave=cqt_bins_per_octave, n_bins=cqt_n_bins)

    features = {
        'y': y,
        'sr': sr,
        'path': path,
        'y_harmonic': y_harmonic,
        'y_percussive': y_percussive,
        'S': S,
        'D': D,
        'chroma': chroma,
        'mel_to_db': mel_to_db,
        'CQT': CQT,
    }

    # Cache features to disk
    with open(feature_cache_path, 'wb') as f:
        pickle.dump(features, f)
    print(f"Features for {song_name} cached to {feature_cache_path}")

    return features
'''


'''
def log_elapsed_time(process_name_getter):

    """
    A decorator to log the elapsed time of a process.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            process_name = process_name_getter(*args, **kwargs)
            start_time = time.time()
            logging.info(f"***Starting process: {process_name}")
            
            # Execute the function
            result = func(*args, **kwargs)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"***Finished process: {process_name}")
            logging.info(f"***Elapsed time for {process_name}: {elapsed_time:.2f} seconds\n")
            
            return result
        return wrapper
    return decorator
'''


'''
def initialize_environment(working_directory, audio_files_dir, json_file_path, sr=44100, debug=0, playback=0, file_names='', load_all_tracks=False):
    """
    Initializes the working environment by setting paths, loading audio files,
    and printing relevant information.
    """
    os.chdir(working_directory)
    print("Current Working Directory:", os.getcwd())

    audio_files_paths = []
    loaded_audio_files = []

    if not os.path.exists(audio_files_dir):
        print(f"Directory {audio_files_dir} does not exist.")
        return []
    else:
        if debug == 1:
            all_files = os.listdir(audio_files_dir)
            print("Files in the directory:")
            for file in all_files:
                print(file, '\n')

    if load_all_tracks:
        print("Loading all audio files in the directory...")
        for file in os.listdir(audio_files_dir):
            if file.endswith((".flac", ".wav", ".mp3", ".aiff")):
                audio_files_paths.append(os.path.join(audio_files_dir, file))
                print(f"Found file: {file}")
    else:
        not_found = 0
        print("Starting file search...")
    
        if file_names == '':
            file_names = [
                "chroma_test",
                "Music For Airports - Brian Eno",
                "Orphans - AFX",
                "Olson - Boards of Canada",
                "Don't Leave Me This Way - Harold Melvin & The Blue Notes",
                "Don't Stop Till You Get Enough - Michael Jackson",
                "Plantas Falsas - Bruxas",
                "Empire Ants - Gorillaz",
                "That's Us/Wild Combination - Arthur Russell",
                "This Is How We Walk on the Moon - Arthur Russell",
                "Gipsy Woman (She's Homeless) - Crystal Waters",
                "Warszava - David Bowie",
                "I Feel Love - 12\"Version - Donna Summer",
                "Workinonit - J Dilla",
                "I Swear, I Really Wanted to Make a 'Rap' Album but This Is Literally the Way the Wind Blew Me This Time - Andre 3000",
                "oo Licky - Matthew Herbert",
                "King Tubby Meets The Rockers Uptown - King Tubby",
                "Mood Swings - Little Simz"
            ]

        for file_name in file_names:
            file_paths = {
                "flac": os.path.join(audio_files_dir, f"{file_name}.flac"),
                "wav": os.path.join(audio_files_dir, f"{file_name}.wav"),
                "mp3": os.path.join(audio_files_dir, f"{file_name}.mp3"),
                "aiff": os.path.join(audio_files_dir, f"{file_name}.aiff")
            }

            found_something = False
            for ext, path in file_paths.items():
                if os.path.exists(path):
                    audio_files_paths.append(path)
                    print(f"{file_name}.{ext} found at {path}!\n")
                    found_something = True
                    break

            if not found_something:
                not_found += 1
                print(f"{file_name} wasn't found in any supported format.\n")

        if not_found == 0:
            print("All Tracks Found \n\n(: \n")
        else:
            print(f"{not_found} tracks were not found!\n\n): \n")

    print("Starting to load audio files...")
    print("================================\n")
   
    ensure_json_file_exists(json_file_path)

    for path in audio_files_paths:
        try:
            y, sr = librosa.load(path, sr=sr)
            duration = librosa.get_duration(y=y, sr=sr)
            loaded_audio_files.append((y, sr, path, duration))
            print(f"Audio file correctly loaded from {path}: y = {y.shape} \n sr = {sr} \n duration = {duration} seconds \n\n")
        except Exception as e:
            print(f"Failed to load audio file from {path}: {e}")

    print("================================")
    print("Audio file loading complete.\n")

    loaded_audio_files.sort(key=lambda x: x[3])

    print("Tracks sorted by duration (shortest to longest):")
    for i, (y, sr, path, duration) in enumerate(loaded_audio_files, 1):
        print(f"{i}. {os.path.basename(path)} - {duration:.2f} seconds")
    print("================================\n")

    if playback == 1 and loaded_audio_files:
        for _, _, path, _ in loaded_audio_files:
            print(f"Listen to {path}")

    return loaded_audio_files

'''


