# context_analyzer.py
# Functions to analyze context around PII using LLMs
import openai
from typing import Dict, List
from pii_detector import *


def analyze_context_with_private_llm(api_key: str, pii_variables: dict, data_usage: str, 
                                     unmasked_text: str, redacted_text: str, llm_model: str) -> Dict[str, List[str]]:
    """
    Analyze context using a private LLM.
    :param pii_variables: List of dictionaries containing PII variables.
    :return: List of dictionaries containing analyzed context information.
    
    Note: Structured to be compaitable with OpenAI API to connect a 
          compatible self-hosted LLM use vLLM framework when deploying
    """
    
    openai.api_key = api_key
    
    prompt = f""" 
    Analyze the following PII (Personally Identifiable Information) variables in the context of their usage.
    The data is being used for: {data_usage}

    Unmasked text: {unmasked_text}
    Redacted text: {redacted_text}

    PII variables detected:
    {pii_variables}

    For each PII variable, identify and list important characteristics the should be preserved during pseudonymization.
    Characteristics should be selected based their relevance within context of what the data is being used for.
    Consider aspects such as:
    - For names: potential racial and gender implications
    - For addresses: geographical importance, urban/rural context
    - For dates: age implications, generational context
    - For identification numbers: format and structure importance
    
    Provide a structured response with the corresponding variables entity_key from the identified PII variables as the key and a list of important characteristics as the value.
    """

    try:
        response = openai.ChatCompletion.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": "You are an AI assistant specialized in analyzing PII data for pseudonymization purposes."},
                {"role": "user", "content": prompt}
            ],
            temperature = 0.2, 
            max_tokens = 500
        )

        # extracting the response content
        analysis = response.choices[0].message['content']

        # parse response into dict
        characteristics_dict = {}
        for line in analysis.split('\n'):
            if ':' in line:
                key, value = line.split(':',1)
                characteristics_dict[key.strip()] = [char.strip() for char in value.strip()[1:-1].split(',')]
        
        return characteristics_dict
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def generate_pii_replacement(api_key: str, pii_characteristics: Dict[str, List[str]], llm_model: str) -> Dict[str, str]:
    openai.api_key = api_key

    replacements = {}

    for variable, characteristics in pii_characteristics.items():
        prompt = f"""
        Generate a replacement for the following PII (Personal Identifiable Information) variable:
        Variable type: {variable}

        The replacement should preserve the following characteristics:
        {', '.join(characteristics)}

        Provide only the generated replacement without any additional explaination or context.
        """

        try:
            response = openai.ChatCompletion.create(
                model = llm_model,
                messages = [
                    {"role": "system", "content": "You are an AI assistant specialized in generating pseudonymized PII data."},
                    {"role": "user", "content": prompt}

                ],
                temperature = 0.7,
                max_tokens = 50
            )

            replacement = response.choices[0].message['content'].strip()
            replacements[variable] = replacement
            
        except Exception as e:
            print(f"An error occurred while generating replancement for {variable}: {e}")
            replacements[variable] = f"[ERROR: Unable to generate replacement for {variable}]"

    return replacements 




def generate_contextual_replacements_with_public_llm(context_data: list) -> list:
    """
    Generate contextually appropriate replacements using a public LLM.
    :param context_data: List of dictionaries containing context information.
    :return: List of dictionaries containing generated replacements.
    """
    # Implement public LLM replacement generation logic here
    pass
