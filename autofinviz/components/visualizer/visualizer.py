import pandas as pd

from autofinviz.utils import generateLLMResponse_viz, preprocess_code, get_globals_dict
# import seaborn as sns
# import matplotlib.pyplot as plt

class Visualizer():
    def __init__(self) -> None:
        pass

    def visualize(
        self, summary: list,
        questions: list,
        data: pd.DataFrame
    ):
        
        system_prompt = """
            You are a helpful assistant highly skilled in writing PERFECT code for visualizations. Given some code template, \
            you complete the template to generate a visualization given the dataset and the goal described. The code you write \
            MUST FOLLOW VISUALIZATION BEST PRACTICES ie. meet the specified goal, apply the right transformation, use the right \
            visualization type, use the right data encoding, and use the right aesthetics (e.g., ensure axis are legible). \
            The transformations you apply MUST be correct and the fields you use MUST be correct. \
            The visualization CODE MUST BE CORRECT and MUST NOT CONTAIN ANY SYNTAX OR LOGIC ERRORS \
            (e.g., it must consider the field types and use them correctly). You MUST first generate a \
            brief plan for how you would solve the task e.g. what transformations you would apply \
            e.g. if you need to construct a new column, what fields you would use, \
            what visualization type you would use, what aesthetics you would use, etc. .
        """

        for question_dict in questions:
            df = data.copy()
            visualization = question_dict["visualization"]
            question = question_dict["question"]

            general_instructions = f"If the solution requires a single value (e.g. max, min, median, first, last etc), ALWAYS add a line (axvline or axhline) \
                to the chart, ALWAYS with a legend containing the single value (formatted with 0.2F). \If using a <field> where semantic_type=date, \
                YOU MUST APPLY the following transform before using that column i) convert date fields to date types \
                using df[''] = pd.to_datetime(df[<field>], errors='coerce'), ALWAYS use errors='coerce' ii) \
                drop the rows with NaT values df = df[pd.notna(df[<field>])] iii) convert field to right time format for plotting. \
                ALWAYS make sure the x-axis labels are legible (e.g., rotate when needed). Solve the task carefully by completing ONLY \
                the <imports> AND <stub> section. Given the dataset summary, the plot(df) method should generate a seaborn chart ({visualization}) \
                that addresses this goal: {question}. DO NOT WRITE ANY CODE TO LOAD THE DATA. The data is already loaded and available in the variable data."
                
            instructions = {
            "role": "assistant",
            "content": f"{general_instructions}"}

            template = \
                """
            import seaborn as sns
            import pandas as pd
            import matplotlib.pyplot as plt
            # Additional imports can be added here if necessary
            <additional_imports>

            # Solution Plan:
            # 1. Describe the first step...
            # 2. Describe the next step...
            # ... continue as needed

            def plot(df: pd.DataFrame):
                # The following section is for custom plotting logic.
                # Modify only within this area.
                <plotting_stub>
                
                # Set the title of the plot. Modify title as needed.
                plt.title(f'{question}', wrap=True)
                
                # Return the plot object
                return plt

            # Dataframe 'df' already contains the data to be plotted.
            # No modifications needed below this line.
            chart = plot(df)
            chart.savefig(f'example/figures/{question}.png')
            """

            messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"The dataset summary is : {summary} \n\n"},
            instructions,
            {"role": "user",
             "content":
             f"Always add a legend with various colors where appropriate. The visualization code MUST only use data fields that exist in the dataset \
                (field_names) or fields that are transformations based on existing field_names). Only use variables that have been defined in the code \
                or are in the dataset summary. You MUST return a FULL PYTHON PROGRAM ENCLOSED IN BACKTICKS ``` that starts with an import statement. \
                DO NOT add any explanation. \n\n THE GENERATED CODE SOLUTION SHOULD BE CREATED BY MODIFYING THE SPECIFIED PARTS OF THE TEMPLATE BELOW: \n\n \
                {template} \n\n. The FINAL COMPLETED CODE BASED ON THE TEMPLATE above is ..."}]

            code = generateLLMResponse_viz(messages)

            code = preprocess_code(code)

            print(code)

            try:
                ex_locals = get_globals_dict(code, df)
                exec(code, ex_locals)
            except Exception as e:
                print(f"An error occurred: {e}")




        







