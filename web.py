from data.make_dataset import make_dataset_dl
from data.make_dataset import make_dataset_ml
from utils import majority_voting
from utils import get_genres
from joblib import load
from tensorflow.keras.models import load_model
from flask import Flask, render_template, Response, request, redirect, url_for 
from  werkzeug  import  secure_filename
import time
import pyaudio
import wave
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)

UPLOAD_FOLDER  =  'static/music/'
ALLOWED_EXTENSIONS  =  set (['wav','mp3'])

def  allowed_file ( filename ): 
    return  '.'  in  filename  and \
            filename.rsplit('.' , 1)[ 1 ]  in  ALLOWED_EXTENSIONS

def  allowed_file ( filename ): 
    return  '.'  in  filename  and \
            filename.rsplit('.' , 1)[ 1 ]  in  ALLOWED_EXTENSIONS

@app.route ("/" ,methods = ['GET','POST']) 
def  upload_file (): 
    if  request.method  ==  'POST' : 
        file  =  request.files ['file'] 
        if  file  and  allowed_file(file.filename): 
            filename  =  secure_filename(file.filename ) 
            file.save ( os.path.join ( UPLOAD_FOLDER,  filename )) 
            return  redirect (url_for('predict' ,filename = filename )) 
    return render_template('index.html') 

@app.route("/predict/",methods = ['GET','POST'])
def predict():
    genres = {
        'metal': 0, 'disco': 1, 'classical': 2, 'hiphop': 3, 'jazz': 4, 
        'country': 5, 'pop': 6, 'blues': 7, 'reggae': 8, 'rock': 9
    }
    test_model = 'cnn.h5'
    filename = request.args.get('filename')
    test_song = UPLOAD_FOLDER + filename
    X = make_dataset_dl(test_song)
    model = load_model(test_model)
    preds = model.predict(X)
    votes = majority_voting(preds, genres)
    print("{} is a {} song".format(test_song, votes[0][0]))
    print("most likely genres are: {}".format(votes[:3]))

    song_name = test_song.split('/')[-1]
    result1 = song_name + " is a " + str(votes[0][0]) + " song."
    result2 = "Most likely genres are: " + str(votes[:3])
    return render_template('result.html',result1=result1, result2=result2, song= 'music/' + song_name ) 

@app.route('/audiofeed')
def audiofeed():
    def gen(microphone):
        while True:
            sound = microphone.getSound()
            #with open('tmp.wav', 'rb') as myfile:
            #   yield myfile.read()

            yield sound

    return Response(stream_with_context(gen(Microphone())))

def getSound(self):
    # Current chunk of audio data
    data = self.stream.read(self.CHUNK)
    self.frames.append(data)
    wave = self.save(list(self.frames))

    return data

if __name__ == "__main__":
    app.run()