# VOICE CONVERSION TEAM – DIVERGENCE 2% LAB

 **Bringing cutting-edge audio transformations to life, one line of code at a time.**

<img src="contruct.png" alt="Project Overview" title="Project Overview" width="50%" height="50%">

---

## Introduction
Welcome to the **Voice Conversion** repository. Here, we push the boundaries of speech processing and database interaction. This guide will help you get started with our setup. **Note:** Our environment now relies on Poetry (Python 3.10+). We will later switch to uv!

---

## Project Setup

### 1. Poetry Environment
1. **Install Poetry**  
   - On macOS / Linux:  
       curl -sSL https://install.python-poetry.org | python3 -
   - On Windows (PowerShell):  
       (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
   - For detailed instructions, see https://python-poetry.org/docs/.

2. **Configure Project**  
   - Clone the repository:
       git clone https://github.com/YourUsername/voice-conversion.git
   - Navigate to the project folder:
       cd voice-conversion
   - Install dependencies via Poetry:
       poetry install
   - Activate the Poetry shell (optional, but recommended for local development):
       poetry env activate (copy paste the output in the terminal)

### 2. Pulling Latest Changes from Main
Keep your local repository up-to-date:
    
    git fetch origin
    git merge origin/main

(Or, if you’re using branches, replace `main` with your target branch.)

---

## Interacting with the Database

(*NOT YET FULLY INTEGRATED*)

We currently rely on **Google Cloud Firestore**.  
1. **Install the gcloud CLI** if you haven’t already.  
2. **Authenticate** with:
   
       gcloud auth application-default login
   
   This grants the necessary permissions to interact with our Firestore database.  
3. Future improvements will refine this authentication step to a more permanent solution.

---

## Additional Tips

- **Updating Dependencies**  
  If you add or remove libraries, simply edit `pyproject.toml` and run:
      
      poetry update

  Or, add the library directly:
      poetry add

  Poetry will handle locking versions in `poetry.lock`.

- **Requirements File (Legacy)**  
  If you still need a `requirements.txt` for external use, you can generate one with:
      
      poetry export -f requirements.txt --output requirements.txt
  
  However, the recommended approach is to rely on Poetry’s lockfile.

---

## Roadmap & Future Work
- **Enhanced gcloud Integration**: We’ll streamline authentication for a more secure and automated experience.  
- **Expanded Testing**: Additional unit and integration tests to ensure robust transformations.  
- **Performance Tuning**: Profiling and optimization for large-scale voice conversion.

---
**Any questions or suggestions?**  
Feel free to open an issue or reach out to the team.

> *Stay tuned for more updates as we refine the pipeline and push the limits of voice conversion technology!*

---

© 2025 Voice Conversion Team – Divergence 2% Lab
