import os
import pandas as pd
import pickle
from django.conf import settings
from sklearn import linear_model
from sklearn.metrics import accuracy_score

from ml import clean as inverse_label
from ml.extractpdf import ResumeParser
from sklearn.model_selection import train_test_split


def check_type(data):
    if type(data) == str or type(data) == str:
        return str(data).title()
    if type(data) == list or type(data) == tuple:
        str_list = ""
        for i, item in enumerate(data):
            str_list += item + ", "
        return str_list
    else:
        return str(data)


class TrainModel:

    _file = 'ml/training_dataset.md.csv'

    def train(self):
        data = pd.read_csv(self._file)
        array = data.values

        for i in range(len(array)):
            if array[i][0] == "Male":
                array[i][0] = 1
            else:
                array[i][0] = 0

        df = pd.DataFrame(array)

        maindf = df[[0, 1, 2, 3, 4, 5, 6]]
        mainarray = maindf.values

        temp = df[7]
        train_y = temp.values
        self.model = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=1000)
        self.model.fit(mainarray, train_y)

    def test(self, test_data):
        test_predict = list()
        for i in test_data:
            test_predict.append(int(i))
        y_pred = self.model.predict([test_predict])
        return y_pred

    def accuracy(self):
        data = pd.read_csv(self._file)
        data['Gender'] = data['Gender'].apply(lambda x: 1 if x == 'Male' else 0)

        # Split data into input and output variables
        x = data.drop('Personality (Class label)', axis=1)
        y = data['Personality (Class label)']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        y_pred = self.model.predict(x_test)

        # Calculate percent error
        percent_error = 100 * (1 - accuracy_score(y_test, y_pred))

        # Print the test set results
        print("Percent error: ", percent_error)


def prediction_result(model, aplcnt_name, cv_path, personality_values):
    """
    After applying a job
    """
    applicant_data = {"Candidate Name": aplcnt_name, "CV Location": cv_path}
    out = {**applicant_data}
    age = personality_values[1]

    print("\n############# Candidate Entered Data #############\n")
    print(applicant_data, personality_values)

    personality = model.test(personality_values).tolist()
    personality = inverse_label(personality, personality_values, hash=len(aplcnt_name))
    print("\n############# Predicted Personality #############\n")

    if personality:
        out['predicted_personality'] = personality
    else:
        out['predicted_personality'] = 'no results found'
    print(personality)
    data = ResumeParser(cv_path).get_extracted_data()
    data['name'] = aplcnt_name
    try:
        del data['name']
        if len(data['mobile_number']) < 10:
            del data['mobile_number']
    except Exception as e:
        pass
    out['extracted_data'] = data
    print("\n############# Resume Parsed Data #############\n")

    for key in data.keys():
        if data[key] is not None:
            print('{} : {}'.format(key, data[key]))
    return out


def load_trained_file():
    pickle_file = os.path.join(settings.BASE_DIR, 'ml', 'ml_model.pkl.bin')
    if not os.path.exists(pickle_file):
        _model = TrainModel()
        _model.train()
        _model.accuracy()
        with open(pickle_file, 'wb') as fp:
            pickle.dump(_model, fp)
    else:
        with open(pickle_file, 'rb') as fp:
            _model = pickle.load(fp)
    return _model


if __name__ == "__main__":
    model = load_trained_file()
    prediction_result(model, "Neha", './media/neharesume1i.pdf', personality_values=('Female', 22, 7, 4, 7, 3, 2))
