import pandas as pd
import datetime
import random
import time
import numpy as np
import collections
import pickle
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

def neural_train(data, target):
  V, V_test, Z, Z_test = train_test_split(data, target, test_size=0.3, random_state = 1)
  
  scaler = preprocessing.StandardScaler()
  #Fit only over test data
  scaler.fit(V)
  V = scaler.transform(V)
  V_test = scaler.transform(V_test)

  random.seed = time.time()
  max_acc = -1
  best_mlp = None
  max_pre = -1

  for i in range(50):
    # mlp = MLPClassifier(solver='adam', alpha=0.0002, learning_rate_init=0.00001, max_iter=500, early_stopping=True, hidden_layer_sizes=(55, ), activation='tanh', random_state=1)
    mlp = MLPClassifier(solver='lbfgs', alpha=0.0002, learning_rate_init=0.00001, max_iter=500, early_stopping=True, hidden_layer_sizes=(30, ), activation='tanh', random_state=1)
    # mlp = MLPClassifier(solver='sgd', alpha=0.0002, learning_rate_init=0.00001, max_iter=500, early_stopping=True, hidden_layer_sizes=(55, ), activation='tanh', random_state=1)

    mlp.fit(V, Z)

    Z_predict = mlp.predict(V_test)

    acc = accuracy_score(Z_test, Z_predict)
#    print(f"Accuracy Score: {acc}")

    pre = precision_score(Z_test, Z_predict)
#    print(f"Precision Score: {pre}")

#    print("Confusion Matrix:")
#    print(confusion_matrix(Z_test, Z_predict))

    if acc > max_acc:
      max_acc = acc
      best_mlp = mlp
    
    if pre > max_pre:
      max_pre = pre


  #print(f"Max acc: {max_acc}")
  #print(f"Max pre: {max_pre}")
  #Print result analise
  print(f"Len V Test: {len(V_test)}")
  print(f"Len Z Test: {len(Z_test)}")
  print(f"Len V: {len(V)}")
  print(f"Len Z: {len(Z)}")

  print("####### Best MLP Results #######")
  Z_predict = best_mlp.predict(V_test)
  accuracy = accuracy_score(Z_test, Z_predict)
  print(f"MLP Accuracy Score: {accuracy_score(Z_test, Z_predict)}\n")
  precision = precision_score(Z_test, Z_predict)
  print(f"MLP Precision Score: {precision}\n")
  recall = recall_score(Z_test, Z_predict)
  print(f"MLP Recall Score: {recall}\n")
  f1 = f1_score(Z_test, Z_predict)
  print(f"MLP F1 Score: {f1}\n")
  cm = confusion_matrix(Z_test, Z_predict)
  print('\n\n')

  # Random Forest
  rf = RandomForestClassifier(n_estimators=1000)
  rf.fit(V,Z)

  Z_predict = rf.predict(V_test)
  acc = accuracy_score(Z_test, Z_predict)
  print("####### Random Forest Results #######")
  print(f"Random Forest Accuracy Score: {accuracy_score(Z_test, Z_predict)}\n")
  precision = precision_score(Z_test, Z_predict)
  print(f"Random Forest Precision Score: {precision}\n")
  recall = recall_score(Z_test, Z_predict)
  print(f"Random Forest Recall Score: {recall}\n")
  f1 = f1_score(Z_test, Z_predict)
  print(f"Random Forest F1 Score: {f1}\n")
  print('\n\n')

  # SVM
  svm = SVC(kernel='rbf')
  svm.fit(V,Z)
  
  Z_predict = svm.predict(V_test)
  acc = accuracy_score(Z_test, Z_predict)
  print("####### SVM Results #######")
  print(f"SVM Accuracy Score: {accuracy_score(Z_test, Z_predict)}\n")
  precision = precision_score(Z_test, Z_predict)
  print(f"SVM Precision Score: {precision}\n")
  recall = recall_score(Z_test, Z_predict)
  print(f"SVM Recall Score: {recall}\n")
  f1 = f1_score(Z_test, Z_predict)
  print(f"SVM F1 Score: {f1}\n")
  print('\n\n')


  print("####### Cross Validation MLP #######")
  cv = 10
  scores_precision = cross_val_score(best_mlp, data, target, cv=cv, scoring='precision')
  print(f'Cross Validation Precision: {scores_precision.mean()}')
  scores_accuracy = cross_val_score(best_mlp, data, target, cv=cv, scoring='accuracy')
  print(f'Cross Validation Accuracy: {scores_accuracy.mean()}')
  scores_recall = cross_val_score(best_mlp, data, target, cv=cv, scoring='recall')
  print(f'Cross Validation Recall: {scores_recall.mean()}')
  scores_f1 = cross_val_score(best_mlp, data, target, cv=cv, scoring='f1')
  print(f'Cross Validation F1: {scores_f1.mean()}')
  print('\n\n')

  print("####### Confusion Matrix MLP #######")
  cmd = ConfusionMatrixDisplay(cm, display_labels=['Up','Down'])
  cmd.plot()
  

df_train_matrix = pd.read_csv('matriz_resultado_rede_neural.csv', header=0, dtype={'date': 'str', 'neu_mean': 'float', 'neg_mean': 'float', 
                                                      'pos_mean': 'float', 'comp_mean': 'float', 'pol_mean' : 'float', 
                                                      'bt_close': 'float', 'bt_open': 'float', 'bt_high': 'float', 'bt_low': 'float',  
                                                      'bt_volumeto': 'float', 'bt_target': 'float'})
target = df_train_matrix['bt_target']
# mixed data (market and tweets)
data = df_train_matrix[['neu_mean', 'neg_mean', 'pos_mean', 'comp_mean', 'pol_mean','bt_close', 'bt_open', 'bt_high', 'bt_low', 'bt_volumeto']]
# market data
# data = df_train_matrix[['bt_close', 'bt_open', 'bt_high', 'bt_low', 'bt_volumeto']]
# tweets data
# data = df_train_matrix[['neu_mean', 'neg_mean', 'pos_mean', 'comp_mean', 'pol_mean']]
neural_train(data, target)