import json
import os
import re
import datetime
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, COMM, TPE1, TALB, TXXX, CHAP, CTOC, TIT2

# --- Configuration ---
# The folder where your MP3 files are located. 
# Change to "." if files are in the same folder as this script.
MP3_DIRECTORY = "./mp3s" 

# --- ASCII ART HEADER ---
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

def parse_cue_timestamps(cue_path):
    """
    Parses a .cue file to extract 'INDEX 01' timestamps.
    Returns a list of strings formatted as 'MM:SS'.
    """
    timestamps = []
    if not os.path.exists(cue_path):
        return []
        
    try:
        with open(cue_path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                # Matches MM:SS:FF or MMM:SS:FF (for 100+ mins)
                match = re.search(r'INDEX 01 (\d+):(\d{2}):\d{2}', line)
                if match:
                    minutes, seconds = match.groups()
                    timestamps.append(f"{minutes}:{seconds}")
    except Exception as e:
        print(f"Warning: Failed to parse CUE file {cue_path}: {e}")
        return []
        
    return timestamps

def time_str_to_ms(time_str):
    """Converts 'MM:SS' string to milliseconds."""
    try:
        parts = time_str.split(':')
        minutes = int(parts[0])
        seconds = int(parts[1])
        return (minutes * 60 + seconds) * 1000
    except (ValueError, IndexError):
        return 0

def generate_comment_text(show_data, filename, timestamps=None):
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
        for i, track in enumerate(playlist):
            artist = track.get('artist', '').strip()
            song = track.get('track', '').strip()
            note = track.get('note', '').strip()
            
            # Timestamp logic for display
            time_str = ""
            if timestamps and i < len(timestamps):
                time_str = f"[{timestamps[i]}] "
            
            entry = f"{i+1}. {time_str}{artist}"
            if song:
                entry += f" - {song}"
            if note:
                entry += f" ({note})"
            
            lines.append(entry)
        
    return "\n".join(lines)

def write_nfo_file(mp3_path, content, log_file):
    try:
        nfo_path = os.path.splitext(mp3_path)[0] + ".nfo"
        header_clean = NFO_HEADER_ART.strip("\n")
        full_nfo_content = header_clean + "\n\n" + content
        
        with open(nfo_path, 'w', encoding='utf-8') as f:
            f.write(full_nfo_content)
        return True, nfo_path
    except Exception as e:
        log_action(log_file, f"   [Error] Could not write NFO file: {e}")
        return False, None

def add_id3_chapters(audio, playlist, timestamps, total_duration_seconds):
    """
    Adds ID3v2 Chapters (CHAP) and Table of Contents (CTOC) to the audio object.
    """
    if not timestamps or not playlist:
        return False, "No timestamps or playlist data for chapters"

    # Remove existing chapters to avoid duplicates
    audio.tags.delall("CHAP")
    audio.tags.delall("CTOC")

    chapter_ids = []
    total_duration_ms = int(total_duration_seconds * 1000)

    for i in range(len(timestamps)):
        # Calculate Start Time
        start_ms = time_str_to_ms(timestamps[i])
        
        # Calculate End Time
        if i + 1 < len(timestamps):
            end_ms = time_str_to_ms(timestamps[i+1])
        else:
            end_ms = total_duration_ms

        # Get Title info
        if i < len(playlist):
            track = playlist[i]
            artist = track.get('artist', '').strip()
            song = track.get('track', '').strip()
            
            if artist and song:
                chapter_title = f"{artist} - {song}"
            elif artist:
                chapter_title = artist
            elif song:
                chapter_title = song
            else:
                chapter_title = f"Track {i+1}"
        else:
            chapter_title = f"Track {i+1}"

        # Create unique Element ID
        element_id = f"chp{i}"
        chapter_ids.append(element_id)

        # Create CHAP Frame
        # The CHAP frame contains a start/end time and an embedded TIT2 (Title) frame
        audio.tags.add(
            CHAP(
                element_id=element_id,
                start_time=start_ms,
                end_time=end_ms,
                sub_frames=[
                    TIT2(encoding=3, text=chapter_title)
                ]
            )
        )

    # Add Table of Contents (CTOC)
    # Required for players to navigate the chapters
    audio.tags.add(
        CTOC(
            element_id="toc",
            flags=3, # Top-level + Ordered
            child_element_ids=chapter_ids,
            sub_frames=[
                TIT2(encoding=3, text="Chapters")
            ]
        )
    )
    
    return True, f"Added {len(chapter_ids)} chapters"


def write_id3_tag(file_path, comment_text, djs_list, show_id, playlist, timestamps, log_file):
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

        # --- ADD CHAPTERS ---
        chapter_msg = ""
        if timestamps:
            # MP3 object has .info.length containing duration in seconds
            total_duration = audio.info.length
            chap_success, chap_msg = add_id3_chapters(audio, playlist, timestamps, total_duration)
            chapter_msg = f" | {chap_msg}"

        # Force ID3v2.3 (Widest compatibility)
        audio.save(v2_version=3)
        
        return True, f"Success (Tags Written{chapter_msg})"

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
        
        # Sort files based on show ID integer
        def show_id_sort_key(fname):
            sid = extract_show_id_from_filename(fname)
            if sid and sid.isdigit():
                return int(sid)
            return float('inf')
            
        files.sort(key=show_id_sort_key)

        if not files:
             log_action(log_file, "No files found in directory.")

        for filename in files:
            if filename.lower().endswith(".mp3"):
                show_id = extract_show_id_from_filename(filename)
                
                if show_id:
                    if show_id in show_lookup:
                        matched_count += 1
                        show_data = show_lookup[show_id]
                        file_path = os.path.join(MP3_DIRECTORY, filename)
                        
                        log_action(log_file, f"--------------------------------------------------")
                        log_action(log_file, f"Processing: {filename}")
                        log_action(log_file, f"   > Match Found: Show ID {show_id}")

                        # Check for CUE file
                        base_name = os.path.splitext(filename)[0]
                        cue_path = os.path.join(MP3_DIRECTORY, base_name + ".cue")
                        timestamps = []
                        
                        if os.path.exists(cue_path):
                            log_action(log_file, f"   > CUE File found: {base_name}.cue")
                            timestamps = parse_cue_timestamps(cue_path)
                            if timestamps:
                                log_action(log_file, f"   > Merging {len(timestamps)} timestamps")
                            else:
                                log_action(log_file, f"   > CUE found but no timestamps parsed (Check format)")
                        else:
                            log_action(log_file, f"   > No CUE file found. Skipping timestamp merge.")
                        
                        # Generate comment
                        comment_text = generate_comment_text(show_data, filename, timestamps)
                        djs_list = show_data.get('meta_info', {}).get('djs', [])
                        playlist_data = show_data.get('playlistbox', [])

                        # Pass timestamps and playlist to write_id3_tag for Chapter creation
                        success, status_msg = write_id3_tag(
                            file_path, 
                            comment_text, 
                            djs_list, 
                            show_id, 
                            playlist_data, 
                            timestamps, 
                            log_file
                        )
                        
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