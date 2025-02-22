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