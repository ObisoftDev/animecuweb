import os
import json
import uuid

ANIMES_DB = 'animes.adb'
EPISODIES_DB = 'episodies.adb'

ANIMES = []
EPISODIES = []


def load():
    global ANIMES
    global EPISODIES
    ANIMES.clear()
    EPISODIES.clear()
    afile = open(ANIMES_DB,'r')
    animestext = str(afile.read()).replace("'",'"')
    afile.close()
    efile = open(EPISODIES_DB,'r')
    episodiestext = str(efile.read()).replace("'",'"')
    efile.close()
    animes = str(animestext).split('\n')
    episodies = str(episodiestext).split('\n')
    for anime in animes:
        try:
            if anime != '':
                jsonanime = json.loads(anime)
                ANIMES.append(jsonanime)
        except:pass
    for epi in episodies:
        try:
            if epi != '':
                jsonepi = json.loads(epi)
                EPISODIES.append(jsonepi)
        except:pass

def save():
    global ANIMES
    global EPISODIES
    text = ''
    for anime in ANIMES:
        text+=str(json.dumps(anime))+'\n'
    fi = open(ANIMES_DB,'w')
    fi.write(text)
    fi.close()
    text = ''
    for epi in EPISODIES:
        text+=str(json.dumps(epi))+'\n'
    fi = open(EPISODIES_DB,'w')
    fi.write(text)
    fi.close()

def createEpisodie(name,thumburl,url,key,tags=[],descripcion=''):
    return {'name':name,
                      'id':str(uuid.uuid4()),
                      'thumburl':thumburl,
                      'tags':tags,
                      'descripcion':descripcion,
                      'url':url,
                      'key':key}

def createAnime(name,thumburl,key,episodies=[],tags=[],descripcion=''):
    return {'name':name,
                      'id':str(uuid.uuid4()),
                      'thumburl':thumburl,
                      'tags':tags,
                      'descripcion':descripcion,
                      'key':key,
                      'episodies':episodies}

def addEpisodie(episodie):
    global EPISODIES
    EPISODIES.append(episodie)
    save()
    pass
def addAnime(anime):
    global ANIMES
    ANIMES.append(anime)
    save()
    pass
def delete(id,key):
    global ANIMES
    global EPISODIES
    for anime in ANIMES:
        if anime['id']==id:
            if 'key' in anime:
                if anime['key']==key or key == 'admindel':
                    ANIMES.remove(anime)
                    save()
                    return True
            else:
                 ANIMES.remove(anime)
                 save()
                 return True
    for epi in EPISODIES:
        if epi['id']==id:
            if 'key' in epi:
                if epi['key']==key or key == 'admindel':
                    EPISODIES.remove(epi)
                    save()
                    return True
            else:
                 EPISODIES.remove(epi)
                 save()
                 return True
    return False

def getInDB(id):
    global ANIMES
    global EPISODIES
    for anime in ANIMES:
        for epi in anime['episodies']:
            if epi['id']==id:
                return epi
        if anime['id']==id:
            return anime
    for epi in EPISODIES:
        if epi['id']==id:
            return epi
    return None

load()