import pandas as pd


class Student():
    def __init__(self, rut, name, major, math_grade, language_grade, english_grade):
        self.rut = rut
        self.name = name
        self.major = major
        self.mean_math_grade = math_grade
        self.mean_language_grade = language_grade
        self.mean_english_grade = english_grade
        self.math_performance = self.performance_indicator(self.mean_math_grade)
        self.languaje_performance = self.performance_indicator(self.mean_language_grade)
        self.english_performance = self.performance_indicator(self.mean_english_grade)

    def performance_indicator(self, grade):
        # Verificar si el valor es NaN o None
        if pd.isna(grade):
            return "No hay datos"
        if grade >= 45.0:
            return "Good"
        elif 40.0 <= grade < 45.0:
            return "At risk"
        else:
            return "Bad"