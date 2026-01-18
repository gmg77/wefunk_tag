import json
import os
import re
import datetime
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, COMM, TPE1, TALB, TXXX

# --- Configuration ---
# The folder where your MP3 files are located. 
# Change to "." if files are in the same folder as this script.
MP3_DIRECTORY = "./mp3s" 

# --- ASCII ART HEADER ---
# This string is intentionally NOT indented to preserve exact alignment.
# If you edit this, ensure the characters start at the very beginning of the line.
NFO_HEADER_ART = r"""
                                                                                                                                                                                                                                                            
                                                                      █                                                                                                                                                                                       
                                                                   ███████                                        ████                                                                                                                                        
                                                                  ██     ████                                   ███  ███                                                                                                                                      
                                                                   ██       ████                             ████       █                                                                                                                                     
                                                                    ██         ████                       ████        █ █                                                                                                                                     
                                                                    ██            █████               █████           ██                                                                                                                                      
                                                                      █               ██████     ██████              █ █  ███████                                                                                                                             
                                                      █████████████████                    ███████                   ██████     ██████                         GMGRIOT77                                                                                               
                                            ███████████                                        █                    █                 ███                                                                                                                     
                                      ███████                            ████               █  █                 ██                     ███                                                                                                                   
                                  █████                                    ███████          █ █               ████                        ███                                                                                                                 
                             ████     ████████████████████████████████         █████        █ █            ████ █                           █                                                                                                                 
                          ███   ██████                               ██████████    ██       █ █          ███   ██                          ██                                                                                                                 
                          █  ███                                               █████        ██         █ █     ██             ███████     ██                         ██████████████                                                                           
                            █                                              █████            ██         ███      ██            ███    ██  ███                 ██████████           ███████                                                                     
                                                                       █████               ██            ███     ███            █████ ████             ███████                           █                                                                    
                                                                    ████                ██████            ███      █████              █           ██████                               █ █                                                                    
                                                                █████                ████    ███            ███   ████          ██████       ██████                                    █ █                                                                    
                                                             ████                 ██████████  ███             █████          ████        █████                                          ███████████████                                                       
                                                         █████                 █████      ███   ███            ██           ██      ██████                                                           ████████████                                             
                                                       ███                    ██   █       ██     ██                         █████████                                 █████████████████                        ███████                                       
                                                      ██                       ██  █        ███    ██                                                            ███████        ████                                  █████                                   
                                   ██████████████      █████                     ███    █     █████ ██                                                    ███████          █████                                          ████                                
                               █████            █████      ███████                      ███       ███                                                 ████████   ███████ ███           ███████████████████████████████████   ███                              
                             ███                    ███        ███████                     ██                                                    █████████       █     ████     ████████         █████                   █████   █                            
                           ███                        ███   ████      ███                █  ███                                             █████  ████          █          ██████           ███     ████                     ██  █                           
                          ███                           █████          █ ██               █   ████                    █               ██████   ████             ██                ███      ████         ████                    ██                            
                          ██                             █  █             ████             ██    ██████             ███████████████████    ████                 █ █                ██    ███               ██                                                 
                         █ █                              ██          █   █   ███████      █ █        ████████████████                   ███                   █  █                 ██    ██              ███                                                 
                         █ █                ███████                  ██  █         █████████           ████           ██████████████     ██                    █  █                  ██   ██              ██                                                  
                          ███               █      ██               ███ ██                  █████ ██████                          ███   ██                  ████████                  ██   ██            ██                                                   
                           ██               ███     ██              ██  ███                    ████                  █             ███ ██                 ███      ███                 ██  ██           ██                                                    
                            ███              ███    ███            █     ██                     ██                   █              ██  █               ███          ██               ███  ██          ███                                                    
                             ███              ████   ██            ██    ██                      █                  █                █  █               ██            ██             ███  ███         ███                                                     
                               ███              ███  █             ██     ███████                                   ██                  █               ██            ██            ███   ██         ███                                                      
                                ███               ███   ██      ████            ██             ██               ████  █              █  █               ██            ██            ██   ██         ███                                                       
                                  ███               ██  █████████             ███            ███              ███     █              █  █               ██            ██           █ █ ███         ███                                                        
                                    ███               ██    █ █             ███            ██  █             ███   ███              ███ ██              ███           ██           █ ███         █                                                            
                                       ██                   ██            ███             ██                ███    ██               █    ██              ███          ██           ██         ███████                                                         
                                    ███                   ██ █          ███             ███  ██             ██    ██                █    ███              ███         ██                            ██████                                                    
                                   ██                      ███        ███             ███    ██             ██   ██                 ███   ██               ███       ███          █                      █████                                                
                                    ███████                  ███    ███              ███     ██            █ █  ███            ██    ██    ██                ██      ██           ███████████                █████                                            
                                         ██████                ██  ███              ██       ██            █ █ ███             ██     ██    ███               ███   ███           █         ████                 ████                                         
                                              ██                ████               ██        ██             █  ██              ██      ██    ██                ███  ██            ██           ███                  ███                                       
                                               ██                ██               ██         ██             █  █               ███      ████   █                 █████             ██            ███                  ████                                    
                                               █ █                               █ █       ████             █  █                 ██       █████ █                 ███              ██              ███                   ███                                  
                                                 █                               ███    ████                 ██                   █ █         ███                                  ███      ██████████                    ███                                 
                                               █ █                                 ██████                                         █  █                                              ██    ████                              ███                               
                                              █ █                                              █                                  █  ███                                             ███ ███                                  ██                              
                                              █ █                                           ██████                                ███  ████                                              █                                     ██                             
                                             ███    ██             █                     ████   █████████      █               ████       ████                                       █████                                      ██                            
                                            ██           █       ██████              █████              ████████████         ███             █████                ████             ███   ██████                                  ██                           
                                             ████████          ███    ████████████████                             ████    ███                   ███████       ████  ██████     ████         ███████████                       ███                            
                                                    █████████  █ █                                                    ██████                          ██████████          ████████                    ████████              ████                              
                                                            ████                                                                                                              █                              ███████      ████                                
                                                                                                                                                                                                                   ████████                                   
                                                                                                                                                                                                                                   
"""

