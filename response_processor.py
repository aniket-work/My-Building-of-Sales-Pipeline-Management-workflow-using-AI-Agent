import logging
from typing import Dict, Any

def process_ai_response(response_str: str) -> Dict[str, Any]:
    """Process and structure the AI response"""
    try:
        # Initialize result dictionary
        result = {
            'lead_qualification': {},
            'development_strategy': {},
            'closing_strategy': {}
        }

        def extract_content(text: str, start_marker: str, end_marker: str = None) -> str:
            if start_marker not in text:
                return "N/A"

            start_idx = text.find(start_marker) + len(start_marker)
            if end_marker and end_marker in text[start_idx:]:
                end_idx = text.find(end_marker, start_idx)
                return text[start_idx:end_idx].strip()
            return text[start_idx:].strip()

        sections = response_str.split('#')

        for section in sections:
            section = section.strip()

            if "Lead Qualification" in section:
                result['lead_qualification'] = {
                    'score': extract_content(section, "Lead Score:", "\n"),
                    'deal_size': extract_content(section, "Deal Size:", "\n"),
                    'reasoning': extract_content(section, "Reasoning:", "Next Steps:")
                }

            elif "Development Strategy" in section:
                result['development_strategy'] = {
                    'strategy': extract_content(section, "Engagement Strategy:", "Key Requirements:"),
                    'requirements': extract_content(section, "Key Requirements:", "Risk Factors:")
                }

            elif "Closing Strategy" in section:
                probability = extract_content(section, "Success Probability:", None).strip('%')
                strategy_start = section.find("Closing Strategy:") + len("Closing Strategy:")
                probability_start = section.find("Success Probability:")

                if strategy_start > -1 and probability_start > -1:
                    strategy = section[strategy_start:probability_start].strip()
                    strategy_lines = [line.strip('123456789. ') for line in strategy.split('\n') if line.strip()]
                    strategy = ' '.join(strategy_lines)
                else:
                    strategy = "N/A"

                result['closing_strategy'] = {
                    'strategy': strategy,
                    'probability': probability
                }

        return result

    except Exception as e:
        logging.error(f"Error processing AI response: {str(e)}")
        logging.error(f"Raw response: {response_str}")
        return {
            'lead_qualification': {'score': 'N/A', 'deal_size': 'N/A', 'reasoning': str(e)},
            'development_strategy': {'strategy': 'N/A', 'requirements': 'N/A'},
            'closing_strategy': {'strategy': 'N/A', 'probability': 'N/A'}
        }