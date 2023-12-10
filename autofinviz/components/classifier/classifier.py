import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

class Classifier():

    def __init__(self) -> None:
        self.model = ChatOpenAI(model_name="gpt-3.5-turbo")
        self.prompt_template = ChatPromptTemplate.from_template("""
            You are an experienced financial analyst. Classify datasets into one of the following categories: \
                'Market Dataset', 'Economic Dataset', or 'Corporate Financial Dataset'. 
            Your response must be exactly one of these three options.

            {message}
            """
        )
        self.output_parser = StrOutputParser()

    def validate_output(self, text):
        valid_tags = ['Market Dataset', 'Economic Dataset', 'Corporate Financial Dataset']
        for tag in valid_tags:
            if tag in text:
                return f"{tag}"
        raise ValueError("Output does not contain a valid dataset tag")

    def classify(self, df: pd.DataFrame):
        col = df.columns

        message = f"""
        Here are the column names of a dataset: {list(col)}. Based on these names, classify the dataset into one of the specified categories.
        """
        chain = self.prompt_template | self.model | self.output_parser
        return self.validate_output(chain.invoke({"message": message}))


if __name__ == "__main__":

    import config
    classifier = Classifier()

    df = pd.read_csv("example/data/Stock_price_TSLA.csv")
    df_name = "Stock_price_TSLA"

    category = classifier.classify(df)
    print(category)