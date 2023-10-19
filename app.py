from selenium import webdriver
from flask import Flask , render_template , request , jsonify
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
        
        try:
            searchString = request.form['content'].replace(" " , "_")
            Youtube_Url = 'https://www.youtube.com/c/@PW-Foundation/' + searchString
            driver = webdriver.Chrome()
            for url in Youtube_Url:  
                driver.get('https://www.youtube.com/@PW-Foundation/' + searchString)
                content = driver.page_source.encode("utf-8").strip()
                soup = BeautifulSoup(content , 'html.parser')
                titles = soup.findAll('yt-formatted-string' , id = 'video-title')
                views = soup.findAll('span' , class_ = 'inline-metadata-item style-scope ytd-video-meta-block')
                Videos_urls = soup.findAll('a' , id = 'video-title-link' , class_= 'yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media')
                print('Channel:{}'.format(url))
                i = 0 #views and time
                j = 0 # for urls
                with open('my_csv_file.csv' , 'w' , newline='') as csvfile:
                 wirter = csv.writer(csvfile)
                 wirter.writerow(['titles' , 'views' , 'time' , 'Video_link'])
                 for video in url:
                     wirter.writerow([video[titles] , video[views], video[views], video[Videos_urls]])
                 


                
                
                
                 
                for title in titles:
                  print('\n{}\t{}\t{}\thttps:\\www.youtube.com{}'.format(title.text , views[i].text,views[i+1].text,Videos_urls[j].get('href')))

                  i+=2
                  j+=1


            
              # Initialize an empty list to store dictionaries
                videos = []
                mydict = {
                "Product": searchString,
                 "Title": titles,
                 "Views": views,
                 "Time": views,
                 "video_link": Videos_urls
                 }
                videos.append(mydict)
            print(url)    
# Log the result
            logging.info("Logged videos: %s", videos)

        except Exception as e:
            print("exception while creating dictonary" , e)

            


            return render_template('results.html' , videos = videos(len(videos)))
        except Exception as e :
            logging.info(e)
            return 'Something is wrong'
        traceback.print_exc()
        

    else : 
        return render_template('index.html')    
    
    
    

if __name__=='__main__':
    app.run(host="0.0.0.0" , debug= True)    
            
            
                
                    
            



            
          

