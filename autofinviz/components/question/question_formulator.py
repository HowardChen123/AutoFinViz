from autofinviz.utils import generateLLMResponse
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser

class QuestionFormulator():
    def __init__(self, model="gpt-3.5-turbo") -> None:
        self.model = ChatOpenAI(model_name=model)

    def formulate_question(self, summary, category, num_goals=5):

        if category == "Market Dataset":
            list_of_graph = ["OHLC Chart", "Moving Average Graph", "RSI Graph","Candlestick Chart", "Moving Average Convergence Divergence",
                "Waterfall Chart", "Funnel Chart", "Time Series graph with a range slider","Multi-Measurment Time Series Graph", ]
        else:
            list_of_graph = ["Multi-Measurment Time Series Graph", "Time Series graph with a range slider"]
    
        # Read the base system prompt from the file
        with open('autofinviz/components/question/prompts/format_instruction.tmpl', 'r') as file:
            format_instruction = file.read()

        # Read the base system prompt from the file
        with open('autofinviz/components/question/prompts/graph_description.tmpl', 'r') as file:
            graph_description = file.read()
        

        user_prompt = f"""

            CHOOSE {num_goals} plots, that fit for dataframe df, among {list_of_graph} as the visulization_type 
            SET a QUESTION as the TITLE of the plot.
            CHOOSE columns name for x axis and y axis.

            FOLLOW this output format instruction:

            {format_instruction}

            'visualization_type' can ONLY be within {list_of_graph}.

        """

        prompt ="""
            Given the summary of dataframe: {{summary}}
            Given description of each graph: {{graph_description}}

            {{user_prompt}}
        """

        prompt = PromptTemplate.from_template(prompt, template_format="jinja2")
        chain = prompt |  self.model | SimpleJsonOutputParser()
        question_result = chain.invoke({"summary": summary, "graph_description": graph_description, "user_prompt": user_prompt})

        return question_result

    #     system_prompt = """
    #         You are an experienced financial data analyst who can generate a given number of insightful QUESTIONS about data, when given a summary of the data. 
    #         Each question should refer to one visualization (THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), and a rationale (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). 
    #         Each question MUST mention the exact fields from the dataset summary above
    #         The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities) AND BE MEANINGFUL 
    #         (e.g., plot longitude and latitude on maps where appropriate). 
    #         MAKE SURE THE QUESTION IS A FINANCIAL/Economic QUESTION INSTEAD OF A STATISTIC QUESTION.`
    #     """

    #     format_instruction = """
    #         THE OUTPUT MUST BE A CODE SNIPPET OF A VALID LIST OF JSON OBJECTS. IT MUST USE THE FOLLOWING FORMAT:

    #         ```
    #         [
    #             { "index": 0,  "question": "How", "visualization": "histogram of X", "rationale": "This tells about "},
    #         ]
    #         ```
    #         THE OUTPUT SHOULD ONLY USE THE JSON FORMAT ABOVE.
    #     """

    #     user_prompt = f"""
    #         The number of QUESTIONS to generate is {num_goals}. The questions should be based on the data summary below, \n\n .
    #         {summary} \n\n

    #         MAKE SURE THE QUESTION IS A FINANCIAL/Economic QUESTION INSTEAD OF A STATISTIC QUESTION.
    #     """

    #     message = f"{user_prompt}\n\n {format_instruction} \n\n. The generated {num_goals} goals are: \n "

    #     return json.loads(generateLLMResponse(system_prompt, message))
        

        

