import os
import pyrootutils
from fish_speech.models.vqgan import inference
from pathlib import Path

# Compute the project root as the parent directory of the directory that contains pyproject.toml.
# Adjust this based on your script's location.
project_root = Path(__file__).resolve().parent.parent

# Setup root using only supported arguments
pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

def main():
    # Path to your input audio file (absolute path)
    input_file = str(project_root / "paimon.wav")
    
    # Path to the model checkpoint (relative to the project root)
    checkpoint_path = str(project_root / "checkpoints/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth")
    
    # Call the inference function from fish_speech.
    output = inference.run_inference(input_file, checkpoint_path)
    print("Inference output:", output)

if __name__ == "__main__":
    main()
