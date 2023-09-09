import os

import xgboost
import xgboost as xgb
import joblib
import numpy as np
from matplotlib import pyplot as plt
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

"""
    File thuc hien nhung chuc nang:
    - Train data su dung 3 mo hinh: Logistic Regression, Support Vector Machine, Extreme Gradient Boosting
    - Danh gia Feature importance
"""

def get_and_preprocess_data(data_name):
    f = open(os.path.dirname(os.path.abspath(__file__)) + "\\Dataset\\MLData\\" + data_name)
    data = np.genfromtxt(f, delimiter=',')
    X = data[:, 1:len(data[0])]
    y = np.array(data[:, 0], dtype=np.int32)

    # Standardize the feature data
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    # Train
    return train_test_split(X_std, y)


def create_model_logit(data_name):
    X_train, X_test, y_train, y_test = get_and_preprocess_data(data_name)
    model = LogisticRegression(penalty='l1', solver='liblinear')
    model.fit(X_train, y_train)
    joblib.dump(model, 'Model/logit.joblib')
    print(model.coef_)

    y_pred_train = model.predict(X_train)
    accuracy_train = accuracy_score(y_train, y_pred_train)
    print(f"Train Accuracy: {accuracy_train}")
    # Evaluate the accuracy of the model on the test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy}")


# Function to learn hyper parameter
def create_model_svm_grid_search(data_name):
    X_train, X_test, y_train, y_test = get_and_preprocess_data(data_name)
    print("Begin training:")

    # Define the parameter grid
    param_grid = {'C': np.arange(0.05, 1.05, .05), 'kernel': ['rbf'], 'gamma': np.arange(.05, 1.05, 0.05)}

    svm_model = SVC()
    grid_search = GridSearchCV(svm_model, param_grid, cv=5, verbose=2)
    grid_search.fit(X_train, y_train)
    print("Finished creating model")
    print("Best Parameter Grid:")
    print(grid_search.best_params_)
    # joblib.dump(grid_search, 'Model/svm_edit_2000.joblib')

    y_pred_train = grid_search.predict(X_train)
    accuracy_train = accuracy_score(y_train, y_pred_train)
    print(f"Train Accuracy: {accuracy_train}")
    # Evaluate the accuracy of the model on the test set
    y_pred = grid_search.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy}")



def create_model_svm(data_name, C=0.35, gamma=0.05, kernel='rbf'):
    X_train, X_test, y_train, y_test = get_and_preprocess_data(data_name)
    print("Begin training:")

    svm_model = SVC(C=C, kernel=kernel, gamma=gamma)
    svm_model.fit(X_train, y_train)
    print("Finished creating model")
    joblib.dump(svm_model, 'Model//' + data_name.split('.')[0] + '_svm.joblib')

    y_pred_train = svm_model.predict(X_train)
    accuracy_train = accuracy_score(y_train, y_pred_train)
    print(f"Train Accuracy: {accuracy_train}")
    # Evaluate the accuracy of the model on the test set
    y_pred = svm_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy}")


def create_model_xgboost(data_name):
    print("XGboost version:", xgboost.__version__)
    X_train, X_test, y_train, y_test = get_and_preprocess_data(data_name)
    xgb_classifier = xgb.XGBClassifier(
        # Regularize
        colsample_bylevel=0.3,      # 0.1 - 1
        colsample_bytree=0.45,      # 0.1 - 1
        subsample=0.8,              # 0.8 - 1
        max_depth=16,               # 2 - 30
        min_child_weight=100,       # [1, 5, 100]
        reg_alpha=4.01,             # [1, 4.01, 10, 100]
        reg_lambda=1,               # [1, 5.51, 10, 100]
        # Learn param
        booster='gbtree',
        learning_rate=0.07,
        n_estimators=150,
        objective='binary:logistic',
        eval_metric='logloss',
        use_label_encoder=False,
    )

    # Fit the classifier to the training data
    xgb_classifier.fit(X_train, y_train)

    print("Finished creating model")
    joblib.dump(xgb_classifier, 'Model//' + data_name.split('.')[0] + '_xgb.joblib')

    y_pred_train = xgb_classifier.predict(X_train)
    accuracy_train = accuracy_score(y_train, y_pred_train)
    print(f"Train Accuracy: {accuracy_train}")
    # Evaluate the accuracy of the model on the test set
    y_pred = xgb_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy}")


# Function to learn hyper parameter
def xgboost_tuning(data_name):
    X_train, X_test, y_train, y_test = get_and_preprocess_data(data_name)
    print("Begin training:")

    # Define the parameter grid
    param_grid = {
        'colsample_bylevel': [0.3, 0.45],  # 0.1 - 1
        'colsample_bytree': [0.3, 0.45],
        'subsample': [0.8, 0.9],
        'max_depth': [16, 20],
        'min_child_weight': [1, 5, 100],
        'reg_alpha': [1, 4.01, 100],
        'reg_lambda': [1, 5.51, 100],
    }


    xgb_classifier = xgb.XGBClassifier(
        booster='gbtree',
        learning_rate=0.07,
        n_estimators=150,
        objective='binary:logistic',
        eval_metric='logloss',
        use_label_encoder=False)

    grid_search = GridSearchCV(xgb_classifier, param_grid, cv=5, verbose=2)
    grid_search.fit(X_train, y_train)
    print("Finished creating model")
    print("Best Parameter Grid:")
    print(grid_search.best_params_)
    # joblib.dump(grid_search, 'Model/svm_edit_2000.joblib')

    y_pred_train = grid_search.predict(X_train)
    accuracy_train = accuracy_score(y_train, y_pred_train)
    print(f"Train Accuracy: {accuracy_train}")
    # Evaluate the accuracy of the model on the test set
    y_pred = grid_search.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {accuracy}")