if __name__ == "__main__":

    question_formulator = QuestionFormulator()
    summary = {'dataset_description': 'This dataset contains monthly inflation rates and price indices for various categories', 'fields': [{'column': 'Date', 'properties': {'dtype': 'date', 'min': '2022-09-01', 'max': '2023-09-01', 'num_unique_values': 13, 'samples': ['2022-09-01', '2022-10-01', '2022-11-01'], 'semantic_type': 'date', 'description': 'The date of the recorded data'}}, {'column': 'All-items', 'properties': {'dtype': 'number', 'min': 152.7, 'max': 158.7, 'num_unique_values': 13, 'samples': [152.7, 153.8, 154.0], 'semantic_type': 'number', 'description': 'The price index for all items'}}, {'column': 'Food 5', 'properties': {'dtype': 'number', 'min': 174.8, 'max': 185.5, 'num_unique_values': 13, 'samples': [174.8, 175.2, 177.3], 'semantic_type': 'number', 'description': 'The price index for food'}}, {'column': 'Shelter 6', 'properties': {'dtype': 'number', 'min': 164.9, 'max': 174.8, 'num_unique_values': 13, 'samples': [164.9, 166.2, 167.2], 'semantic_type': 'number', 'description': 'The price index for shelter'}}, {'column': 'Household operations, furnishings and equipment', 'properties': {'dtype': 'number', 'min': 131.3, 'max': 133.7, 'num_unique_values': 11, 'samples': [132.7, 132.9, 131.9], 'semantic_type': 'number', 'description': 'The price index for household operations, furnishings, and equipment'}}, {'column': 'Clothing and footwear', 'properties': {'dtype': 'number', 'min': 93.8, 'max': 97.9, 'num_unique_values': 12, 'samples': [96.1, 97.7, 97.3], 'semantic_type': 'number', 'description': 'The price index for clothing and footwear'}}, {'column': 'Transportation', 'properties': {'dtype': 'number', 'min': 164.2, 'max': 173.6, 'num_unique_values': 13, 'samples': [166.5, 170.1, 168.6], 'semantic_type': 'number', 'description': 'The price index for transportation'}}, {'column': 'Gasoline', 'properties': {'dtype': 'number', 'min': 208.3, 'max': 248.6, 'num_unique_values': 13, 'samples': [227.6, 248.6, 239.6], 'semantic_type': 'number', 'description': 'The price index for gasoline'}}, {'column': 'Health and personal care', 'properties': {'dtype': 'number', 'min': 139.6, 'max': 147.4, 'num_unique_values': 12, 'samples': [139.6, 140.4, 141.5], 'semantic_type': 'number', 'description': 'The price index for health and personal care'}}, {'column': 'Recreation, education and reading', 'properties': {'dtype': 'number', 'min': 121.7, 'max': 129.4, 'num_unique_values': 13, 'samples': [125.2, 125.0, 123.4], 'semantic_type': 'number', 'description': 'The price index for recreation, education, and reading'}}, {'column': 'Alcoholic beverages, tobacco products and recreational cannabis', 'properties': {'dtype': 'number', 'min': 182.4, 'max': 192.0, 'num_unique_values': 13, 'samples': [182.4, 183.5, 184.5], 'semantic_type': 'number', 'description': 'The price index for alcoholic beverages, tobacco products, and recreational cannabis'}}, {'column': 'All-items excluding food and energy 7', 'properties': {'dtype': 'number', 'min': 143.6, 'max': 148.3, 'num_unique_values': 12, 'samples': [143.6, 144.1, 144.2], 'semantic_type': 'number', 'description': 'The price index for all items excluding food and energy'}}, {'column': 'All-items excluding energy 7', 'properties': {'dtype': 'number', 'min': 148.9, 'max': 154.5, 'num_unique_values': 13, 'samples': [148.9, 149.4, 149.8], 'semantic_type': 'number', 'description': 'The price index for all items excluding energy'}}, {'column': 'Energy 7', 'properties': {'dtype': 'number', 'min': 197.7, 'max': 218.4, 'num_unique_values': 13, 'samples': [205.1, 217.9, 214.6], 'semantic_type': 'number', 'description': 'The price index for energy'}}, {'column': 'Goods 8', 'properties': {'dtype': 'number', 'min': 139.8, 'max': 145.6, 'num_unique_values': 13, 'samples': [140.2, 141.9, 142.2], 'semantic_type': 'number', 'description': 'The price index for goods'}}, {'column': 'Services 9', 'properties': {'dtype': 'number', 'min': 164.8, 'max': 171.3, 'num_unique_values': 12, 'samples': [164.8, 165.2, 165.5], 'semantic_type': 'number', 'description': 'The price index for services'}}, {'column': 'Inflation rate', 'properties': {'dtype': 'number', 'min': -0.5844155844155874, 'max': 0.7203667321545648, 'num_unique_values': 12, 'samples': [0.7203667321545648, 0.13003901170349774, -0.5844155844155874], 'semantic_type': 'number', 'description': 'The monthly inflation rate'}}, {'column': 'Core inflation rate', 'properties': {'dtype': 'number', 'min': -0.1386962552010984, 'max': 0.6206896551724128, 'num_unique_values': 12, 'samples': [0.3481894150417775, 0.0693962526023606, -0.1386962552010984], 'semantic_type': 'number', 'description': 'The core inflation rate excluding food and energy'}}, {'column': 'Price index for specific categories', 'properties': {'dtype': 'number', 'min': 771.0000000000001, 'max': 808.3, 'num_unique_values': 13, 'samples': [771.0000000000001, 776.9, 778.0], 'semantic_type': 'number', 'description': 'The price index for specific categories'}}]}
    print(question_formulator.formulate_question(summary, "Economic Dataset",1))