import os

def render_html(file,args={}):
    fopen = open(file,'r')
    html = fopen.read()
    fopen.close()
    if args:
        for replace in args:
            replacetag = '{{'+str(replace)+'}}'
            html = str(html).replace(replacetag,str(args[replace]))
    return html