import openai
from typing import Dict, List, Union
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import EngineResult, OperatorConfig
from pprint import pprint
import csv
import os
import json
import io
import tempfile

from app.utils.pii_detector import *
from app.utils.mask_generator import *
from app.utils.mask_generator import *
from app.utils.context_analyzer import *


def process_text(file_path: str, api_key: str, data_usage: str, llm_model: str) -> str:
    """
    Process a text file to mask PII, preserving the original file type and structure.
    
    :param file_path: Path to the input text file
    :param project: Dictionary containing project information including API key, data usage, and model
    :return: Path to the output file with masked PII
    """

    # Get the file extension
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # Read and process the file based on its type
    if file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        masked_content = mask_text(content, api_key, data_usage, llm_model)
    elif file_extension == '.csv':
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            content = [row for row in csv_reader]
        masked_content = [mask_text(' '.join(row), api_key, data_usage, llm_model).split() for row in content]
    elif file_extension == '.json':
        with open(file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)
        masked_content = mask_json(content, api_key, data_usage, llm_model)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Supported types are .txt, .csv, and .json")

    # Prepare the output file path
    output_dir = os.path.join(os.path.dirname(file_path), 'masked')
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.basename(file_path)
    output_file_path = os.path.join(output_dir, f"masked_{file_name}")

    # Write the masked content to the output file
    if file_extension == '.txt':
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(masked_content)
    elif file_extension == '.csv':
        with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(masked_content)
    elif file_extension == '.json':
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(masked_content, f, indent=2)

    return output_file_path


def mask_text(text: str, api_key: str, data_usage: str, llm_model: str) -> str:
    """Helper function to mask a single text string"""
    analyzer_results = detect_pii_in_text(text)
    anonymized_text, entity_mapping = get_anonymized_text(text, analyzer_results)
    pii_variables = {result.entity_type: result.text for result in analyzer_results}
    context_analysis = get_context_characteristics(api_key, pii_variables, data_usage, text, anonymized_text, llm_model)
    replacements = generate_pii_replacement(api_key, context_analysis, llm_model)
    return generate_text_mask(text, context_analysis, replacements)


def mask_json(data: Union[Dict, List], api_key: str, data_usage: str, llm_model: str) -> Union[Dict, List]:
    """Helper function to mask JSON data"""
    if isinstance(data, dict):
        return {k: mask_json(v, api_key, data_usage, llm_model) if isinstance(v, (dict, list)) else mask_text(str(v), api_key, data_usage, llm_model) for k, v in data.items()}
    elif isinstance(data, list):
        return [mask_json(item, api_key, data_usage, llm_model) if isinstance(item, (dict, list)) else mask_text(str(item), api_key, data_usage, llm_model) for item in data]
    else:
        return data


def process_text_file(input_file_path: str, api_key: str, data_usage: str, llm_model: str, output_file_path: str = None) -> str:
    """Process a file to mask PII, preserving the original file type and structure."""
    # Get the file extension
    _, file_extension = os.path.splitext(input_file_path)
    file_extension = file_extension.lower()

    # Read and process the file based on its type
    if file_extension == '.txt':
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        masked_content = mask_text(content, api_key, data_usage, llm_model)
    elif file_extension == '.csv':
        with open(input_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            content = [row for row in csv_reader]
        masked_content = [mask_text(' '.join(row), api_key, data_usage, llm_model).split() for row in content]
    elif file_extension == '.json':
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = json.load(file)
        masked_content = mask_json(content, api_key, data_usage, llm_model)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Supported types are .txt, .csv, and .json")

    # Prepare the output file path if not provided
    if output_file_path is None:
        file_name, _ = os.path.splitext(input_file_path)
        output_file_path = f"{file_name}_masked{file_extension}"

    # Write the masked content to the output file
    if file_extension == '.txt':
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(masked_content)
    elif file_extension == '.csv':
        with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(masked_content)
    elif file_extension == '.json':
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(masked_content, f, indent=2)

    return output_file_path


def mask_text(text: str, api_key: str, data_usage: str, llm_model: str) -> str:
    """Helper function to mask a single text string"""
    analyzer_results = detect_pii_in_text(text)
    anonymized_text, entity_mapping = get_anonymized_text(text, analyzer_results)
    pii_variables = {result.entity_type: result.text for result in analyzer_results}
    context_analysis = get_context_characteristics(api_key, pii_variables, data_usage, text, anonymized_text, llm_model)
    replacements = generate_pii_replacement(api_key, context_analysis, llm_model)
    return generate_text_mask(text, context_analysis, replacements)


def mask_json(data: Union[Dict, List], api_key: str, data_usage: str, llm_model: str) -> Union[Dict, List]:
    """Helper function to mask JSON data"""
    if isinstance(data, dict):
        return {k: mask_json(v, api_key, data_usage, llm_model) if isinstance(v, (dict, list)) else mask_text(str(v), api_key, data_usage, llm_model) for k, v in data.items()}
    elif isinstance(data, list):
        return [mask_json(item, api_key, data_usage, llm_model) if isinstance(item, (dict, list)) else mask_text(str(item), api_key, data_usage, llm_model) for item in data]
    else:
        return data


def extract_text_from_file(file_path: str) -> Union[str, List[str], Dict[str, Union[str, List[str]]]]:
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Get the file extension 
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    # Process the file based on its extension
    if file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    
    elif file_extension == '.csv':
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            return [' '.join(row) for row in csv_reader]
    
    elif file_extension == '.json':
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, dict):
                return {k: v if isinstance(v, str) else json.dumps(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [item if isinstance(item, str) else json.dumps(item) for item in data]
            else:
                return json.dumps(data)
    
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Supported types are .txt, .csv, and .json")
