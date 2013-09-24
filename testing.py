import SocketServer 
import CGIHTTPServer 
import urllib2

from pyechonest import artist, playlist, track, song
from echonest.remix.audio import LocalAudioFile, AudioData
from echonest.remix.action import render, Playback, display_actions
import my_modify
import shutil
import datetime

PORT = 8080

def header():
  return "<html><title>testing</title><body>"
def footer():
  return "</body></html>"
def get_song_characteristics(sID): #(sTitle, sArtist):
  sSong = song.profile(ids =sID)
  dsSummary = sSong[0].get_audio_summary()
  print(dsSummary)
  #print(sSong)
  #sSong = song.search(artist=sArtist, title=sTitle, results=1, buckets=['audio_summary'])
  #print(sID)
  #tTrack = track.track_from_id(identifier=sID)
  #tTrack.get_analysis()
  #print(str(tTrack))
  #things I may be able to impact
  #"tempo": 74.694,
  #"loudness": -4.613,
  #energy": 0.6617689403520844,
  return dsSummary

def get_suggestions(artists):
  asSuggestions = []
  #print(artists)
  asSeed_artist_ids = lookup_seeds(artists)
  if len(asSeed_artist_ids) >5:
    asSeed_artist_ids = asSeed_artist_ids[:4]
  acPlaylist = playlist.static(type='artist-radio', artist_id=asSeed_artist_ids, variety=1)
  
  dJoined = {}
  dJoined['tempo'] = 0  
  dJoined['loudness'] = 0  
  dJoined['key'] = 0  
  dJoined['danceability'] = 0  
  dJoined['valence'] = 0  
  dJoined['time_signature'] = 0  
  dJoined['liveness'] = 0  
  for cSong in acPlaylist:
    print(str(cSong))
    sName = cSong.artist_name
    sTitle = cSong.title
    #{u'time_signature': 4, u'analysis_url': u'http://echonest-analysis.s3.amazonaws.com/TR/OqovGwdNlmWtC8VzwJogN4Opv5rBOGHWijcEaB/3/full.json?AWSAccessKeyId=AKIAJRDFEY23UEVW42BQ&Expires=1379809796&Signature=v6ip9VeZolRYdPLQb6ZCHLjty5Q%3D', 
    #u'energy': 0.6618792929537817, u'liveness': 0.20491740560245644, 
    #u'tempo': 101.236, u'speechiness': 0.04450662602495192, u'acousticness': 0.041829643112355895, u'mode': 1, u'key': 6, u'duration': 303.64, 
    #u'loudness': -8.239, u'audio_md5': u'6aea199d3def4f58dca07819772586cb', 
    #u'valence': 0.6757293197830115, u'danceability': 0.29761525479382267}
    dChars = get_song_characteristics(cSong.id)
    for key, val in dChars.items():
      if (dJoined.get(key) != None):
        dJoined[key] += val
    asSuggestions.append(sName + sTitle)
  print(dJoined, len(asSuggestions))
  return [asSuggestions, dJoined]

def lookup_seeds(seed_artist_names):
    seed_ids = []
    for artist_name in seed_artist_names:
        try:
            seed_ids.append("%s" % (artist.Artist(artist_name).id,))
        except Exception:
            print('artist "%s" not found.' % (artist_name,))
            # we could try to do full artist search here
            # and let them choose the right artist
    print('seed_ids: %s' % (seed_ids,))
    return seed_ids

class Proxy(CGIHTTPServer.CGIHTTPRequestHandler):
  def get_vars(self, asFields):
      anLocs = []
      for sField in asFields:
        anLocs.append(self.path.find(sField))
      anLocs.append(len(self.path) + 1)
      dsVars = {}
      for i, nLoc in enumerate(anLocs[:-1]):
        #                                plus one for =         +1 for next field loc #-1 for next field starting loc vs end
        dsVars[asFields[i]] = self.path[ nLoc + len(asFields[i]) + 1 : anLocs[i+1] - 1 ]
      return dsVars

  def do_GET(self):
    if "static" in self.path or "music" in self.path:
      fFileToServe = open(self.path[1:] ,'r') #urllib removed front / urllib 2 gives it thus starting at 1
      self.copyfile(fFileToServe, self.wfile)
      fFileToServe.close()
    elif "set_fields" in self.path:
      #this section assumes the fields are all given, no query. 
      #need mp3 tempo, key change, timbres to use, 
      asFields = ["song", "tempo", "key", "timbres"]
      dsVars = self.get_vars(asFields)
      
      sTimestampedFileName = 'music/' + dsVars['song']+ '_to_' + dsVars['timbres'] + datetime.datetime.now().strftime('%d.%h%M%S') + '.wav'
      #writes file called niceout.wav
      my_modify.do_something('music/' + dsVars['song'], int(dsVars['tempo']), int(dsVars['key']), 0, dsVars['timbres'])
      shutil.move('niceout.wav', sTimestampedFileName) #just note to self, niceout.wav will be file, want to move it to a timestamped fil

      self.wfile.write(header()) 
      self.wfile.write('original<audio controls><source src="music/' +dsVars['song'] + '" type="audio/wav"></audio>')
      self.wfile.write('<br>new<audio controls><source src="' + sTimestampedFileName + '" type="audio/wav"></audio>')
      self.wfile.write(footer()) 
    else:
      self.wfile.write(header()) 
      sArtistFieldName = "&artists="
      sSongFieldName = "?song="
      sGenreFieldName = "&genre="
      nSongLoc = self.path.find(sSongFieldName)
      nArtistLoc = self.path.find(sArtistFieldName)
      nGenreLoc = self.path.find(sGenreFieldName)
      if nArtistLoc == -1 or nSongLoc == -1 or nGenreLoc == -1:
        self.wfile.write("<br>no artists input")
      else: 
        sSong = self.path[nSongLoc+len(sSongFieldName):nArtistLoc]
        sArtists = self.path[nArtistLoc+len(sArtistFieldName):nGenreLoc]
        sGenre = self.path[nGenreLoc + len(sGenreFieldName):]
        print(sArtists,sSong, sGenre)
        self.wfile.write("<br>" + sArtists + " yields the following suggestions<br>")
        [asSugs, dJoined] = get_suggestions(sArtists)
        for sSug in asSugs:
          sSug = sSug.encode('ascii', 'ignore')
          self.wfile.write(sSug + "<br>")
          #self.wfile.write(urllib2.quote(sSug.encode("utf-8")) + "\n")
        nSamples = len(asSugs)
        my_modify.do_something('../music/' + sSong, dJoined['tempo']/nSamples, dJoined['key']/nSamples, dJoined['loudness']/nSamples, sGenre)
        sTimestampedFileName = '../music/' + sSong+ '_to_' + sArtists+ datetime.datetime.now().strftime('%d.%h%M%S') + '.wav'
        shutil.move('niceout.wav', sTimestampedFileName) #just note to self, niceout.wav will be file, want to move it to a timestamped file, 
        self.wfile.write('original<audio controls ><source src="../music/' +sSong + '" type="audio/wav">Your browser does not support the audio element. </audio>')        
        self.wfile.write('<br>new<audio controls ><source src="' + sTimestampedFileName + '" type="audio/wav">Your browser does not support the audio element. </audio>')        
      self.wfile.write(footer())
  def do_POST(self):
    self.wFile.write("posting")


httpd = SocketServer.ForkingTCPServer(('', PORT), Proxy)
print "serving at port", PORT
httpd.serve_forever()

