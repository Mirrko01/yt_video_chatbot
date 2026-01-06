import pytube as pt
from pytube import extract
import re


def extract_video_id(video_url: str):
    """
       Estrae l'ID del video da un URL di YouTube.

       Args:
           video_url (str): L'URL del video di YouTube.

       Returns:
           str or None: L'ID del video estratto dall'URL, se presente, altrimenti None.
       """

    # Pattern per trovare l'ID del video in un URL di YouTube
    return extract.video_id(video_url)


def download_video(video_url: str):
    """
        Scarica l'audio da un video di YouTube.

        Args:
            video_url (str): L'URL del video di YouTube.

        Returns:
            str: Il path del file audio scaricato
        """

    # Estrae l'ID del video dall'URL fornito
    video_id = extract_video_id(video_url)

    # Inizializza un'istanza di YouTube
    yt = pt.YouTube(video_url)

    # Filtra gli stream disponibili per ottenere solo lo stream audio
    stream = yt.streams.filter(only_audio=True).first()

    if stream:
        # Definisce il nome del file come l'ID del video seguito dall'estensione .mp3
        file_name = video_id + ".mp3"
        output_path = "C:/Users/mirko.contini/git/tirocinio-video-rag/resources/audio_files"

        # Effettua il download dell'audio del video nella cartella specificata
        stream.download(output_path=output_path, filename=file_name)

        print()
        return output_path + "/" + file_name
