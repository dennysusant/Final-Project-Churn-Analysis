from flask import Flask, abort, jsonify, render_template,url_for, request,send_from_directory,redirect
import numpy as np 
import pandas as pd 
import json
import requests 
import pickle
import mysql.connector
from sklearn import preprocessing
import pickle
#===============================================Read CSV================================
data=pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
app=Flask(__name__)
columnCat=['gender', 'Partner', 'Dependents','PhoneService', 'MultipleLines', 'InternetService','OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport','StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling','PaymentMethod']


ListOption=[]
for item in data.columns:
    ListOption.append([item,data[item].unique()])
# print(ListOption)
ListOption=ListOption[1:-1]

label= preprocessing.LabelEncoder()
data['Churn']=label.fit_transform(data['Churn'])


@app.route('/')
def home():
    return render_template('home.html',ListOption=ListOption)

@app.route('/hasil', methods=['GET','POST'])
def hasil():
    body=request.values
    print(body['gender'])
    prep=[]
    for item in data.columns[1:-1]:
        if item in columnCat:
            label.fit(data[item])
            prep.append(int(label.transform([body[item]])))
        else:
            prep.append(float(body[item]))
    series = {}
    for item,item1 in zip(prep,data.columns[1:-1]):
        series[item1]=item
    vector=pd.DataFrame(series,index=[0])
    print(vector)
    a=xgb.predict(vector.iloc[:1])[0]
    if a==1:
        return render_template('home.html',ListOption=ListOption,x='Customer might Churn')
    else:
        return render_template('home.html',ListOption=ListOption,x='Customer will not Churn')

if __name__=='__main__':
    import pickle
    with open('XGBModel.pkl','rb') as x:
        xgb=pickle.load(x)
    app.run(host='0.0.0.0',port=5000,debug=True)
