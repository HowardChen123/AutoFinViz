from autofinviz.utils import generateLLMResponse
import json

class QuestionFormulator():
    def __init__(self) -> None:
        pass

    def formulate_question(self, summary, num_goals=5):
        system_prompt = """
            You are an experienced financial data analyst who can generate a given number of insightful QUESTIONS about data, when given a summary of the data. 
            Each question should refer to one visualization (THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), and a rationale (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). 
            Each question MUST mention the exact fields from the dataset summary above
            The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities) AND BE MEANINGFUL 
            (e.g., plot longitude and latitude on maps where appropriate). 
            MAKE SURE THE QUESTION IS A FINANCIAL/Economic QUESTION INSTEAD OF A STATISTIC QUESTION.`
        """

        format_instruction = """
            THE OUTPUT MUST BE A CODE SNIPPET OF A VALID LIST OF JSON OBJECTS. IT MUST USE THE FOLLOWING FORMAT:

            ```
            [
                { "index": 0,  "question": "How", "visualization": "histogram of X", "rationale": "This tells about "},
                { "index": 1,  "question": "How", "visualization": "lineplot of X", "rationale": "This tells about "}, ..
            ]
            ```
            THE OUTPUT SHOULD ONLY USE THE JSON FORMAT ABOVE.
        """

        user_prompt = f"""
            The number of QUESTIONS to generate is {num_goals}. The questions should be based on the data summary below, \n\n .
            {summary} \n\n

            MAKE SURE THE QUESTION IS A FINANCIAL/Economic QUESTION INSTEAD OF A STATISTIC QUESTION.
        """

        message = f"{user_prompt}\n\n {format_instruction} \n\n. The generated {num_goals} goals are: \n "

        return json.loads(generateLLMResponse(system_prompt, message))


if __name__ == "__main__":

    question_formulator = QuestionFormulator()
    summary = {'dataset_description': '', 'fields': [{'column': 'Date', 'properties': {'dtype': 'date', 'min': '2022-11-21', 'max': '2023-11-17', 'num_unique_values': 250, 'samples': ['2022-11-21', '2022-11-22', '2022-11-23'], 'semantic_type': '', 'description': ''}}]}
    print(question_formulator.formulate_question(summary, 1))