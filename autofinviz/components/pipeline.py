from autofinviz.components.summarizer import Summarizer
from autofinviz.components.question import QuestionFormulator

class Pipeline(object):
    def __init__(self):
        """
        Initialize the Pipeline
        """

        self.summarizer = Summarizer()
        self.question_formulator = QuestionFormulator()
        
        self.data = None

    def summarize(self, df, df_name, category):
        return self.summarizer.summarize(df, df_name, category)

    def formulate_questions(self, summary, num_goals):
        return self.question_formulator.formulate_question(summary, num_goals)
