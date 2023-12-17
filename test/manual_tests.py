import config
import pandas as pd
from autofinviz.components.classifier import Classifier
from autofinviz.components.summarizer import Summarizer
from autofinviz.components.question import QuestionFormulator
from autofinviz.components.visualizer import Visualizer

def test_classifier():
    classifier = Classifier()

    df = pd.read_csv("example/data/Stock_price_TSLA.csv")

    category = classifier.classify(df)
    print(category)

def test_summarizer():
    summarizer = Summarizer()

    df = pd.read_csv("example/data/Stock_price_TSLA.csv")
    df_name = "Stock_price_TSLA"
    category = "Market Dataset"

    summary, df = summarizer.summarize(df, df_name, category)
    print(summary)

def test_question_formulator():
    question_formulator = QuestionFormulator()
    summary = {'dataset_description': 'This dataset contains monthly inflation rates and price indices for various categories', 'fields': [{'column': 'Date', 'properties': {'dtype': 'date', 'min': '2022-09-01', 'max': '2023-09-01', 'num_unique_values': 13, 'samples': ['2022-09-01', '2022-10-01', '2022-11-01'], 'semantic_type': 'date', 'description': 'The date of the recorded data'}}, {'column': 'All-items', 'properties': {'dtype': 'number', 'min': 152.7, 'max': 158.7, 'num_unique_values': 13, 'samples': [152.7, 153.8, 154.0], 'semantic_type': 'number', 'description': 'The price index for all items'}}, {'column': 'Food 5', 'properties': {'dtype': 'number', 'min': 174.8, 'max': 185.5, 'num_unique_values': 13, 'samples': [174.8, 175.2, 177.3], 'semantic_type': 'number', 'description': 'The price index for food'}}, {'column': 'Shelter 6', 'properties': {'dtype': 'number', 'min': 164.9, 'max': 174.8, 'num_unique_values': 13, 'samples': [164.9, 166.2, 167.2], 'semantic_type': 'number', 'description': 'The price index for shelter'}}, {'column': 'Household operations, furnishings and equipment', 'properties': {'dtype': 'number', 'min': 131.3, 'max': 133.7, 'num_unique_values': 11, 'samples': [132.7, 132.9, 131.9], 'semantic_type': 'number', 'description': 'The price index for household operations, furnishings, and equipment'}}, {'column': 'Clothing and footwear', 'properties': {'dtype': 'number', 'min': 93.8, 'max': 97.9, 'num_unique_values': 12, 'samples': [96.1, 97.7, 97.3], 'semantic_type': 'number', 'description': 'The price index for clothing and footwear'}}, {'column': 'Transportation', 'properties': {'dtype': 'number', 'min': 164.2, 'max': 173.6, 'num_unique_values': 13, 'samples': [166.5, 170.1, 168.6], 'semantic_type': 'number', 'description': 'The price index for transportation'}}, {'column': 'Gasoline', 'properties': {'dtype': 'number', 'min': 208.3, 'max': 248.6, 'num_unique_values': 13, 'samples': [227.6, 248.6, 239.6], 'semantic_type': 'number', 'description': 'The price index for gasoline'}}, {'column': 'Health and personal care', 'properties': {'dtype': 'number', 'min': 139.6, 'max': 147.4, 'num_unique_values': 12, 'samples': [139.6, 140.4, 141.5], 'semantic_type': 'number', 'description': 'The price index for health and personal care'}}, {'column': 'Recreation, education and reading', 'properties': {'dtype': 'number', 'min': 121.7, 'max': 129.4, 'num_unique_values': 13, 'samples': [125.2, 125.0, 123.4], 'semantic_type': 'number', 'description': 'The price index for recreation, education, and reading'}}, {'column': 'Alcoholic beverages, tobacco products and recreational cannabis', 'properties': {'dtype': 'number', 'min': 182.4, 'max': 192.0, 'num_unique_values': 13, 'samples': [182.4, 183.5, 184.5], 'semantic_type': 'number', 'description': 'The price index for alcoholic beverages, tobacco products, and recreational cannabis'}}, {'column': 'All-items excluding food and energy 7', 'properties': {'dtype': 'number', 'min': 143.6, 'max': 148.3, 'num_unique_values': 12, 'samples': [143.6, 144.1, 144.2], 'semantic_type': 'number', 'description': 'The price index for all items excluding food and energy'}}, {'column': 'All-items excluding energy 7', 'properties': {'dtype': 'number', 'min': 148.9, 'max': 154.5, 'num_unique_values': 13, 'samples': [148.9, 149.4, 149.8], 'semantic_type': 'number', 'description': 'The price index for all items excluding energy'}}, {'column': 'Energy 7', 'properties': {'dtype': 'number', 'min': 197.7, 'max': 218.4, 'num_unique_values': 13, 'samples': [205.1, 217.9, 214.6], 'semantic_type': 'number', 'description': 'The price index for energy'}}, {'column': 'Goods 8', 'properties': {'dtype': 'number', 'min': 139.8, 'max': 145.6, 'num_unique_values': 13, 'samples': [140.2, 141.9, 142.2], 'semantic_type': 'number', 'description': 'The price index for goods'}}, {'column': 'Services 9', 'properties': {'dtype': 'number', 'min': 164.8, 'max': 171.3, 'num_unique_values': 12, 'samples': [164.8, 165.2, 165.5], 'semantic_type': 'number', 'description': 'The price index for services'}}, {'column': 'Inflation rate', 'properties': {'dtype': 'number', 'min': -0.5844155844155874, 'max': 0.7203667321545648, 'num_unique_values': 12, 'samples': [0.7203667321545648, 0.13003901170349774, -0.5844155844155874], 'semantic_type': 'number', 'description': 'The monthly inflation rate'}}, {'column': 'Core inflation rate', 'properties': {'dtype': 'number', 'min': -0.1386962552010984, 'max': 0.6206896551724128, 'num_unique_values': 12, 'samples': [0.3481894150417775, 0.0693962526023606, -0.1386962552010984], 'semantic_type': 'number', 'description': 'The core inflation rate excluding food and energy'}}, {'column': 'Price index for specific categories', 'properties': {'dtype': 'number', 'min': 771.0000000000001, 'max': 808.3, 'num_unique_values': 13, 'samples': [771.0000000000001, 776.9, 778.0], 'semantic_type': 'number', 'description': 'The price index for specific categories'}}]}
    print(question_formulator.formulate_question(summary, "Economic Dataset",3))

def test_visualizer():
    visualizer = Visualizer()
    questions = [{'index': 0, 'title': 'Monthly Inflation Rates for Various Categories', 'visualization_type': 'Time Series graph with a range slider', 'x_axis': ['Date'], 'y_axis': ['Inflation rate', 'Core inflation rate']}]
    df = pd.read_csv("example/data/Consumer_price_index.csv")

    visualizer.visualize(questions, df)