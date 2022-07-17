from flask import Flask, send_file,send_from_directory,jsonify,redirect,abort,request,render_template
import json
import os
import uuid
from utils import render_html

import database

template_dir = os.path.abspath('web')
app = Flask(__name__,template_folder=template_dir)


@app.route("/<path:path>")
def static_dir(path):
    return send_from_directory("web", path)

@app.route("/")
def base(path):
    return redirect('/home.html')

@app.route("/api/get-latest-episodies")
def get_episodies():
    database.load()
    args = request.args
    result = database.EPISODIES
    if 'animeid' in args:
        animeid = args['animeid']
        get = database.getInDB(animeid)
        result = get['episodies']
    return jsonify({'status':'OK','result':result})

@app.route("/api/get-animes")
def get_animes():
    database.load()
    return jsonify({'status':'OK','result':database.ANIMES})


@app.route("/api/streamVideo/<path:path>")
def stream_video(path):
    database.load()
    get = database.getInDB(path)
    if get:
       return redirect(get['url'])
    abort(480)


@app.route("/api/get-a-db")
def get_a_db():
    return send_file(database.ANIMES_DB)
@app.route("/api/get-e-db")
def get_e_db():
    return send_file(database.EPISODIES_DB)

@app.route("/video")
def get_video():
    database.load()
    args = request.args
    episodies = database.EPISODIES
    if args:
        if 'animeid' in args:
            get = database.getInDB(args['animeid'])
            if get:
                episodies = get['episodies']
        if 'id' in args:
            for epi in episodies:
                if epi['id'] == args['id']:
                    return render_html('web/videoview.html',
                                       {'videoid':args['id'],
                                        'poster':epi['thumburl'],
                                        'name':epi['name'],
                                        'descripcion':epi['descripcion']})
            return ''
    abort(480)

@app.route("/anime")
def get_anime():
    database.load()
    args = request.args
    if args:
        if 'id' in args:
            for anime in database.ANIMES:
                if anime['id'] == args['id']:
                    return render_html('web/animeview.html',
                                       {'animeid':args['id'],
                                        'poster':anime['thumburl'],
                                        'name':anime['name'],
                                        'descripcion':anime['descripcion']})
            return ''
    abort(480)

@app.route("/poster",methods=['GET','POST'])
def poster():
    database.load()
    args = request.args
    form = request.form
    data = {}
    posttype = ''
    if args:
        if 'post' in args:
            posttype = args['post']
    if form:
        if posttype=='episodie':
            episodie = database.createEpisodie(form['name'],
                                               form['thumburl'],
                                               form['url'],
                                               form['key'],
                                               form['genres'],
                                               form['description'])
            database.addEpisodie(episodie)
            return redirect('/home.html')
            pass
        if posttype=='anime':
            anime = database.createAnime(form['name'],
                                               form['thumburl'],
                                               form['key'],
                                               [],
                                               form['genres'],
                                               form['description'])
            if anime['name']=='' or anime['thumburl']=='' or anime['key']=='':
                return render_html('web/poster-a.html',data)
            episodies = str(form['episodies']).replace('\r','').split('\n')
            for epi in episodies:
                if epi!='':
                    get = database.getInDB(epi)
                    if get:
                        anime['episodies'].append(get)
                        database.delete(get['id'],get['key'])
            database.addAnime(anime)
            return redirect('/directorio.html')
            pass
        pass
    if posttype=='anime':
       return render_html('web/poster-a.html',data)
    if posttype=='episodie':
       return render_html('web/poster-e.html',data)
    abort(480)

@app.route("/delete",methods=['GET','POST'])
def delete():
    database.load()
    args = request.args
    form = request.form
    id = ''
    key = ''
    postname = ''
    error = ''
    if args:
        if 'id' in args:
            id = args['id']
    get = database.getInDB(id)
    if get:
        postname = get['name']
    if form:
        try:
            key = form['key']
            deleting = database.delete(id,key)
            if deleting:
                return redirect('/home.html')
            error = 'Error En La Clave'
        except:error = 'Error En La Clave'
    return render_html('web/delete.html',{'postid':id,'postname':postname,'error':error})

if __name__ == "__main__":
    app.run(port=443)
