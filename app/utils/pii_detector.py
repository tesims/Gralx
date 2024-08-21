# pii_detector.py
# Functions to detect PII in various types of data
from presidio_analyzer import AnalyzerEngine 
from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine, OperatorConfig
from presidio_anonymizer.operators import Operator, OperatorType

from typing import Dict
from pprint import pprint

class InstanceCounterAnonymizer(Operator):
    # Replaces each text with a unique identifier 

    REPLACING_FORMAT = "<{entity_type}_{index}>"

    def operate(self, text: str, params: Dict = None) -> str:
        # Anonymizes the input text 

        entity_type: str = params["entity_type"]

        # entity_mapping is a dict of dicts containing mappings per entity type
        entity_mapping: Dict[Dict:str] = params["entity_mapping"]
        
        entity_mapping_for_type = entity_mapping.get(entity_type)
        if not entity_mapping_for_type:
            new_text = self.REPLACING_FORMAT.format(
                entity_type=entity_type, index=0
            )
            entity_mapping[entity_type] = {}
        
        else: 
            if text in entity_mapping_for_type:
                return entity_mapping_for_type[text]
            
            previous_index = self.get_last_index(entity_mapping_for_type)
            new_text = self.REPLACING_FORMAT.format(
                entity_type = entity_type, index=previous_index + 1
            )
        
        entity_mapping[entity_type][text] = new_text
        return new_text
    
    @staticmethod
    def _get_last_index(entity_mapping_for_type: Dict) -> int:
        
        def get_index(value: str) -> int:
            return int(value.split("_")[-1][:-1])
        
        indices = [get_index(v) for v in entity_mapping_for_type.values()]
        
        return max(indices)
    
    def validate(self, params: Dict = None) -> None:
        if "entity_mapping" not in params:
            raise ValueError("An input Dict called `entity_mapping` is required.")
        if "entity_type" not in params: 
            raise ValueError("An entity_type param is required.")
        
    def operator_name(self) -> str:
        return "entity_counter"
    
    def operator_type(self) -> OperatorType:
        return OperatorType.Anonymize

def detect_pii_in_text(text: str) -> list:
    """
    Detect PII in a text string.
    :param text: Input text.
    :return: List of dictionaries containing detected PII information.
    """
    # Implement text PII detection logic here
    # Use Presidio to Identify PII Variables


    print("Original Text: ")
    pprint(text)
    analyzer = AnalyzerEngine()
    analyzer_results = analyzer.analyze(text=text, language="en")
    print("Analyzer Results: ")
    pprint(analyzer_results)
    
    return analyzer_results

def get_anonymized_text(text: str, analyzer_results: dict) -> str:
    """
    Get Redacted Text with PII Variables Mapped
    :param text: original text, list of dicts with PII variables
    :return: text str of redacted text with entity mapping labels
    """
    anonymizer_engine = AnonymizerEngine()
    anonymizer_engine.add_anonymizer(InstanceCounterAnonymizer)

    entity_mapping = dict()

    anonymized_result = anonymizer_engine.anonymize(
        text,
        analyzer_results,
        {
            "DEFAULT": OperatorConfig(
                "entity_counter", {"entity_mapping": entity_mapping}
            )
        },
    )

    print(anonymized_result.text)
    return anonymized_result.text



def detect_pii_in_image(image_data: str) -> list:
    """
    Detect PII in image data.
    :param image_data: Path to image or raw image data.
    :return: List of dictionaries containing detected PII information.
    """
    # Implement image PII detection logic here
    pass

def detect_pii_in_audio(transcript: str) -> list:
    """
    Detect PII in an audio transcript.
    :param transcript: Transcribed text of the audio.
    :return: List of dictionaries containing detected PII information.
    """
    # Implement audio PII detection logic here
    pass

def detect_pii_in_video(video_data: str) -> list:
    """
    Detect PII in video data.
    :param video_data: Path to video or extracted data from the video.
    :return: List of dictionaries containing detected PII information.
    """
    # Implement video PII detection logic here
    pass
