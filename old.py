from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

#Parses the message to determine desired function
def processText(message):
    #Sanitize message
    message = message.lower().strip()

    ##Spotify handlers
    if message.startswith("https://open.spotify.com/track/"):           #Queue a song by URL
        return spotify('q',message)
    elif message.startswith("song"):     #Info about current song
        return spotify('s',"foo")
    return "Oh"


##Spotify Functions
def spotify(req, msg):
    if req == 'q':
        SCOPE = 'user-modify-playback-state'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE)) #client_id=SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI))
        sp.add_to_queue(msg)
        return "Your song has been added to the queue!"
    elif req == "s":
        SCOPE = 'user-read-currently-playing'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI, scope=SCOPE))
        reply = sp.current_user_playing_track()
        return "Current Song: " + reply["item"]["name"] + " - " + reply["item"]["artists"][0]["name"]
        
    
# Main method. When a POST request is sent to our local host through Ngrok 
# (which creates a tunnel to the web), this code will run. The Twilio service # sends the POST request
@app.route('/sms', methods=['GET', 'POST'])
def incoming_sms():
    reply = processText(request.values.get('Body', None))
    resp = MessagingResponse()
    resp.message('\n\n' + reply)
    return str(resp)
	

# when you run the code through terminal, this will allow Flask to work
if __name__ == '__main__':
    app.run()
    
    
  