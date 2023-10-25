from selenium import webdriver
from flask import Flask , render_template , request ,redirect,url_for, jsonify
from flask_cors import CORS , cross_origin
import requests
from bs4 import BeautifulSoup
import logging
logging.basicConfig(filename= "youtube_video.log" , level=logging.INFO )
import traceback
import csv
app = Flask(__name__)

@app.route("/" , methods = ["GET"] )
def homepage ():
    return render_template("index.html")

@app.route("/videos", methods = ["POST" , "GET"])
def index():
    if request.method == 'POST':
        title1 = []
        try:
            searchString = request.form['content'].replace(" " , "_")
            Youtube_Url = 'https://www.youtube.com/c/@PW-Foundation/' + searchString
            driver = webdriver.Chrome()  
            driver.get('https://www.youtube.com/@PW-Foundation/' + searchString)
            content = driver.page_source.encode("utf-8").strip()
            soup = BeautifulSoup(content , 'html.parser')
            titles = soup.findAll('yt-formatted-string' , id = 'video-title')
            views = soup.findAll('span' , class_ = 'inline-metadata-item style-scope ytd-video-meta-block')
            Videos_urls = soup.findAll('a' , id = 'video-title-link' , class_= 'yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media')
            print('Channel:{}'.format(Youtube_Url))
            i = 0 #views and time
            j = 0 # for urls
               # Initialize an empty list to store dictionaries
            for title, view, video_url in list(zip(titles, views, Videos_urls))[:6]:
                video_info_text = f"{title.text} || {views[i].text} views {views[i + 1].text} https://www.youtube.com/{video_url['href']}"
                mydict = {
                
                 "Text": video_info_text,
                    "video_link": "https://www.youtube.com/" + video_url['href']
                 }
                title1.append(mydict)
                i+=2
                j+=1
            print(title1)


            with open('video_data.csv' , 'w' , newline='' , encoding='utf-8') as csvfile:
                            wirter = csv.writer(csvfile)
                            wirter.writerow(['heading' , 'Views' , 'Time' , 'Link'])
                            for item in title1:
                                      wirter.writerow([item['Text'] , item["video_link"]])
# Log the result
            logging.info("Logged title: %s", title1)
            return render_template('results.html' , title1 = title1)
        except Exception as e:
            print("exception while creating dictonary" , e)
            
            return redirect(url_for('homepage'))
        
            
            
        except Exception as e :
            logging.info(e)
            return 'Something is wrong'
            
        traceback.print_exc()
        return redirect(url_for('homepage'))    

    else : 
     return render_template('index.html')    
    
    
    

if __name__=='__main__':
    app.run(host="0.0.0.0" , debug= True)    
            
            
                
                    
            



            
          

