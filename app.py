from flask import Flask,render_template,request
from PythonScripts.Connecting_and_Storing_Data import Connect_Store_Data
from PythonScripts.Create_Model import Get_Predictions
from flask import Response
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
def collectData():
   if request.method=='POST':
       stock = request.form['selectItem']
       obj = Connect_Store_Data(stock)
       obj.update_data()
       days = int(request.form['No_of_days'])
       obj1 = Get_Predictions(stock)
       (labels, values, values1) = obj1.create_model(days)
       return render_template('output.html', labels=labels, values=values, values1=values1)



if __name__=='__main__':
    app.run(host="0.0.0.0", port=8080)