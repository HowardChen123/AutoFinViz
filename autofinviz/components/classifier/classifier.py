import pandas as pd

from autofinviz.utils import generateLLMResponse

class Classifier():
    def __init__(self) -> None:
        pass

    def classify(self, df: pd.DataFrame):

        col = df.columns

        system_prompt = """
        You are an experienced financial analyst that understand all financial datasets and can classify them into Market Dataset, Economic Dataset or Corporate Financial Dataset.
        i) ALWAYS choose one from Market Dataset, Economic Dataset or Corporate Financial Dataset when classifying dataset
        ii) ONLY return either 'Market Dataset' tag, 'Economic Dataset' tag or 'Corporate Financial Dataset' tag.
        """

        message = f"""
        Classify the dataset into Market Dataset, Economic Dataset or Corporate Financial Dataset, with its columns names below
        {list(col)}
        ONLY return either 'Market Dataset' tag, 'Economic Dataset' tag or 'Corporate Financial Dataset' tag.
        """

        return generateLLMResponse(system_prompt, message)


