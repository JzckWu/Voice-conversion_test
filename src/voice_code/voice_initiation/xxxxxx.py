# import os
# import csv
# import requests
# import subprocess
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import whisper  # Importing OpenAI's Whisper model

print(f"Error converting FAILFAILFAIL")
print(f"Error converting FAILFAILFAIL")
print(f"Error converting FAILFAILFAIL")
print(f"Error converting FAILFAILFAIL")

# def convert_to_wav(input_path, output_path):
#     """Convert audio file to WAV format using ffmpeg."""
#     command = [
#         "ffmpeg",
#         "-i", input_path,
#         "-ar", "16000",  # Set sample rate to 16000 Hz
#         "-ac", "1",      # Set number of audio channels to 1 (mono)
#         output_path,
#         "-y"             # Overwrite output file if it exists
#     ]
#     result = subprocess.run(command, capture_output=True, text=True)
#     if result.returncode != 0:
#         print(f"Error converting {input_path} to WAV: {result.stderr}")

# def transcribe_audio(wav_path, model):
#     """Transcribe the given WAV file using Whisper."""
#     result = model.transcribe(wav_path)
#     return result["text"].strip()

# def scrape_and_transcribe(character_url, output_dir, character_name):
#     """Scrape audio files, convert to WAV, transcribe, and save metadata."""
#     wav_dir = os.path.join(output_dir, "wavs")
#     os.makedirs(wav_dir, exist_ok=True)

#     # Load Whisper model
#     print("Loading transcription model...")
#     model = whisper.load_model("base")

#     response = requests.get(character_url)
#     if response.status_code != 200:
#         print(f"Failed to fetch page: {response.status_code}")
#         return

#     soup = BeautifulSoup(response.text, 'html.parser')
#     voice_entries = soup.select("table.wikitable tr")
#     print(f"Found {len(voice_entries)} voice lines. Starting download and transcription...")

#     metadata = []  # To store [filename, transcription]

#     for i, row in enumerate(voice_entries, start=1):
#         audio_elem = row.select_one("audio[src]")
#         if not audio_elem:
#             continue

#         audio_url = urljoin(character_url, audio_elem["src"])
#         audio_filename = f"{character_name}{i:04d}.ogg"
#         audio_path = os.path.join(wav_dir, audio_filename)

#         # Download audio
#         try:
#             with requests.get(audio_url, stream=True) as r:
#                 r.raise_for_status()
#                 with open(audio_path, "wb") as f:
#                     for chunk in r.iter_content(1024):
#                         f.write(chunk)
#         except requests.exceptions.RequestException as e:
#             print(f"Failed to download {audio_filename}: {e}")
#             continue

#         # Convert to WAV
#         wav_filename = audio_filename.replace(".ogg", ".wav")
#         wav_path = os.path.join(wav_dir, wav_filename)
#         convert_to_wav(audio_path, wav_path)
#         os.remove(audio_path)  # Remove the original OGG file

#         # Transcribe audio
#         print(f"Transcribing {wav_filename}...")
#         transcription = transcribe_audio(wav_path, model)
#         print(f"Transcription: {transcription}")

#         # Append to metadata
#         metadata.append([wav_filename, transcription])

#     # Save metadata to CSV
#     metadata_file = os.path.join(output_dir, "metadata.csv")
#     with open(metadata_file, "w", newline="") as f:
#         writer = csv.writer(f, delimiter="|")
#         writer.writerows(metadata)
#     print(f"Metadata saved at {metadata_file}")

# # Parameters
# character_name = "MARCH_7th"
# character_url = "https://honkai-star-rail.fandom.com/wiki/March_7th/Voice-Overs"
# output_dir = os.path.join("data", character_name)

# scrape_and_transcribe(character_url, output_dir, character_name)







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
