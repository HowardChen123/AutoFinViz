from autofinviz.components.classifier import Classifier
from autofinviz.components.summarizer import Summarizer
from autofinviz.components.question import QuestionFormulator
from autofinviz.components.visualizer import Visualizer

import pandas as pd

class Pipeline(object):
    def __init__(self):
        """
        Initialize the Pipeline
        """
        self.classifier = Classifier()
        self.summarizer = Summarizer()
        self.question_formulator = QuestionFormulator()
        self.visualizer = Visualizer()
        
        self.data = None

    def classify(self, df):
        return self.classifier.classify(df)

    def summarize(self, df, df_name, category):
        return self.summarizer.summarize(df, df_name, category)

    def formulate_questions(self, summary, category, num_goals):
        return self.question_formulator.formulate_question(summary, category, num_goals)
    
    def visualize(self, questions, df):
        return self.visualizer.visualize(questions, df)
    

if __name__ == "__main__":

    pipline = Pipeline()

    ## Market Dataset Example
    df = pd.read_csv("example/data/Stock_price_TSLA.csv")
    df_name = "Stock_price_TSLA"

    # ## Economic Dataset Example
    # df = pd.read_csv("example/data/Consumer_price_index.csv")
    # df_name = "Consumer_price_index"

    # ## Corporate Financial Dataset Example
    # df = pd.read_csv("example/data/Income_statement.csv")
    # ## Our system cannot handle too many dimension dataset
    # df.drop(columns=df.columns[-15:], inplace = True)
    # df_name = "Income_statement"

    print("Classification")
    category = pipline.classify(df)
    print(category)
    print("\n")

    print("Summarization")
    summary, df = pipline.summarize(df, df_name, category)
    print(summary)
    print("\n")

    print("Question Formulation")
    questions = pipline.formulate_questions(summary, category, 3)
    print(questions)
    print("\n")

    print("Visualization")
    visualizer_results = pipline.visualize(questions, df)
    print("\n")

    print("Result")
    print(visualizer_results)
    print(len(visualizer_results))
    