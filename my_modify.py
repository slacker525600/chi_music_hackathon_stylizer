from echonest.remix.audio import LocalAudioFile, AudioData
from echonest.remix.action import render, Playback, display_actions
import random
import numpy
import sys
import time
import echonest.remix.audio as audio
import cPickle
from echonest.remix import modify
from pyechonest import config
config.ECHO_NEST_API_KEY="V2SK2YI479RJEKRGG"

def reverse():
    sInputFileName = '../music/Lorde_royals.mp3'
    sOutputFileName = '../music/new.wav'
    audioFile = audio.LocalAudioFile(sInputFileName)
    sToReverse = 'segments' # ... dont know what this does, want to test it ... 
    if sToReverse == 'beats' :
        chunks = audioFile.analysis.beats
    elif sToReverse == 'segments' :
        chunks = audioFile.analysis.segments
    else :
        print usage
        return
    chunks.reverse()
    reversedAudio = audio.getpieces(audioFile, chunks)
    reversedAudio.encode(sOutputFileName)

def do_something(sFileToConvert, nTempoToHit, nPitchOffset, nLoudness, sGenre):#dJoined):
  fFile = open('../music/' + sGenre, 'r')
  aTimbres = cPickle.load(fFile)
  fFile.close()
  print('using timbres:' + str(aTimbres))
  #sGenre needs to match one of the .clstr files in music. 
  mod = modify.Modify()
  track = audio.LocalAudioFile(sFileToConvert, verbose='verbose')
  #... trying to read waltzify, but its not awesome, not unclear persay, but too complicated of an example to work from. 
  beats = track.analysis.beats
  out_shape = (len(track.data),)
  anNewBeats = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)
  #print(track.analysis.key)
  nPitchOffset = nPitchOffset -track.analysis.key['value']
  for i, beat in enumerate(beats):
    #data = track[beat].data
    anNewBeats.append(mod.shiftPitchSemiTones(track[beat], int(nPitchOffset *1.5))) #convert from key to pitch

  track.data = anNewBeats
  segments = track.analysis.segments
  print(track.analysis.tempo['value'])
  fScaleTime = nTempoToHit / track.analysis.tempo['value']
  chunks = []
  for segment in segments:
    segment.duration = segment.duration /fScaleTime
    anTimbreDistances = []
    for anTimbre in aTimbres:
      timbre_diff = numpy.subtract(segment.timbre,anTimbre)
      anTimbreDistances.append(numpy.sum(numpy.square(timbre_diff)))
    segment.timbre = aTimbres[anTimbreDistances.index(min(anTimbreDistances))]
    chunks.append(segment)
  print(track.analysis.tempo['value'])
    
  modAudio = audio.getpieces(track.data, chunks)
  #modAudio = audio.fadeEdges(modAudio.data)
  modAudio.encode('niceout.wav')

def one():
  audiofile = audio.LocalAudioFile(input_filename)  
  bars = audiofile.analysis.bars
  collect = audio.AudioQuantumList()
  for bar in bars:
      collect.append(bar.children()[0])
  out = audio.getpieces(audiofile, collect)
  out.encode(output_filename)

def chipmunk(sFile):
  do_something(sFile, 120, 10,0, 'ebm.mp3.clstr')

#could put if main if statement here, 
if (__name__ == '__main__') :
  #do_something('../music/gam.mp3', 150, 5, 5,'ebm.mp3.clstr')
  chipmunk('../music/gam.mp3')


class my_mod_class(modify.Modify):
  nothing = 'nothing'
