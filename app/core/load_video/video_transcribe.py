import whisper
import json
import os


def transcribe_video(audio_path: str):
    """
    Trascrive il testo di un video e salva nella cartella resources/transcription_dictionaries
    un file json con la trascrzione

    Args:
        audio_path (str): Il percorso del file audio.

    Returns:
        str: Il path contentente il file json con la trascrizione
    """

    if audio_path:
        # Path della directory in cui verrà salvata la trascrizione
        directory_path = "C:/Users/mirko.contini/git/tirocinio-video-rag/resources/transcripions_dictionaries/"

        # Nome del file audio che è stato trascritto
        file_name = os.path.basename(audio_path)

        # Rimuovo l'estensione dal nome del file
        file_name = os.path.splitext(file_name)[0]

        # Carica il modello di whisper
        model = whisper.load_model("base")

        # Trascrive il video con i timestamp delle parole
        result = model.transcribe(audio_path, word_timestamps=True)

        json_file_path = directory_path + file_name + ".json"

        # Salvo la trascrizione nella cartella
        with open(json_file_path, "w") as file:
            json.dump(result, file)

        return json_file_path
