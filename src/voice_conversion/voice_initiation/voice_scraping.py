#!/usr/bin/env python3
import os
import csv
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import whisper  # Importing OpenAI's Whisper model
from .audio_matching import convert_to_wav  # Import the existing conversion function

def generate_silence(silence_path, duration=1):
    """Generate a silence WAV file (PCM S16LE)."""
    command = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", "anullsrc=channel_layout=mono:sample_rate=16000",
        "-t", str(duration),
        "-c:a", "pcm_s16le",
        silence_path,
        "-y"
    ]
    subprocess.run(command, capture_output=True, text=True)

def concatenate_with_time_limit(wav_files, output_path, silence_path, min_duration=13, max_duration=17):
    """
    Concatenate audio files (with silence gaps) until the total duration is
    between min_duration and max_duration seconds. If the greedy selection
    doesn't reach the minimum, fall back to using all available files.
    """
    list_file = os.path.join(os.path.dirname(output_path), "wav_list.txt")
    total_duration = 0.0
    selected_files = []

    for wav in wav_files:
        try:
            duration_cmd = [
                "ffprobe", "-i", wav,
                "-show_entries", "format=duration",
                "-v", "quiet",
                "-of", "csv=p=0"
            ]
            duration_str = subprocess.run(duration_cmd, capture_output=True, text=True).stdout.strip()
            if not duration_str:
                continue
            duration = float(duration_str)
        except Exception:
            print(f"⚠️ Skipping unreadable file: {wav}")
            continue

        if total_duration + duration > max_duration:
            # If not reached min_duration, add this file even if it exceeds max_duration.
            if total_duration < min_duration:
                selected_files.append(wav)
                total_duration += duration
            break
        selected_files.append(wav)
        total_duration += duration

    if total_duration < min_duration:
        print("⚠️ Not enough audio to reach the minimum duration. Using all available files instead.")
        selected_files = wav_files

    with open(list_file, "w") as f:
        for wav in selected_files:
            f.write(f"file '{wav}'\n")
            f.write(f"file '{silence_path}'\n")

    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file,
        "-c:a", "pcm_s16le", output_path, "-y"
    ], capture_output=True, text=True)
    os.remove(list_file)
    print(f"✅ Combined audio saved at {output_path}")

def transcribe_audio(wav_path, model):
    """Transcribe the given WAV file using Whisper."""
    result = model.transcribe(wav_path, language='en')
    return result.get("text", "").strip()

def scrape_voice_lines(character_url, character_name):
    """
    Scrape voice lines, convert them to WAV, transcribe them,
    and save metadata (filename and transcription) to a CSV file.
    Then, concatenate the individual WAV files into a combined audio file,
    transcribe that file, and append its transcription to the CSV.
    """
    # Create output directory next to this script
    project_root = os.path.dirname(__file__)
    output_dir = os.path.join(project_root, "data", character_name)
    wav_dir = os.path.join(output_dir, "wavs")
    os.makedirs(wav_dir, exist_ok=True)

    # Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    # Fetch the voice lines page
    response = requests.get(character_url)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    voice_entries = soup.select("table.wikitable tr")
    print(f"Found {len(voice_entries)} voice lines. Starting download and transcription...")

    metadata = []  # List of [wav_filename, transcription]
    wav_files = []

    for i, row in enumerate(voice_entries, start=1):
        audio_elem = row.select_one("audio[src]")
        if not audio_elem:
            continue

        audio_url = urljoin(character_url, audio_elem["src"])
        audio_filename = f"{character_name}{i:04d}.ogg"
        audio_path = os.path.join(wav_dir, audio_filename)

        # Download audio file
        try:
            with requests.get(audio_url, stream=True) as r:
                r.raise_for_status()
                with open(audio_path, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
        except requests.exceptions.RequestException:
            continue

        # Convert OGG to WAV using the imported function
        wav_filename = audio_filename.replace(".ogg", ".wav")
        wav_path = os.path.join(wav_dir, wav_filename)
        convert_to_wav(audio_path, wav_path)
        os.remove(audio_path)

        # Transcribe the individual WAV file
        transcription = transcribe_audio(wav_path, model)
        metadata.append([wav_filename, transcription])
        wav_files.append(wav_path)
        print(f"Processed {wav_filename}")

    # Save metadata CSV
    metadata_file = os.path.join(output_dir, "metadata.csv")
    with open(metadata_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter="|")
        writer.writerow(["filename", "transcription"])
        writer.writerows(metadata)

    # Generate silence and concatenate audio files (total duration ~13-17 seconds)
    silence_path = os.path.join(wav_dir, "silence.wav")
    generate_silence(silence_path)
    # Append "@" to the filename so script.py can quickly locate it for zero-shot reference
    combined_output = os.path.join(output_dir, f"{character_name}_combined@.wav")
    concatenate_with_time_limit(wav_files, combined_output, silence_path)

    # Transcribe the combined WAV file and append its transcription to the metadata CSV
    if os.path.exists(combined_output) and os.path.getsize(combined_output) > 0:
        combined_transcription = transcribe_audio(combined_output, model)
        print(f"Combined transcription: {combined_transcription}")
        with open(metadata_file, "a", newline="") as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([os.path.basename(combined_output), combined_transcription])
    else:
        print("⚠️ Combined audio file not created or is empty.")

if __name__ == "__main__":
    # Example: Use Herta's voice lines from the fan wiki
    character_name = "Herta"
    character_url = "https://honkai-star-rail.fandom.com/wiki/Herta/Voice-Overs"
    scrape_voice_lines(character_url, character_name)
