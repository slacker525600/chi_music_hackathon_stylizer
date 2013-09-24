# want to analyze ... and then cluster the timbers from the segments. 
import os
import cPickle
from hcluster import linkage, fclusterdata, dendrogram
from echonest.remix.audio import LocalAudioFile, AudioData
from echonest.remix.action import render, Playback, display_actions
import echonest.remix.audio as audio
from echonest.remix import modify
from pyechonest import config
config.ECHO_NEST_API_KEY="V2SK2YI479RJEKRGG"

def get_clusters(aanTimbres):
  #linkage was example ... output didnt make sense to me. 
  #return linkage(aanTimbres, method='complete')
  #was thinking, each instrument by each note maybe, but whatever
  return fclusterdata(aanTimbres, 50, criterion='maxclust') 

def try_something(sInputFileName):
  audioFile = audio.LocalAudioFile(sInputFileName)
  segments = audioFile.analysis.segments
  anTimbres = []
  print(len(segments))
  for s in segments:
    #print(s.timbre)
    anTimbres.append(s.timbre)
  anCluster = get_clusters(anTimbres)
  #dendrogram(aanCluster)
  dnMeans = {}
  for nSound in range(0,len(anCluster)):
    nIn = anCluster[nSound]
    nExists = dnMeans.get(nIn) 
    if nExists != None:
      #print(len(nExists[0]), len(anTimbres[nIn]))
      for nTimbre in range(0, len(anTimbres[nSound])):
        nExists[0][nTimbre] += anTimbres[nSound][nTimbre] #this is pretty wrong, db arent additive. 
      nExists[1] += 1
    else:
      dnMeans[nIn] = [anTimbres[nSound], 1]
  anVectors = []
  for key, val in dnMeans.items():
    #a lot of these clusters are unique sounds. if it only shows up once, ignore it, not a defining characteristic
    if (val[1] == 1):
      continue
    for nTimbre in val[0]: #normalizing back the additions above
      val[0][val[0].index(nTimbre)] /= val[1] #same wrong addendum above matches here. 
    anVectors.append(val[0])
  return anVectors

if __name__ == "__main__":
  asFiles = os.listdir('music/')
  clusters = []
  for sFile in asFiles:
    if '.clstr' in sFile:
      continue
    elif sFile+'.clstr' in asFiles:
      continue
    else:
      print('new file found, performing analysis')
      clusters.append([sFile, try_something(sFile)])
  for ac in clusters:
    fOut = open(ac[0]+'.clstr', 'w')
    cPickle.dump(ac[1], fOut)
    fOut.close()
