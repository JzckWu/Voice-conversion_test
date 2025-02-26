import subprocess
import json

def get_audio_properties(audio_path):
    """Extract the sample rate and channels from the original audio file."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate,channels",
        "-of", "json", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)
    stream = info["streams"][0]
    return int(stream["sample_rate"]), int(stream["channels"])

def convert_to_wav(audio_path, wav_path):
    """Convert audio to WAV while preserving original sample rate and channels."""
    sample_rate, channels = get_audio_properties(audio_path)
    subprocess.run([
        "ffmpeg", "-i", audio_path,
        "-ar", str(sample_rate),
        "-ac", str(channels),
        "-c:a", "pcm_s16le",
        wav_path, "-y"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
