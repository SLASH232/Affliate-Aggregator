from flask import Flask,request,jsonify,redirect
from flask_cors import CORS
import asyncio
import subprocess
from main import compared_commission_rates,get_result_bq,get_url

app=Flask(__name__)
CORS(app)

@app.route("/",methods=['GET'])
def say_hello():
    return jsonify("Hey !!"),200


## Commission

# input and get  commission rates for all other sites
@app.route('/get_commission_rates',methods=['POST'])
def get_commission_rates():
    product_link=request.json.get('productLink')
  
    commission_rates =  asyncio.run(compared_commission_rates(product_link))
    return jsonify(commission_rates) ,200

# take product title and affiliate links and store it in db
@app.route('/create_link',methods=['POST'])
def submit_form():
    title= request.json.get('title')
    amazon_url = request.json.get('amazon_url')
    flipkart_url= request.json.get('flipkart_url')
    keyword=request.json.get('keyword')
       
    # Run scraper asynchronously in a separate Python process
    command = f"python3 ./__init__.py {amazon_url} \"{flipkart_url}\" \"{title}\" \"{keyword}\" /results"
    subprocess.Popen(command, shell=True)    

    response={'message':'Recieved data successfully'}
    return jsonify(response),200

# i want that product according choosen column
@app.route('/result',methods=['GET'])
def get_result():
    results=get_result_bq()
    product_dict = {}
    for index, result in results.iterrows():
        product_dict[result['title']] = {
            'pid':result['pid'],
            'title':result['title'],
            'status':result['status'],
                }

    formatted_results = list(product_dict.values())

    return jsonify(formatted_results),200

# handle genrallink
@app.route('/my-product/<pid>')
def redirect_to_site(pid):
    # Map site_name to actual URLs
    target_url = get_url(pid)
    return redirect(target_url)


if __name__ == '__main__':
    app.run(debug=True, port=8080)