from llmx import llm, TextGenerationConfig
from autofinviz.components.summarizer import Summarizer
from autofinviz.components.question import QuestionFormulator
from autofinviz.utils import get_api_key

class Pipeline(object):
    def __init__(self):
        """
        Initialize the Pipeline
        """

        self.summarizer = Summarizer()
        self.question_formulator = QuestionFormulator()
        
        self.data = None

    def get_generator(self):
        api_key = get_api_key()
        self.generator = llm(provider="openai", api_key=api_key)
        self.generation_config = TextGenerationConfig(model="gpt-3.5-turbo", use_cache=True)


    def summarize(self):
        return

    
