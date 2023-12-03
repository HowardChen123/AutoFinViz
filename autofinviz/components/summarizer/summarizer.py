import pandas as pd
import json

from autofinviz.utils import generateLLMResponse

class Summarizer():
    def __init__(self) -> None:
        pass

    def find_new_metrics(self, df: pd.DataFrame, df_name: str, category: str) -> list:

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
            Identify the top 3 metrics that can be derived from a given dataset. The metrics must be calculable from each data row. 
            Leverage your domain knowledge, the derived metrics should meaningful and convey important message.
            Respond only with the metric names in the format: ["metric 1", "metric 2", "metric 3"].
        """

        message = f"""
            Analyzing the dataset '{df_name}', which includes the following columns: {', '.join(col)}. 
            What are the top 3 metrics that can be derived from this dataset? Please list them without explanation. 
        """

        new_metrics = generateLLMResponse(system_prompt, message)
        new_metrics = json.loads(new_metrics)

        return new_metrics

    def create_new_col(self, new_metrics: list, df: pd.DataFrame, df_name: str, category: str) -> str:

        col = df.columns

        if category == "Market Dataset":

            system_prompt = """
            You are an experienced Market financial analyst that understand all market dataset, including Stock Price market, Commodity Price market and Currecy Exchange Price market.
            You know all the calculation of financial concepts.
            """

        elif category == "Economic Dataset":

            system_prompt = """
            You are an experienced Economist that understand all economic dataset, including Gross Domestic Product, Unemployment Rate and Consumer Price Index.
            You know all the calculation of economic concepts.
            """

        elif category == "Corporate Dataset":
            
            system_prompt = """
            You are an experienced Economist that understand all economic dataset, including Gross Domestic Product, Unemployment Rate and Consumer Price Index.
            You know all the calculation of economic concepts.
            """

        else:
            return None


        system_prompt += """
            Provide only executable Python code. The code should:
            1. Use 'df' to represent the dataframe.
            2. Not read the dataset into a dataframe.
            3. Not print out any new values.
            4. Add new columns as specified.
            5. Require no further input or interaction.
        """

        message = f"""
            Dataset name: {df_name}
            Column names: {', '.join(col)}
            Required new columns: {', '.join(new_metrics)}

            Generate executable Python code to add these new columns to 'df'. The code should follow the above guidelines and not perform any additional actions.
        """

        return generateLLMResponse(system_prompt, message)
    
    def update_df(self,  df: pd.DataFrame, code: str):

        try:
            exec(code)
        except Exception as e:
            print(f"An error occurred: {e}")

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
    ):

        new_metrics = self.find_new_metrics(df, df_name, category)

        print(new_metrics)

        new_col_code = self.create_new_col(new_metrics, df, df_name, category)

        print(new_col_code)

        self.update_df(df, new_col_code)

        print(df)
        
        base_summary = self.base_summary(df)
        summary = {
            "dataset_description": "",
            "fields": base_summary,
        }

        return summary, df


if __name__ == "__main__":

    summarizer = Summarizer()

    df = pd.read_csv("example/data/Stock_price_TSLA.csv")
    df_name = "Stock_price_TSLA"
    category = "Market Dataset"

    summarizer.summarize(df, df_name, category)