from selenium import webdriver
from flask import Flask , render_template , request , jsonify
from flask_cors import CORS , cross_origin
import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(filename= "youtube_video.log" , level=logging.INFO )
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

@app.route("/" , methods = ["GET"] )
def homepage ():
    return render_template("index.html")

@app.route("/videos" , methods = ["POST" , "GET"])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace[" ", " "]
            Youtube_Url = 'https://www.youtube.com/results?search_query=' + searchString
            driver = webdriver.Chrome()
            driver.get('https://www.youtube.com/results?search_query=' + searchString)
            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content , 'lxml')
            titles = soup.findAll('yt-formatted-string' , id = 'video-title')
            views = soup.findAll('span' , class_ = 'inline-metadata-item style-scope ytd-video-meta-block')
            Videos_urls = soup.findAll('a' , id = 'thumbnail' , class_= 'yt-simple-endpoint inline-block style-scope ytd-thumbnail')
            print('Channel:{}'.format(Youtube_Url))
            i = 0 #views and time
            j = 0 # for urls
            filename = searchString + ".csv"
            fw = open(filename , "w")
            headers = "Title" , "Views" , "Time" , "video_link \n"
            fw.write(headers)
            videos = []
            for title in titles():
                print('\n{}\t{}\t{}\thttps:\\www.youtube.com{}'.format(title.text , views[i].text,views[i+1].text,Videos_urls[j].get('href')))

                i+=2
                j+=1


            try:
              mydict = {"Product": searchString , "Title" : titles , "views" : views , "Time" : views , "video_link" : Videos_urls }
              videos.append(mydict)
            except Exception as e:
              print("exception while creating dictonary" , e)

              logging.info("log my final result{}".format(videos))
        
        
           
            uri = "mongodb+srv://Pytonlearning:Bishu1994@cluster0.ozde5yd.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
            client = MongoClient(uri, server_api=ServerApi('1'))
            db = client['youtube_scrap']
            review_col = db['youtube_scrap_data']
            review_col.insert_many(videos)


            return render_template('results.html' , videos = videos[0: (len(videos)-1)])
        except Exception as e :
            logging.info(e)
            return 'Something is wrong'
        

    else : 
        return render_template('index.html')    
    


if __name__=='__main__':
    app.run(host="0.0.0.0" , debug= True)    
            
            
                
                    
            



            
          