def load_model(data_name, model_name):
    X_train, X_test, y_train, y_test = get_and_preprocess_data(data_name)
    model = joblib.load(os.path.dirname(os.path.abspath(__file__)) + "\\Model\\" + model_name)
    # print( model.get_booster().get_score(importance_type='weight'))
    # print(model.feature_importances_)
    # plot_importance(model)
    # pyplot.show()
    print(permutation_importance(model, X_test, y_test))
    y_pred_train = model.predict(X_train)
    y_pred = model.predict(X_test)
    accuracy_train = accuracy_score(y_train, y_pred_train)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Train Accuracy: {accuracy_train}")
    print(f"Test Accuracy: {accuracy}")


# Lazy stuff
def visual_svm():
    features = np.array(["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"])
    perm_importance = np.array([0.09732, 0.00981333, 0.00942667, 0.00937333, 0.05841333,
     0.00728, 0.00948, 0.00985333, 0.02553333, 0.00478667])
    sorted_idx = perm_importance.argsort()
    plt.barh(features[sorted_idx], perm_importance[sorted_idx])
    plt.xlabel("Permutation Importance using SVM")
    plt.show()


def visual_xgboost(data_name, model_name):
    X_train, X_test, y_train, y_test = get_and_preprocess_data(data_name)
    features = np.array(["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"])
    model = joblib.load(os.path.dirname(os.path.abspath(__file__)) + "\\Model\\" + model_name)
    perm_import = permutation_importance(model, X_test, y_test).importances_mean
    sorted_idx = perm_import.argsort()
    plt.barh(features[sorted_idx], perm_import[sorted_idx])
    plt.xlabel("Permutation Importance using Xgboost")
    plt.show()


def visual_logit(data_name, model_name):
    X_train, X_test, y_train, y_test = get_and_preprocess_data(data_name)
    features = np.array(["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"])
    model = joblib.load(os.path.dirname(os.path.abspath(__file__)) + "\\Model\\" + model_name)
    perm_import = permutation_importance(model, X_test, y_test).importances_mean
    sorted_idx = perm_import.argsort()
    plt.barh(features[sorted_idx], perm_import[sorted_idx])
    plt.xlabel("Permutation Importance using Logit")
    plt.show()



if __name__ == "__main__":
    # create_model_xgboost("CVRP_true.txt")
    # load_model("CVRP_true.txt", "CVRP_true_svm.joblib")
    # xgboost_tuning("CVRP.txt")

    visual_svm()
    # visual_xgboost("CVRP_true.txt", "CVRP_true_xgb.joblib")
    # visual_logit("CVRP_true.txt", "logit.joblib")

    # create_model_xgboost("CVRP.txt")
    # create_model_svm("CVRP_true.txt")
    # create_model_logit("CVRP_true.txt")
    # create_model_svm_grid_search("CVRP_N_2000.txt")


"""
    Original version (train with 2000 bigger instance):
    {'C': 0.35, 'gamma': 0.05, 'kernel': 'rbf'}
    Train Accuracy: 0.712762412529157
    Test Accuracy: 0.7202797202797203

    Adjust avg to min/max all (2000):
    Best Parameter Grid:
    {'C': 0.25, 'gamma': 0.05, 'kernel': 'rbf'}
    Train Accuracy: 0.692435854715095
    Test Accuracy: 0.6623376623376623

    SVM - CVRP:
    Train Accuracy: 0.6794393353769603
    Test Accuracy: 0.6827935492469679
    
    Parameter tuning:
    svm: Best known: {'C': 0.6 or 0.95, 'gamma': 0.1, 'kernel': 'rbf'}. Train Accuracy: 0.7464178607130957, Test Accuracy: 0.7042957042957043
    Xgboost: Best Parameter Grid: {'colsample_bytree': 0.3, 'learning_rate': 0.07999999999999999, 'max_depth': 20, 'n_estimators': 200, 'reg_alpha': 1.7000000000000002, 'reg_lambda': 2.9000000000000004}. Train Accuracy: 0.9956681106297901, Test Accuracy: 0.7092907092907093
  
  
    svm log:
    {'importances_mean': array([0.09732   , 0.00981333, 0.00942667, 0.00937333, 0.05841333,
           0.00728   , 0.00948   , 0.00985333, 0.02553333, 0.00478667]), 'importances_std': array([0.00245181, 0.00094789, 0.00084074, 0.00222974, 0.00135804,
           0.00127986, 0.00105696, 0.00107612, 0.00126139, 0.00085832]), 'importances': array([[0.0956    , 0.0964    , 0.09713333, 0.0954    , 0.10206667],
           [0.00813333, 0.01006667, 0.01106667, 0.01      , 0.0098    ],
           [0.00953333, 0.00966667, 0.01006667, 0.0078    , 0.01006667],
           [0.00666667, 0.01166667, 0.01233333, 0.00846667, 0.00773333],
           [0.05873333, 0.0604    , 0.059     , 0.05753333, 0.0564    ],
           [0.00686667, 0.0074    , 0.00573333, 0.0068    , 0.0096    ],
           [0.00906667, 0.00873333, 0.01013333, 0.0112    , 0.00826667],
           [0.00846667, 0.01013333, 0.01153333, 0.0102    , 0.00893333],
           [0.02593333, 0.0278    , 0.02506667, 0.02433333, 0.02453333],
           [0.00513333, 0.006     , 0.00346667, 0.00506667, 0.00426667]])}
"""
