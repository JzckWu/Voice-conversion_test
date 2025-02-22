import os
import csv
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def generate_silence(silence_path, duration=1):
    subprocess.run(
        ["ffmpeg", "-f", "lavfi", "-i", f"anullsrc=channel_layout=mono:sample_rate=16000", 
         "-t", str(duration), silence_path, "-y"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def concatenate_with_gaps(wav_files, output_path, silence_path):
    # Create a list file for FFmpeg
    list_file = "wav_list.txt"
    with open(list_file, "w") as f:
        for wav in wav_files:
            f.write(f"file '{wav}'\n")
            f.write(f"file '{silence_path}'\n")  # Add silence between files

    # Concatenate using FFmpeg
    subprocess.run(
        ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", output_path, "-y"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    os.remove(list_file)

def scrape_voice_lines(character_url, output_dir, character_name):
    response = requests.get(character_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    os.makedirs(f"{output_dir}/wavs", exist_ok=True)
    metadata = []
    wav_files = []

    voice_entries = soup.select("table.wikitable tr")
    print(f"Found {len(voice_entries)} voice lines. Starting download...")

    for i, row in enumerate(voice_entries, start=1):
        audio_elem = row.select_one("audio[src]")
        text_elem = row.find_previous("th")

        if not audio_elem or not text_elem:
            continue  

        text = text_elem.text.strip()
        audio_url = urljoin(character_url, audio_elem["src"])  
        audio_filename = f"{character_name}{i:04d}.ogg"
        audio_path = os.path.join(output_dir, "wavs", audio_filename)

        with requests.get(audio_url, stream=True) as r:
            with open(audio_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

        wav_filename = audio_filename.replace(".ogg", ".wav")
        wav_path = os.path.join(output_dir, "wavs", wav_filename)
        subprocess.run(["ffmpeg", "-i", audio_path, "-ar", "16000", wav_path, "-y"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(audio_path)  

        metadata.append([wav_filename, text, text])
        wav_files.append(wav_path)
        print(f"Processed {i}/{len(voice_entries)}: {wav_filename}") 

    metadata_file = os.path.join(output_dir, "metadata.csv")
    with open(metadata_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerows(metadata)

    print(f"Metadata saved at {metadata_file}")

    # Generate silence file
    silence_path = os.path.join(output_dir, "wavs", "silence.wav")
    generate_silence(silence_path)

    # Concatenate WAVs with silence
    combined_output = os.path.join(output_dir, f"{character_name}_combined.wav")
    concatenate_with_gaps(wav_files, combined_output, silence_path)

    print(f"Combined audio saved at {combined_output}")

# Parameters
character_name = "MARCH_7TH"
character_url = "https://honkai-star-rail.fandom.com/wiki/March_7th/Voice-Overs"
output_dir = f"XTTS/notebooks/tts_train_dir/{character_name}"

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
