from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
import os 


def load_model(model_name):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name=model_name)
    return llm 


def convert_newlines(prompt):
    prompt = prompt.replace("\n", "  \n")
    return prompt


def apply_skill(llm, skill, prompt, lang_eng=False):
    with open(f"templates/system.prompt", "r") as f:
        system_message = f.read()

    if lang_eng:
        with open(f"templates/lang_eng.prompt", "r") as f:
            lang_message = f.read()
    else:
        with open(f"templates/lang_default.prompt", "r") as f:
            lang_message = f.read()

    system_message = system_message + '\n' + lang_message
    print(system_message)

    with open(f"templates/{skill}.prompt", "r") as f:
        template = f.read()

    prompt_template = PromptTemplate.from_template(template)
    formatted_input = prompt_template.format(prompt=prompt)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=formatted_input),
    ]

    response = llm.invoke(messages)

    return response.content


def insert_phrases(llm, phrases_to_insert, prompt):
    with open(f"templates/system.prompt", "r") as f:
        system_message = f.read() 
    
    with open(f"templates/insert_phrases.prompt", "r") as f:
        template = f.read()

    phrases_collection = ""
    for i, phrase in enumerate(phrases_to_insert):
        phrases_collection += f"{i+1}. {phrase}\n"
    
    prompt_template = PromptTemplate.from_template(template)
    formatted_input = prompt_template.format(phrases_collection=phrases_collection,
                                             prompt=prompt)
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=formatted_input),
    ]

    response = llm.invoke(messages)

    return response.content


