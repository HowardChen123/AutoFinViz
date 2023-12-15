from autofinviz.utils import generateLLMResponse
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser

class QuestionFormulator():
    def __init__(self, model="gpt-3.5-turbo") -> None:
        self.model = ChatOpenAI(model_name=model)

    def formulate_question(self, summary, num_goals=5):

        list_of_graph = ["OHLC Chart", "Candlestick Chart", "Moving Average Graph", "RSI Graph", "Moving Average Convergence Divergence",
            "Waterfall Chart", "Funnel Chart", "Time Series graph with a range slider","Multi-Measurment Time Series Graph", ]

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
    summary = {'dataset_description': '', 'fields': [{'column': 'Date', 'properties': {'dtype': 'date', 'min': '2022-11-21', 'max': '2023-11-17', 'num_unique_values': 250, 'samples': ['2022-11-21', '2022-11-22', '2022-11-23'], 'semantic_type': '', 'description': ''}}]}
    print(question_formulator.formulate_question(summary, 1))