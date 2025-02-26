import os
import csv
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .audio_matching import convert_to_wav  # Import function from audio_matching.py


def generate_silence(silence_path, duration=1):
    """Generate a silence WAV file."""
    result = subprocess.run(
        ["ffmpeg", "-f", "lavfi", "-i", "anullsrc=channel_layout=mono:sample_rate=16000",
         "-t", str(duration), silence_path, "-y"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error generating silence: {result.stderr}")


def concatenate_with_gaps(wav_files, output_path, silence_path):
    """Concatenate WAV files with silence in between using absolute paths."""
    list_file = os.path.join(os.path.dirname(output_path), "wav_list.txt")

    with open(list_file, "w") as f:
        for wav in wav_files:
            # Write absolute paths to avoid relative path issues
            f.write(f"file '{os.path.abspath(wav)}'\n")
            f.write(f"file '{os.path.abspath(silence_path)}'\n")

    result = subprocess.run(
        ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", output_path, "-y"],
        capture_output=True, text=True
    )

    os.remove(list_file)  # Clean up

    if result.returncode != 0:
        print(f"❌ Error during concatenation:\n{result.stderr}")
    else:
        print(f"✅ Combined audio saved at {output_path}")



def ensure_data_dir(output_dir, character_name):
    """Ensure no double 'data' directories are created."""
    path_parts = os.path.normpath(output_dir).split(os.sep)
    return output_dir if "data" in path_parts else os.path.join("data", character_name)


def scrape_voice_lines(character_url, output_dir, character_name):
    """Scrape voice lines, convert them to WAV, and save metadata with a combined audio file."""
    output_dir = ensure_data_dir(output_dir, character_name)
    wav_dir = os.path.join(output_dir, "wavs")
    os.makedirs(wav_dir, exist_ok=True)

    response = requests.get(character_url)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    voice_entries = soup.select("table.wikitable tr")
    print(f"Found {len(voice_entries)} voice lines. Starting download...")

    metadata = []
    wav_files = []

    for i, row in enumerate(voice_entries, start=1):
        audio_elem = row.select_one("audio[src]")
        text_elem = row.find_previous("th")

        if not audio_elem or not text_elem:
            continue

        text = text_elem.text.strip()
        audio_url = urljoin(character_url, audio_elem["src"])
        audio_filename = f"{character_name}{i:04d}.ogg"
        audio_path = os.path.join(wav_dir, audio_filename)

        # Download audio
        try:
            with requests.get(audio_url, stream=True) as r:
                r.raise_for_status()
                with open(audio_path, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {audio_filename}: {e}")
            continue

        # Convert to WAV
        wav_filename = audio_filename.replace(".ogg", ".wav")
        wav_path = os.path.join(wav_dir, wav_filename)
        convert_to_wav(audio_path, wav_path)
        os.remove(audio_path)  # Remove the original OGG

        metadata.append([wav_filename, text, text])
        wav_files.append(wav_path)
        print(f"Processed {i}/{len(voice_entries)}: {wav_filename}")

    # Save metadata
    metadata_file = os.path.join(output_dir, "metadata.csv")
    with open(metadata_file, "w", newline="") as f:
        csv.writer(f, delimiter="|").writerows(metadata)
    print(f"Metadata saved at {metadata_file}")

    # Generate silence and concatenate
    silence_path = os.path.join(wav_dir, "silence.wav")
    generate_silence(silence_path)

    combined_output = os.path.join(output_dir, f"{character_name}_combined.wav")
    concatenate_with_gaps(wav_files, combined_output, silence_path)


# Parameters
character_name = "MARCH_7th"
character_url = "https://honkai-star-rail.fandom.com/wiki/March_7th/Voice-Overs"
output_dir = os.path.join("data", character_name)

scrape_voice_lines(character_url, output_dir, character_name)


# import os
# from TTS.api import TTS
# import subprocess

# # Function to download and convert YouTube video to WAV
# def download_audio(youtube_url, output_file="speaker.wav"):
#     print("Downloading audio...")
#     command = [
#         "yt-dlp",
#         "-x",  # Extract audio
#         "--audio-format", "wav",  # Convert to WAV
#         "-o", output_file,  # Save as specified file
#         youtube_url
#     ]
    
#     subprocess.run(command, check=True)
#     print(f"Audio downloaded and saved as {output_file}.")

# def main():

#     youtube_url = input("Enter YouTube video URL: ").strip()
#     output_file = "speaker.wav"
#     download_audio(youtube_url, output_file)

#     tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

#     text = input("Enter the text you want to convert to speech: ").strip()

#     tts.tts_to_file(
#         text=text,
#         speaker_wav=output_file,
#         language="en",
#         file_path="output.wav"
#     )
#     print("TTS conversion complete. Output saved as 'output.wav'.")
