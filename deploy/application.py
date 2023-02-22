from flask import Flask,request,render_template
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import requests
import pymongo
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app=Flask(__name__)
@app.route('/')
def home():
    return render_template("index.html")



@app.route("/vas",methods=["POST"])
def begin():
    if(request.method=="POST"):
        try:
            link=request.form["search"]
            ddd=urlopen(link)
            mmm=ddd.read()
            ddd.close()
            data=bs(mmm,"html.parser")
            mm=data.find_all("div",{"class":"review-container"})
            reviews=[]
            d={}
            for i in mm:
                d={}
                comment=i.find("div",{"class":"text show-more__control"}).text
                name=i.find("div",{"class":"display-name-date"}).text
                user=name.split(" ")[0]
                month=name.split(" ")[1]
                year=name.split(" ")[2]
                rate=i.div.div.span.text[-6:-4]
                d={"comment":comment,"username":user,"month":month,"year":year,"rating":rate}
                reviews.append(d)
            client = pymongo.MongoClient("mongodb+srv://harshithvarmapothuri:12345harshith@cluster0.qmngqfd.mongodb.net/?retryWrites=true&w=majority")
            db = client.test
            dbs=db["harshithvarmapothuri"]
            coll=dbs["asdfgh"]
            coll.insert_many(reviews)
            return render_template("result.html",results=reviews[0:(len(reviews)-1)])
        except:
            return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0")
