chi_music_hackathon_stylizer
============================

trying to use the echonest remix library to modify some songs

... 
currently things are a bit broken, I reorganized some folders when I got home from the hackathon to ... well better organize

trying to make it a little less hacky. 

hopefully I will get a modify subclass built to do the timbre things I wanted to do earlier

currently reorganizing. 

next thing Im trying to get done is to get the fade function from audio working. 

not sure who uses the remix library but it seems a bit buggy. not sure if its my install / linux setup or what

but I will also be trying to resolve some of those issues if I can, not that I can push them to the echonest, but whatever.

things to do going forward ... 

  try to ignore issues. 

    except, fix en-ffmpeg to work with mp3s

    maybe glance at why api key gets dropped on submit... probably a python goodie where somebody doesnt think about a reference... it happens

  subclass the modify class to actually get the kind of edits I want. 

  if I bang my head to hard against a wall... search for a different library / methodology

    want to be able to use the remix library to modify existing songs, 

     can take sound data from samples as broken down by remix, but modify does not edit songs the way I want. 

     can use remix modify package to put two samples together, which is a fairly powerful thing, 

       and if I can get sample information I can do most of the editing I want, I think, but Im not certain. 

        ie still investigating. ... but it will be more like, here is the timbre I want to get to

         .. and then modifying/replacing the sounddata ... requires investigating. 

  set up dynamic html pages to modify a folder as opposed to a list. ... 

    sort of working towards that, but not there

  save feature after processing one song, dont do it again. 

  check if timbre methodology actually makes sense... 


currently investigating loris, as it appears to have the closet starting point to what I am looking for. should be interesting

 need to investigate differences between representations, how to use the the libs interchangably or to switch over what I have..

 we shall see. 


also somebody just suggested mixxx to me ... so downloading that lets see where this investigation leads ... 
  guess I should actually play around with loris first. 
