import os
import json

# --------------------------------------------------------------
# Function: select_folder_option
# --------------------------------------------------------------
# Prompts the user to select from multiple folder options.
#
# Parameters:
# - folder_options (list): A list of folder path options to choose from.
# - description (str): A description to display for the type of folder.
#
# Returns:
# - str: The selected folder path.
#
# Example usage:
# selected_folder = select_folder_option(folder_options, "audio files root directory")
# --------------------------------------------------------------
def select_folder_option(folder_options, description):
    print(f"\n\nMultiple {description} options detected. Please choose one of the following:")
    for i, option in enumerate(folder_options):
        print(f"{i + 1}. {option}")

    selection = None
    while selection is None:
        try:
            choice = int(input(f"\n\nEnter the number for the {description} you want to use: ")) - 1
            if 0 <= choice < len(folder_options):
                selection = folder_options[choice]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return selection

# --------------------------------------------------------------
# Function: save_last_used_folders
# --------------------------------------------------------------
# Saves the selected folder options to a JSON file.
#
# Parameters:
# - config (dict): A dictionary of folder paths to be saved.
#
# Returns:
# None
#
# Example usage:
# save_last_used_folders(config)
# --------------------------------------------------------------
def save_last_used_folders(config):
    config_file_path = 'last_used_folders.json'
    with open(config_file_path, 'w') as f:
        json.dump(config, f)

# --------------------------------------------------------------
# Function: load_last_used_folders
# --------------------------------------------------------------
# Loads the last used folder options from a JSON file if it exists.
#
# Returns:
# - dict: The previously saved folder configuration, or None if not found.
#
# Example usage:
# last_used = load_last_used_folders()
# if last_used:
#     print("Loaded previous configuration")
# --------------------------------------------------------------
def load_last_used_folders():
    config_file_path = 'last_used_folders.json'
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as f:
            return json.load(f)
    return None

# --------------------------------------------------------------
# Function: ask_to_use_previous_config
# --------------------------------------------------------------
# Asks the user if they want to use the previously selected folder options.
#
# Returns:
# - bool: True if the user wants to use the previous configuration, False otherwise.
#
# Example usage:
# use_previous = ask_to_use_previous_config()
# --------------------------------------------------------------
def ask_to_use_previous_config():
    choice = input("\n\nDo you want to use the last selected folders? (y/n): ").strip().lower()
    return choice == 'y'

# --------------------------------------------------------------
# Function: get_user_folder_choices
# --------------------------------------------------------------
# Handles folder selection by the user and saves the choices.
#
# Parameters:
# - audio_files_root_dir_options (list): Options for the audio files root directory.
# - audio_files_location_options (list): Options for the audio files subdirectory.
# - graphs_root_dir_options (list): Options for the graphs root directory.
# - graphs_location_options (list): Options for the graphs subdirectory.
#
# Returns:
# - dict: A dictionary containing the selected folder paths.
#
# Example usage:
# config = get_user_folder_choices(audio_files_root_dir_options, audio_files_location_options, 
#                                  graphs_root_dir_options, graphs_location_options)
# --------------------------------------------------------------
def get_user_folder_choices(audio_files_root_dir_options, audio_files_location_options,
                            graphs_root_dir_options, graphs_location_options):
    audio_files_root_dir = select_folder_option(audio_files_root_dir_options, "audio files root directory")
    audio_files_location = select_folder_option(audio_files_location_options, "audio files location")
    graphs_root_dir = select_folder_option(graphs_root_dir_options, "graphs root directory")
    graphs_location = select_folder_option(graphs_location_options, "graphs location")

    config = {
        "audio_files_root_dir": audio_files_root_dir,
        "audio_files_location": audio_files_location,
        "graphs_root_dir": graphs_root_dir,
        "graphs_location": graphs_location
    }
    save_last_used_folders(config)

    return config

# --------------------------------------------------------------
# Function: configure_folders
# --------------------------------------------------------------
# Loads previous folder selections or prompts the user to select new ones.
#
# Parameters:
# - audio_files_root_dir_options (list): Options for the audio files root directory.
# - audio_files_location_options (list): Options for the audio files subdirectory.
# - graphs_root_dir_options (list): Options for the graphs root directory.
# - graphs_location_options (list): Options for the graphs subdirectory.
#
# Returns:
# - dict: A dictionary containing the folder paths.
#
# Example usage:
# config = configure_folders(audio_files_root_dir_options, audio_files_location_options, 
#                            graphs_root_dir_options, graphs_location_options)
# --------------------------------------------------------------
def configure_folders(audio_files_root_dir_options, audio_files_location_options,
                      graphs_root_dir_options, graphs_location_options):
    last_used_config = load_last_used_folders()

    if last_used_config and ask_to_use_previous_config():
        print("Using the last selected folders.")
        return last_used_config
    else:
        return get_user_folder_choices(audio_files_root_dir_options, audio_files_location_options,
                                       graphs_root_dir_options, graphs_location_options)
