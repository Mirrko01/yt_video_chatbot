from app.core.load_video import video_download, video_transcribe, video_vectorialize


def load(payload):
    """
       Carica un video, effettua la trascrizione e lo vettorializza.

       Questa funzione esegue le seguenti operazioni:
       1. Scarica il video dalla URL specificata nel payload.
       2. Trascrive il video scaricato.
       3. Vettorializza la trascrizione del video.

       @param payload: Il payload contenente l'URL del video da scaricare.

       @return: Il database vettoriale aggiornato.
       """

    # Ottieni il percorso della trascrizione del video
    from app.__init__ import video_transcription_path

    # Scarica il video dalla URL specificata nel payload
    # downloaded_video_path = video_download.download_video(payload["video_url"])

    # Trascrivi il video scaricato
    # video_transcription_path = video_transcribe.transcribe_video(downloaded_video_path)

    # Vettorializza la trascrizione del video
    vectorDB = video_vectorialize.vectorialize_video(video_transcription_path)
