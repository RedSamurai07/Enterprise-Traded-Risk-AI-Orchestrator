from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def mask_pii(text: str) -> str:
    # Analyzes text for entities like Names, Account Numbers, etc.
    results = analyzer.analyze(text=text, entities=["PERSON", "IBAN_CODE", "CREDIT_CARD"], language='en')
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized.text

if __name__ == "__main__":
    sample = "Trader John Doe breached the limit on account IBAN12345678."
    print("Masked:", mask_pii(sample))
