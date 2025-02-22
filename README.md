# Voice Conversion team (Divergence 2% Lab)
Requires python 3.10 btw

## Setting up virtual environment (Mac):

python -m venv venv

source venv/bin/activate (OUTDATED UPDATE LATER - CHANGED TO POETRY)

## Setting up venv (Windows):
py -3.10 -m venv venv
venv/Scripts/activate (OUTDATED UPDATE LATER - CHANGED TO POETRY)

## download libraries:
pip install -r requirements.txt (OUTDATED UPDATE LATER - CHANGED TO POETRY)

## Interacting with the db
first install gcloud however u want

make sure to run: and log in with the appropriate account to get perms to interact with the db
gcloud auth application-default login

this is a temporary solution and theres a better one we need to work on later.

## Update requirements.txt with new libraries: 
pip freeze > requirements.txt

## pulling from main branch
git fetch origin
git merge origin/main 




