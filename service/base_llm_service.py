
### `services/llm_service.py`

class BaseLLMService:
    def __init__(self):
        pass

    def get_answers(self, questions, file):
        raise NotImplementedError("Subclasses should implement this method")


class LLMFactory:
    @staticmethod
    def get_llm_service(service_type):
        from service.openai_service import OpenAIService
        from service.grok_service import GrokService
        if service_type == 'openai':
            return OpenAIService()
        elif service_type == 'grok':
            return GrokService()
        else:
            raise ValueError(f"Invalid service type: {service_type}")
