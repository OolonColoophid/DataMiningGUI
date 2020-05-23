from sklearn.model_selection import cross_val_score
import numpy as np


class Model:

    def __init__(self, mainframe, model):
        self.mainframe = mainframe
        self.model = model
        self.split_data_attributes_class()

    def set_model(self, model):
        self.model = model

    def split_data_attributes_class(self):
        df = self.mainframe.importExportDataManager.get_data()
        attributes = self.mainframe.importExportDataManager.get_column_names()
        class_label = self.mainframe.getSelectedClassLabel()
        attributes.remove(class_label)
        X = df[attributes]
        y = df[class_label]
        y = y.astype('category')
        self.X = X
        self.y = y

    def cross_validate(self, scoring):
        cv = self.mainframe.optionsWindow.settings.get("k-fold cross validation")
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
