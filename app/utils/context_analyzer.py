# context_analyzer.py
# Functions to analyze context around PII using LLMs
import time
import random
from openai import OpenAI
from typing import Dict, List
from app.utils.pii_detector import *
from config import OPENAI_API_KEY


def get_context_characteristics(api_key: str, pii_variables: Dict[str, str], data_usage: str,
                                unmasked_text: str, redacted_text: str, llm_model: str) -> Dict[str, List[str]]:
    """
    Analyze context using a private LLM to determine important characteristics of PII variables.
    
    :param api_key: API key for OpenAI
    :param pii_variables: Dictionary containing PII variables and their values
    :param data_usage: Description of how the data is being used
    :param unmasked_text: Original text with PII
    :param redacted_text: Text with PII replaced by placeholders
    :param llm_model: Name of the LLM model to use
    :return: Dictionary containing analyzed context information for each PII type
    """


    prompt = f"""
    Analyze the following PII (Personally Identifiable Information) variables in the context of their usage.
    The data is being used for: {data_usage}
    
    Unmasked text: {unmasked_text}
    Redacted text: {redacted_text}
    
    PII variables detected:
    {pii_variables}
    
    For each PII variable type, identify and list important characteristics that should be preserved during pseudonymization.
    Characteristics should be selected based on their relevance within the context of what the data is being used for.
    Consider aspects such as:
    - For names: potential racial and gender implications
    - For addresses: geographical importance, urban/rural context
    - For dates: age implications, generational context
    - For identification numbers: format and structure importance
    
    Provide a structured response with the PII variable type as the key and a list of important characteristics as the value.
    """

    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(model=llm_model,
        messages=[
            {"role": "system", "content": "You are an AI assistant specialized in analyzing PII data for pseudonymization purposes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500)

        # Extracting the response content
        analysis = response.choices[0].message.content

        # Parse response into dict
        characteristics_dict = {}
        for line in analysis.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                characteristics_dict[key.strip()] = [char.strip() for char in value.strip()[1:-1].split(',')]

        return characteristics_dict

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


def generate_pii_replacement(api_key: str, pii_characteristics: Dict[str, List[str]], llm_model: str) -> Dict[str, str]:
    """
    Generate pseudonymized replacements for PII variables based on their characteristics.
    
    :param api_key: API key for OpenAI
    :param pii_characteristics: Dictionary of PII types and their characteristics
    :param llm_model: Name of the LLM model to use
    :return: Dictionary of PII types and their generated replacements
    """
    client = OpenAI(api_key=api_key)
    replacements = {}
    max_retries = 5

    for variable, characteristics in pii_characteristics.items():
        prompt = f"""
        Generate a replacement for the following PII (Personal Identifiable Information) variable:
        Variable type: {variable}

        The replacement should preserve the following characteristics:
        {', '.join(characteristics)}

        Provide only the generated replacement without any additional explanation or context.
        """

        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model=llm_model,
                    messages=[
                        {"role": "system", "content": "You are an AI assistant specialized in generating pseudonymized PII data."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=50
                )

                replacement = response.choices[0].message.content.strip()
                replacements[variable] = replacement
                break  # Success, exit the retry loop

            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Failed to generate replacement for {variable} after {max_retries} attempts: {e}")
                    replacements[variable] = f"[ERROR: Unable to generate replacement for {variable}]"
                else:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Error generating replacement for {variable}. Retrying in {wait_time:.2f} seconds...")
                    time.sleep(wait_time)

    return replacements