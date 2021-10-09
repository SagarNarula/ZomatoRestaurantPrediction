import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('Zomato.pkl', 'rb'))
file = open("mapping_dict.obj",'rb')
dict_all_loaded = pickle.load(file)
file.close()



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    
    '''
    if request.method == 'POST':
        data=pd.DataFrame()
        votes = int(request.form['Votes'])
        Average_Cost = float(request.form['AverageCost'])
        online_order = request.form['OnlineOrder']
        if(online_order=='Yes'):
            online_order = 1
                
        else:
            online_order = 0
        book_table=request.form['BookTable']
        if(book_table=='Yes'):
            book_table=1
                
        else:
             book_table=0
        
        location=request.form['locate']
        cuisines=request.form['cuisine']
        rest_type=request.form['Rest']
        
        data.loc[0,'location']=location
        data.loc[0,'cuisines']=cuisines
        data.loc[0,'rest_type']=rest_type
        
        data['location']=data['location'].astype(object)
        data['cuisines']=data['cuisines'].astype(object)
        data['rest_type']=data['rest_type'].astype(object)
        
        for col in data.columns:
             data.replace(dict_all_loaded[col], inplace=True)
        data['votes']=votes
        data['Average_Cost']=Average_Cost
        data['book_table']=book_table
        data['online_order']=online_order
        
        

        
    #int_features = [int(x) for x in request.form.values()]
    #final_features = [np.array(int_features)]
    prediction = model.predict(data)

    output = round(prediction[0], 2)

    return render_template('Index.html', prediction_text='Rating for this Hotel is  {}'.format(output))



if __name__ == "__main__":
    app.run(debug=True)