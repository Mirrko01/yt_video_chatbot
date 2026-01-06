import json

from langchain_core.documents import Document


def vectorialize_video(video_transcription_path):
    """
        Vettorializza la trascrizione del video.

        Questa funzione legge un file di trascrizione JSON, elabora i suoi segmenti e li aggiunge come documenti
        al database vettoriale con i metadati associati.

        @param video_transcription_path: Il percorso del file JSON di trascrizione del video.

        @return: Il database vettoriale aggiornato.
        """
    from app.__init__ import vectorDB, embeddings

    # Apri e carica il file di trascrizione JSON
    with open(video_transcription_path, "r") as file:
        loaded_dictionary = json.load(file)

    text_with_timestamps_dict = []

    # Estrai informazioni rilevanti (id, testo, inizio, fine) da ogni segmento della trascrizione
    for segment in loaded_dictionary["segments"]:
        tmp_dict = {"id": segment["id"], "text": segment["text"], "start": segment["start"], "end": segment["end"]}
        text_with_timestamps_dict.append(tmp_dict)

    documents_list = []

    # Crea oggetti Document per ogni segmento con metadati e aggiungili alla lista dei documenti
    for tmp in text_with_timestamps_dict:
        document = Document(
            page_content=tmp["text"],
            metadata=tmp,
        )
        documents_list.append(document)

    # Aggiungi i documenti al database vettoriale
    vectorDB.add_documents(documents=documents_list)

    return vectorDB
