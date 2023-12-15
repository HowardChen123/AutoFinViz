from autofinviz.components.classifier import Classifier
from autofinviz.components.summarizer import Summarizer
from autofinviz.components.question import QuestionFormulator
from autofinviz.components.visualizer import Visualizer

import time

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

    def formulate_questions(self, summary, num_goals):
        return self.question_formulator.formulate_question(summary, num_goals)
    
    def visualize(self, questions, df):
        return self.visualizer.visualize(questions, df)
    

if __name__ == "__main__":

    pipline = Pipeline()

    df = pd.read_csv("example/data/Stock_price_TSLA.csv")
    df_name = "Stock_price_TSLA"

    category = pipline.classify(df)
    print(category)

    summary, df = pipline.summarize(df, df_name, category)
    print(summary)

    questions = pipline.formulate_questions(summary, 3)
    print(questions)

    visualizer_results = pipline.visualize(questions, df)

    print("Reuslt")
    print(visualizer_results)
    