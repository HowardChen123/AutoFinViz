import pandas as pd
from abc import ABC, abstractmethod
from llmx import llm, TextGenerationConfig

class Summarizer(ABC):
    def __init__(self) -> None:
        pass

    def get_prompt(self) -> str:
        """
        Define prompt for enriching data summary. This is an abstract method and must be
        implemented by all subclasses.

        Returns:
            str: Prompt for enriching data summary
        """
        pass

    def enriched_summary(self) -> str:
        pass

    @classmethod
    def base_summary(self) -> str:
        pass

    @classmethod
    def cols_info(cls, df: pd.DataFrame, n_samples=3) -> list[dict]:
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


    @classmethod
    def summarize(
        self, data: pd.DataFrame,
        generator: llm,
        generation_config: TextGenerationConfig,
    ):
        
        data_info = self.cols_info(data)
        base_summary = {
            "dataset_description": "",
            "fields": data_info,
        }



        
        