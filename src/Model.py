import io
from tkinter import messagebox
from tkinter.filedialog import askdirectory

import matplotlib.pyplot as plt
import pandas as pd
import pydotplus as pydotplus
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import export_graphviz, DecisionTreeClassifier


class Model:

    def __init__(self, mainframe, model, dataframe):
        self.mainframe = mainframe
        self.model = model
        self.dataframe = dataframe
        self.X, self.y = self.split_data_attributes_class()

    def set_model(self, model):
        self.model = model

    def split_data_attributes_class(self):
        attributes = list(self.dataframe.columns)
        class_label = self.mainframe.getSelectedClassLabel()
        attributes.remove(class_label)
        X = self.dataframe[attributes]
        y = self.dataframe[class_label]
        y = self.map_class_labels(y)
        y = y.astype('category')
        return X, y

    def map_class_labels(self, column):
        if isinstance(column, pd.Series):
            if column.dtype == "object":
                unique_values = column.unique()
                mapping = {label: idx for idx, label in enumerate(unique_values)}
                column = column.map(mapping)
        return column

    def optimize_model_hyperparams(self, model):

        global param_grid
        print("Optimizing hyperparameters...")
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3)
        if isinstance(model, DecisionTreeClassifier):
            param_grid = {'criterion': ['gini', 'entropy'],
                          'splitter': ['best', 'random'],
                          'max_depth': [2, 3, 5, 7],
                          'min_samples_split': [10, 20, 50, 100],
                          'min_samples_leaf': [5, 10, 20, 50],
                          'max_leaf_nodes': [2, 5, 10, 20]}
        elif isinstance(model, LogisticRegression):
            param_grid = {'penalty': ['l2'],
                          'tol': [0.0001, 0.001, 0.01, 0.1],
                          'C': [0.001, 0.01, 0.1, 1, 10],
                          'solver': ['lbfgs', 'liblinear'],
                          'max_iter': [1000]}
        elif isinstance(model, GaussianNB):
            param_grid = {'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6]}
        gs = GridSearchCV(estimator=model,
                          param_grid=param_grid,
                          scoring='accuracy',
                          cv=int(self.mainframe.optionsWindow.settings.get("k-fold cross validation")),
                          n_jobs=1)
        gs = gs.fit(X_train, y_train)
        print(gs.best_estimator_)
        self.model = gs.best_estimator_

    def cross_validate(self, scoring):
        cv = int(self.mainframe.optionsWindow.settings.get("k-fold cross validation"))
        score = cross_val_score(self.model, self.X, self.y,
                                scoring=scoring, cv=cv, n_jobs=1)
        score_mean, score_std = np.mean(score), np.std(score)
        return score_mean, score_std

    def get_performance(self):
        accuracy_mean, accuracy_std = self.cross_validate('accuracy')
        precision_mean, precision_std = self.cross_validate('precision')
        recall_mean, recall_std = self.cross_validate('recall')
        f_one = 2 * ((precision_mean * recall_mean) / (precision_mean + recall_mean))
        performance = {"name": self.model,
                       "f_one": f_one,
                       "accuracy mean": accuracy_mean,
                       "accuracy std": accuracy_std,
                       "precision mean": precision_mean,
                       "precision std": precision_std,
                       "recall mean": recall_mean,
                       "recall std": recall_std}

        return performance

    def performance_summary(self):
        perf = self.get_performance()
        print("Classifier: %s" % (perf.get("name")))
        print("Accuracy: %.3f +/- %.3f" % (perf.get("accuracy mean"), perf.get("accuracy std")))
        print("Precision: %.3f +/- %.3f" % (perf.get("precision mean"), perf.get("precision std")))
        print("Recall: %.3f +/- %.3f" % (perf.get("recall mean"), perf.get("recall std")))
        print("F1 score: %.3f" % (perf.get("f_one")))
        if isinstance(self.model, DecisionTreeClassifier):
            self.model.fit(self.X, self.y)
            self.draw_tree(self.model, "test")
            self.show_tree()

    def draw_tree(self, tree, file):
        if isinstance(self.model, DecisionTreeClassifier):
            messageBox = messagebox.askquestion("Save figure", "Would you like to save the constructed decision tree?")
            if messageBox == 'yes':
                try:
                    f = io.StringIO()
                    directory = askdirectory()
                    export_graphviz(tree,
                                    out_file=f,
                                    feature_names=self.X.columns,
                                    class_names=list(self.mainframe.importExportDataManager.class_labels.keys()),
                                    filled=True)
                    pydotplus.graph_from_dot_data(f.getvalue()).write_png(directory + "\\" + file + ".png")
                except IOError:
                    messageBox = messageBox.showinfo("File not found", "Warning: could not find directory")

    def show_tree(self):
        plt.figure()
        sklearn.tree.plot_tree(self.model,
                               feature_names=self.X.columns,
                               class_names=list(self.mainframe.importExportDataManager.class_labels.keys()))
        plt.title("Decision tree")
        plt.show()
