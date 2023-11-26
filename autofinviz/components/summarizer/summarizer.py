import pandas as pd
from abc import ABC, abstractmethod
from llmx import llm, TextGenerationConfig

class Summarizer(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        """
        Define prompt for enriching data summary. This is an abstract method and must be
        implemented by all subclasses.

        Returns:
            str: Prompt for enriching data summary
        """
        pass

    @abstractmethod
    def enriched_summary(self) -> str:
        pass

    @classmethod
    def base_summary(self) -> str:
        pass

    @classmethod
    def summarize(
        self, data: pd.DataFrame,
        generator: llm,
        generation_config: TextGenerationConfig,
    ):
        pass