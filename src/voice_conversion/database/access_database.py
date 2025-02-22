from google.cloud import firestore

def fetch_voice_lines(character, emotion=None):
    print(f"fetching {character}'s {emotion} voice lines")
    db = firestore.Client(project="voice-samples-f2816")
    
    collection_ref = db.collection("character_voice_lines")
    query = collection_ref.where("character", "==", character)
    
    if emotion:
        query = query.where("emotion", "==", emotion)
    
    results = query.stream()
    
    voice_lines = [doc.to_dict() for doc in results]
    
    if not voice_lines:
        print("No matching voice lines found.")
        return []
    
    return voice_lines


character_name = "MARCH_7TH"
emotion_filter = "testing"  # Change this to None if no emotion filtering is needed

voice_lines = fetch_voice_lines(character_name, emotion_filter)
for line in voice_lines:
    print(line)


