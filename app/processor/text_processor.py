import openai
from typing import Dict, List, Union
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import EngineResult, OperatorConfig
from pprint import pprint
import csv
import os
import tempfile

from utils.pii_detector import *
from utils.mask_generator import *
from utils.context_analyzer import *

def process_text(text: str, api_key: str, data_usage: str, llm_model: str) -> Dict:

    # Detect pii in the text
    anaylzer_results = detect_pii_in_text(text)

    # Get the anonymized text with entity mapping labels
    anonymized_text = get_anonymized_text(text, analyzer_results)

    # Analyze context with private LLM
    pii_variables = {result.entity_type: result.text for result in anaylzer_results}
    context_analysis = analyze_context_with_private_llm(
        api_key,
        pii_variables,
        data_usage,
        text,
        anonymized_text,
        llm_model
    )

    # Generate pii replacements
    replacements = generate_pii_replacement(api_key, context_analysis, llm_model)

    # Generate final masked text
    final_masked_result = generate_text_mask(text, context_analysis, replacements)

    result = {
        "original_text": text,
        "anonymized_text": anonymized_text,
        "context_analysis": context_analysis,
        "replacements": replacements,
        "final_masked_text": final_masked_result.text,
        "masked_entities": [
            {
            "entity_type": item.entity_type,
            "start": item.start,
            "end": item.end,
            "original_text": item.text,
            "replacement_text": replacements.get(item.entity_type, "[REDACTED]")
            }
            for item in final_masked_result.items
        ]
    }

    return result


def extract_text_from_file(file_path: str) -> Union[str, List[str], Dict[str, Union[str, List[str]]]]:
    pass