def get_timestamp_filename():
    """Generates a unique filename using the current date and time."""
    now = datetime.datetime.now()
    return f"wefunk_tag_log_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

def log_action(file_handle, message):
    """Writes a message to both the console and the log file."""
    print(message)
    file_handle.write(message + "\n")

def load_show_data(json_file, log_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        log_action(log_file, f"Error: JSON file '{json_file}' not found.")
        return None
    except json.JSONDecodeError:
        log_action(log_file, f"Error: Failed to decode JSON from '{json_file}'.")
        return None

    lookup = {}
    for entry in data:
        show_id = str(entry['show_id'])
        lookup[show_id] = entry
    return lookup

def extract_show_id_from_filename(filename):
    match = re.search(r'Show_?(\d+)', filename, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def extract_date_from_filename(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return None

def generate_comment_text(show_data, filename):
    meta = show_data.get('meta_info', {})
    playlist = show_data.get('playlistbox', [])
    
    lines = []
    
    # Header Info
    lines.append(f"WEFUNK Radio Show {show_data['show_id']}")
    
    recorded_date = meta.get('recorded', 'Unknown')
    if recorded_date.lower() == 'unknown':
        filename_date = extract_date_from_filename(filename)
        if filename_date:
            recorded_date = filename_date
            
    lines.append(f"Recorded: {recorded_date}")
    
    djs = meta.get('djs', [])
    if djs:
        lines.append(f"DJs: {', '.join(djs)}")

    # Description
    desc = show_data.get('showdescription', '')
    if desc:
        lines.append(f"\nDescription:\n{desc}")
    
    # Extra Notes
    if 'extra_notes' in meta:
        lines.append(f"\nNotes:\n{meta['extra_notes']}")

    # Links
    if 'extra_notes_links' in meta and meta['extra_notes_links']:
        lines.append("\nLinks:")
        for link in meta['extra_notes_links']:
            lines.append(link)

    # Playlist
    if playlist:
        lines.append("\nPlaylist:")
        for i, track in enumerate(playlist, 1):
            artist = track.get('artist', '').strip()
            song = track.get('track', '').strip()
            note = track.get('note', '').strip()
            
            entry = f"{i}. {artist}"
            if song:
                entry += f" - {song}"
            if note:
                entry += f" ({note})"
            
            lines.append(entry)
        
    return "\n".join(lines)

def write_nfo_file(mp3_path, content, log_file):
    try:
        nfo_path = os.path.splitext(mp3_path)[0] + ".nfo"
        
        # Strip leading newline from header to avoid double spacing at top if raw string used one
        header_clean = NFO_HEADER_ART.strip("\n")
        full_nfo_content = header_clean + "\n\n" + content
        
        with open(nfo_path, 'w', encoding='utf-8') as f:
            f.write(full_nfo_content)
        return True, nfo_path
    except Exception as e:
        log_action(log_file, f"   [Error] Could not write NFO file: {e}")
        return False, None

def write_id3_tag(file_path, comment_text, djs_list, show_id, log_file):
    try:
        audio = MP3(file_path, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()

        # Update COMMENT (COMM)
        keys_to_delete = [k for k in audio.tags.keys() if k.startswith('COMM')]
        for k in keys_to_delete:
            del audio.tags[k]
        audio.tags.add(COMM(encoding=3, lang='eng', desc='', text=comment_text))
        
        # Update ARTIST (TPE1)
        artist_string = ""
        if djs_list:
            artist_string = ", ".join(djs_list)
            audio.tags.add(TPE1(encoding=3, text=artist_string))

        # Update ALBUM (TALB)
        album_string = f"WEFUNK Show {show_id}"
        audio.tags.add(TALB(encoding=3, text=album_string))

        # Update CUSTOM DESCRIPTION (TXXX:Description)
        if 'TIT3' in audio.tags:
            del audio.tags['TIT3']
        audio.tags.add(TXXX(encoding=3, desc='Description', text=comment_text))

        # Force ID3v2.3
        audio.save(v2_version=3)
        
        # --- VERIFICATION ---
        audio_verify = MP3(file_path, ID3=ID3)
        verified = True
        
        # Simple check: verify file updated
        if not audio_verify.tags:
            verified = False
            
        if verified:
            return True, "Success (Tags Written)"
        else:
            return False, "Verification failed"

    except Exception as e:
        return False, str(e)

def get_json_input():
    files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if not files:
        print("No .json files found in the current directory.")
        return input("Please enter the full path to your JSON file: ").strip()
    
    print("\nAvailable JSON files:")
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")
    
    while True:
        choice = input(f"\nEnter filename or number (1-{len(files)}): ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                return files[idx]
        if os.path.exists(choice):
            return choice
        print("Invalid selection. Please try again.")

def main():
    log_filename = get_timestamp_filename()
    
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        log_action(log_file, "--- WEFUNK ID3 Tagger + Fixed ASCII Log ---")
        log_action(log_file, f"Log started at: {datetime.datetime.now()}")
        
        json_source_file = get_json_input()
        log_action(log_file, f"\nSource JSON: {json_source_file}")
        
        show_lookup = load_show_data(json_source_file, log_file)
        if not show_lookup:
            return

        log_action(log_file, f"Scanning directory: {MP3_DIRECTORY}")
        if not os.path.exists(MP3_DIRECTORY):
            log_action(log_file, f"Error: Directory '{MP3_DIRECTORY}' does not exist.")
            return

        matched_count = 0
        tagged_count = 0
        nfo_count = 0
        skipped_count = 0

        files = os.listdir(MP3_DIRECTORY)
        if not files:
             log_action(log_file, "No files found in directory.")

        for filename in files:
            if filename.lower().endswith(".mp3"):
                show_id = extract_show_id_from_filename(filename)
                
                if show_id:
                    if show_id in show_lookup:
                        matched_count += 1
                        show_data = show_lookup[show_id]
                        
                        comment_text = generate_comment_text(show_data, filename)
                        djs_list = show_data.get('meta_info', {}).get('djs', [])
                        
                        file_path = os.path.join(MP3_DIRECTORY, filename)
                        
                        log_action(log_file, f"--------------------------------------------------")
                        log_action(log_file, f"Processing: {filename}")
                        log_action(log_file, f"   > Match Found: Show ID {show_id}")
                        
                        success, status_msg = write_id3_tag(file_path, comment_text, djs_list, show_id, log_file)
                        
                        if success:
                            tagged_count += 1
                            log_action(log_file, f"   > [ID3] {status_msg}")
                            
                            nfo_success, nfo_path = write_nfo_file(file_path, comment_text, log_file)
                            if nfo_success:
                                nfo_count += 1
                                log_action(log_file, f"   > [NFO] Created: {os.path.basename(nfo_path)}")
                            
                        else:
                            log_action(log_file, f"   > [ID3 FAILED] {status_msg}")
                            
                    else:
                        log_action(log_file, f"[Skip] Show {show_id} found in filename but NOT in JSON data.")
                        skipped_count += 1
                else:
                    pass

        log_action(log_file, "\n--- Summary ---")
        log_action(log_file, f"Files Matched in JSON: {matched_count}")
        log_action(log_file, f"Files Tagged (ID3):    {tagged_count}")
        log_action(log_file, f"NFO Files Created:     {nfo_count}")
        log_action(log_file, f"Files Skipped:         {skipped_count}")
        log_action(log_file, f"Log saved to: {log_filename}")

if __name__ == "__main__":
    main()