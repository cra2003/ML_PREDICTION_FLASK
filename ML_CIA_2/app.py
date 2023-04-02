from flask import Flask, request,    render_template
import mysql.connector as sql



app = Flask(__name__)
import pickle

model = pickle.load(open('model.pkl','rb'))

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login",methods=["GET","POST"])
def login():
    con=sql.connect(user='root', password='Karthic@2206*',host='localhost',database='ACCT')
    cur=con.cursor()

    username = request.form['username']
    password = request.form['password']
    cur.execute('select * from details')
    t=cur.fetchone()
    # Check if the username exists and the password matches
    if username ==t[0] and password==t[1]:
        return render_template("index.html")

    else:
        return render_template("login.html")


  
@app.route("/predict", methods=['post'])
def pred():

    import pandas as pd
    data=pd.read_csv('completevirat.csv')


    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    data['grd'] = le.fit_transform(data['Ground'])
    g1={}
    g2={}
    for i,j in data.iterrows():
        g1[j['Ground']]=j['grd']
        g2[j['grd']]=j['Ground']

        
    data['opponent'] = le.fit_transform(data['Opp'])
    o1={}
    o2={}
    for i,j in data.iterrows():
        o1[j['Opp']]=j['opponent']
        o2[j['opponent']]=j['Opp']






    features = [(i) 
                for i in 
                (request.form.values())]
    
    feat=[features[0],g1[features[1]],o1[features[2]]]
    pred = model.predict([feat])
    print(features)
    if pred==[0]:
        return render_template("success.html",
                           data='<30')
    elif pred==[1]:
        return render_template("success.html",
                           data='30-50')
    else:
        return render_template("success.html",
                           data='>50')
    
if __name__=='__main__':
    app.run(host='localhost',port=5000,debug=True)
    
    
    
    
    
    
    
    