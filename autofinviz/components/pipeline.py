from autofinviz.components.classifier import Classifier
from autofinviz.components.summarizer import Summarizer
from autofinviz.components.question import QuestionFormulator
from autofinviz.components.viz import Viz

class Pipeline(object):
    def __init__(self):
        """
        Initialize the Pipeline
        """
        self.classifier = Classifier()
        self.summarizer = Summarizer()
        self.question_formulator = QuestionFormulator()
        self.viz = Viz()
        
        self.data = None

    def classify(self, df):
        return self.classifier.classify(df)

    def summarize(self, df, df_name, category):
        return self.summarizer.summarize(df, df_name, category)

    def formulate_questions(self, summary, num_goals):
        return self.question_formulator.formulate_question(summary, num_goals)
    
    def visualize(self, summary, questions):
        return self.viz.visualize(summary, questions)
