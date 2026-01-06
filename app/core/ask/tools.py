import json
import textwrap
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain


def input_to_json(input_msg: str):
    """
       Converte un messaggio di input in formato JSON.

       Questa funzione utilizza un modello linguistico per generare un JSON contenente informazioni
       su un intervallo di tempo specificato nel messaggio di input.

       @param input_msg: Il messaggio di input contenente l'intervallo di tempo.
       @return: Il JSON generato.
    """

    from app.__init__ import video_transcription_path, llm

    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY')
    )

    timestamps_example = [{"start": 10, "end": 15}, {"start": 300, "end": 600}]
    prompt = f'''
    You are an assistant tasked with rephrasing an input string. From this string, you will need to extract a "start"
    and an "end" field in JSON format, representing the beginning and end of a time interval in a video.
    Obviously, the start should be the smallest of the two numbers.
    If the input contains a time interval with minutes instead of seconds, you have to convert it to seconds.

    It is mandatory that in the output, start and end are are enclosed in double quotes like this "start" "end"
    For example:


    "What happens from second 10 to second 15 of the video?"
    {timestamps_example[0]}

    
    "What happens from minute 1 to minute 50 of the video?"
    {timestamps_example[1]}

    This is the body of text to extract the information from:
    {input_msg}
    '''

    openai_response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}]
    )

    json_response = json.loads(
        openai_response.choices[0].message.content.replace("'start'", '"start"').replace("'end'", '"end"'))
    return json_response


@tool
def question_tool(question):
    """
        Use this tool when the question has no time stamp references, so when the question "
        asks something in general about the videos
    """

    from app.__init__ import vectorDB, llm

    template = """Answer the following question based only on the provided context, the context will be 
                    the transcription of a video, if you are unsure about the 
                    answer, just say that you don't know how to answer, don't make up any answer.

                    <context>                           
                    {context}
                    </context>

                    Question: {input}"""

    prompt = ChatPromptTemplate.from_template(template)

    document_chain = create_stuff_documents_chain(llm, prompt)

    retriever = vectorDB.as_retriever()

    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    res = retrieval_chain.invoke({
        "input": question
    })

    return res


@tool
def timestamp_question_tool(question):
    """
        Execute the elaboration of the input question

        This tool extracts the corresponding text from the time interval specified in the question
        and returns an elaboration of that text

        Args:
        question (str): La domanda contenente un riferimento temporale.
    Returns:
        str: A response to the question
    """

    from app.__init__ import video_transcription_path, llm

    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY')
    )

    json_file_path = video_transcription_path

    with open(json_file_path, "r") as file:
        loaded_dictionary = json.load(file)

    input_timestamps = input_to_json(question)

    text = ""
    first_segment_id = -1
    last_segment_id = -1

    for segment in loaded_dictionary["segments"]:
        for word in segment["words"]:

            if int(word["start"]) == input_timestamps["start"] and first_segment_id == -1:
                first_segment_id = segment["id"]

            if int(word["start"]) == input_timestamps["end"]:
                last_segment_id = segment["id"]

    if first_segment_id != -1 and last_segment_id != -1:
        for segment in loaded_dictionary["segments"]:
            if first_segment_id <= segment["id"] <= last_segment_id:
                text += segment["text"]

        print(first_segment_id, last_segment_id)

        prompt = f'''
                Take the following text, which represents a section of a video, and do the following:
    
                Summarize the content in a clear and verbose manner.
                Reformulate the text to make it more comprehensible.
                Highlight the most important topic discussed in the section.
                Provide a suitable title that reflects the main idea.
    
                The format of your output should be:
                [TITLE]
                [SUMMARIZED TEST]
    
    
                Text:
                {text}
                '''

        openai_response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}]
        )

        return openai_response

    else:
        return "Timestamps not found"


@tool
def summarization_tool(question):
    """
            Execute the elaboration of the input question

            You should use this tool when the question asks a summarization of the video,
            or what main topics are beign discussed in the video.

            The output should be a bulleted list, each bullet should represent the summarization of a section of the
            video transcription

    """
    from app.__init__ import video_transcription_path, llm

    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY')
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"])

    with open(video_transcription_path) as f:
        text = f.read()

    texts = text_splitter.split_text(json.loads(text)["text"])

    for i in range(0, len(texts), 5):
        texts[i] += " #end of section#"

    prompt = f'''
        You are an assistant tasked with summarizing a long text file. The text is divided in sections, each of them 
        ends with the separator "#end of section#". You should summarize each section.

        Write a concise bullet point summary of the following text, 
        every point should be a really concise title of what the section is talking about,
        use up to 4 words for every bullet point

        This is the input text
        {texts}
        '''

    openai_response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return openai_response.choices[0].message.content
