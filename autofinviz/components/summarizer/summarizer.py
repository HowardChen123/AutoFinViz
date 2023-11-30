import pandas as pd
from abc import ABC, abstractmethod
from openai import OpenAI
import json
import re

# from ...utils import get_api_key

class Summarizer():
    def __init__(self) -> None:
        pass

    def find_new_metrics(self, df: pd.DataFrame, df_name: str, category: str, gpt_client: OpenAI) -> list:

        col = df.columns

        if category == "Market Dataset":

            system_prompt = "You are an experienced Market financial analyst that understand all market dataset, including Stock Price market, Commodity Price market and Currecy Exchange Price market."
        
        elif category == "Economic Dataset":

            system_prompt = "You are an experienced Economist that understand all economic dataset, including Gross Domestic Product, Unemployment Rate and Consumer Price Index"

        elif category == "Corporate Dataset":

            system_prompt = " You are an experienced Corporate financial analyst that understand all company statement, including Income Statement and Cash Flow Statement."
        
        else:
            return None

        system_prompt += """
        You can figure out the TOP3 metrics derived from the dataset.
        TOP means each data row can calculate a new metric.
        ONLY return the result in a form of "["name 1", "name 2", "name 3"]"
        """

        message = f"""
        I have a dataset called {df_name}, with its columns names below
        {list(col)}
        What are the TOP3 metrics I can derived from this dataset? (without explaination) 
        """

        completion = gpt_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": message},
            ]
        )

        new_metrics = completion.choices[0].message.content
        new_metrics = json.loads(new_metrics)

        return new_metrics

    def create_new_col(self, new_metrics: list, df: pd.DataFrame, df_name: str, category: str, gpt_client: OpenAI) -> str:

        col = df.columns

        if category == "Market Dataset":

            system_prompt = """
            You are an experienced Market financial analyst that understand all market dataset, including Stock Price market, Commodity Price market and Currecy Exchange Price market.
            You know all the calculation of financial concpets.
            """

        elif category == "Economic Dataset":

            system_prompt = """
            You are an experienced Economist that understand all economic dataset, including Gross Domestic Product, Unemployment Rate and Consumer Price Index.
            You know all the calculation of economic concpets.
            """

        elif category == "Corporate Dataset":
            
            system_prompt = """
            You are an experienced Economist that understand all economic dataset, including Gross Domestic Product, Unemployment Rate and Consumer Price Index.
            You know all the calculation of economic concpets.
            """

        else:
            return None


        system_prompt += """
        i) ONLY return Executable Python code, nothing else
        ii) NO NEED TO read the dataset into a dataframe
        iii) DO NOT print out the new values
        iv) USE "df" to represent the dataframe in the code
        """

        message = f"""
        I have a dataset called {df_name}, with its columns names below
        {list(col)}
        
        Can you provide executable Python code to add the following columns
        {new_metrics}

        ONLY return Executable Python code, nothing else
        USE "df" to represent the dataframe in the code
        Code must not require further input
        
        """

        completion = gpt_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": message},
        ])

        return completion.choices[0].message.content
    
    def update_df(self,  df: pd.DataFrame, code: str):

        try:
            exec(code)
        except Exception as e:
            print(f"An error occurred: {e}")
            # self.update_df(df, code)



    def base_summary(self, df: pd.DataFrame, n_samples=3) -> list:
        def get_samples(column):
            non_null = column.dropna().unique()
            return non_null[:n_samples].tolist()

        properties_list = []
        for column in df.columns:
            col_data = df[column]
            dtype = col_data.dtype

            # Determine the data type
            if dtype in [int, float, complex]:
                dtype_str = "number"
                min_val = float(col_data.min()) if dtype == float else int(col_data.min())
                max_val = float(col_data.max()) if dtype == float else int(col_data.max())
            elif dtype == bool:
                dtype_str, min_val, max_val = "boolean", None, None
            elif pd.api.types.is_datetime64_any_dtype(col_data) or (dtype == object and pd.to_datetime(col_data, errors='coerce').notna().any()):
                dtype_str, min_val, max_val = "date", col_data.min(), col_data.max()
            elif dtype == object:
                dtype_str, min_val, max_val = "string" if col_data.nunique() / len(col_data) >= 0.5 else "category", None, None
            else:
                dtype_str, min_val, max_val = str(dtype), None, None

            properties = {
                "dtype": dtype_str,
                "min": min_val,
                "max": max_val,
                "num_unique_values": col_data.nunique(),
                "samples": get_samples(col_data),
                "semantic_type": "",
                "description": ""
            }

            properties_list.append({"column": column, "properties": properties})

        return properties_list


    def summarize(
        self, df: pd.DataFrame,
        df_name: str, 
        category: str,
        gpt_client: OpenAI
        # generator: llm,
        # generation_config: TextGenerationConfig,
    ):

        new_metrics = self.find_new_metrics(df, df_name, category, gpt_client)

        print(new_metrics)

        new_col_code = self.create_new_col(new_metrics, df, df_name, category, gpt_client)

        print(new_col_code)


        self.update_df(df, new_col_code)

        print(df)
        
        base_summary = self.base_summary(df)
        summary = {
            "dataset_description": "",
            "fields": base_summary,
        }

        print(summary)


if __name__ == "__main__":

    summarizer = Summarizer()

    # df = pd.read_csv("example/data/Stock_price_TSLA.csv")
    # df_name = "Stock_price_TSLA"
    # category = "Market Dataset"

    df = pd.read_csv("example/data/Consumer_price_index.csv")
    df_name = "Consumer_price_index"
    category = "Economic Dataset"

    df = pd.read_csv("example/data/Consumer_price_index.csv")
    df_name = "Consumer_price_index"
    category = "Economic Dataset"

    def get_api_key():
        try:
            with open("apikey", 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("'%s' file not found" % "apikey")

    api_key = get_api_key()       

    gpt_client = OpenAI(
        api_key= api_key
    )

    summarizer.summarize(df, df_name, category, gpt_client)


        