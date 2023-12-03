import pandas as pd

from autofinviz.utils import generateLLMResponse_viz, preprocess_code

class Viz():
    def __init__(self) -> None:
        pass

    def visualize(
        self, summary: list,
        questions: list,    
    ):
        
        system_prompt = """
        You are a helpful assistant highly skilled in writing PERFECT code for visualizations. Given some code template, you complete the template to generate a visualization given the dataset and the goal described. The code you write MUST FOLLOW VISUALIZATION BEST PRACTICES ie. meet the specified goal, apply the right transformation, use the right visualization type, use the right data encoding, and use the right aesthetics (e.g., ensure axis are legible). The transformations you apply MUST be correct and the fields you use MUST be correct. The visualization CODE MUST BE CORRECT and MUST NOT CONTAIN ANY SYNTAX OR LOGIC ERRORS (e.g., it must consider the field types and use them correctly). You MUST first generate a brief plan for how you would solve the task e.g. what transformations you would apply e.g. if you need to construct a new column, what fields you would use, what visualization type you would use, what aesthetics you would use, etc. .
        """

        for question in questions:

            general_instructions = f"If the solution requires a single value (e.g. max, min, median, first, last etc), ALWAYS add a line (axvline or axhline) to the chart, ALWAYS with a legend containing the single value (formatted with 0.2F). If using a <field> where semantic_type=date, YOU MUST APPLY the following transform before using that column i) convert date fields to date types using data[''] = pd.to_datetime(data[<field>], errors='coerce'), ALWAYS use  errors='coerce' ii) drop the rows with NaT values data = data[pd.notna(data[<field>])] iii) convert field to right time format for plotting.  ALWAYS make sure the x-axis labels are legible (e.g., rotate when needed). Solve the task  carefully by completing ONLY the <imports> AND <stub> section. Given the dataset summary, the plot(data) method should generate a seaborn chart ({visualization}) that addresses this goal: {question}. DO NOT WRITE ANY CODE TO LOAD THE DATA. The data is already loaded and available in the variable data."

            matplotlib_instructions = f" {general_instructions} DO NOT include plt.show(). The plot method must return a matplotlib object (plt). Think step by step. \n"

            instructions = {
            "role": "assistant",
            "content": f"{matplotlib_instructions}. Use BaseMap for charts that require a map. "}

            template = \
                f"""
            import seaborn as sns
            import pandas as pd
            import matplotlib.pyplot as plt
            <imports>
            # solution plan
            # i.  ..
            def plot(df: pd.DataFrame):

                <stub> # only modify this section
                plt.title('{question}', wrap=True)
                return plt;

            chart = plot(df) # data already contains the data to be plotted. Always include this line. No additional code beyond this line."""

            messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"The dataset summary is : {summary} \n\n"},
            instructions,
            {"role": "user",
             "content":
             f"Always add a legend with various colors where appropriate. The visualization code MUST only use data fields that exist in the dataset (field_names) or fields that are transformations based on existing field_names). Only use variables that have been defined in the code or are in the dataset summary. You MUST return a FULL PYTHON PROGRAM ENCLOSED IN BACKTICKS ``` that starts with an import statement. DO NOT add any explanation. \n\n THE GENERATED CODE SOLUTION SHOULD BE CREATED BY MODIFYING THE SPECIFIED PARTS OF THE TEMPLATE BELOW \n\n {template} \n\n.The FINAL COMPLETED CODE BASED ON THE TEMPLATE above is ... \n\nBe aware of the following error, i.e. ValueError: Multi-dimensional indexing (e.g. `obj[:, None]`) is no longer supported. Convert to a numpy array before indexing instead."}]

            code = generateLLMResponse_viz(messages)

            code = preprocess_code(code)

            try:
                exec(code)
            except Exception as e:
                print(f"An error occurred: {e}")


            




        







