import langchain.agents
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.prompts.base import BasePromptTemplate
from app.core.ask.tools import question_tool, timestamp_question_tool, summarization_tool
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate


def ask(payload):
    """
    Richiedi una risposta dall'agente basata sulla domanda specificata nel payload.

    Questa funzione crea un agente che utilizza un prompt per generare una risposta basata sulla domanda
    specificata nel payload. L'agente viene quindi eseguito per generare la risposta.

    @param payload: Il payload contenente la domanda dell'utente.
    """

    tools = [question_tool, timestamp_question_tool, summarization_tool]

    # Importa il database vettoriale e il llm
    from app.__init__ import vectorDB, llm

    # Definisci il prompt utilizzato dall'agente
    prompt = ChatPromptTemplate.from_template(
        """You have access to the following tools:
            
            {tools}
            
            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            (this Thought/Action/Action Input/Observation can repeat 3 times)
            
            Final Answer: the final answer to the original input question            
            Question: {question}
            Thought: {agent_scratchpad}

            """
    )

    # Crea l'agente utilizzando il llm, gli strumenti e il prompt definiti
    agent = langchain.agents.create_react_agent(llm=llm, tools=tools, prompt=prompt)

    # Esegui l'agente per generare la risposta alla domanda specificata nel payload
    agent_executor = AgentExecutor(agent=agent,
                                   tools=tools,
                                   verbose=True,
                                   handle_parsing_errors=True,
                                   handle_tool_error=True)
    response = agent_executor.invoke({"question": payload["question"]})

    print(response)
    return response
