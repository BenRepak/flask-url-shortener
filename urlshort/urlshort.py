from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os.path
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort',__name__)

# routes are GET by default
@bp.route('/')
def home():
    # Jinja templating and variable passing
    # return render_template('home.html', name='Ben')
    return render_template('home.html',codes=session.keys())

@bp.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        # create dict of urls
        urls = {}

        # check if file exists
        if os.path.exists('urls.json'):
            # if so, open file and check for entry
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        # check if key exists
        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))

        # check if this is file or url 
        if 'url' in request.form.keys():
            ## build key value pair from form 
            urls[request.form['code']] = {'url':request.form['url']}
        # if not url then it's a file
        else: 
            f = request.files['file']
            # make sure file name is secure before uploading
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/benrepak/Documents/dev/url-shortener/urlshort/static/user_files/'+full_name)
            urls[request.form['code']] = {'file':full_name}


        # build/update json
        with open('urls.json', 'w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']] = True

        # use .form with post, use .args with get
        return render_template('your_url.html', code=request.form['code'])
    else:
        # calls the function home()
        return redirect(url_for('urlshort.home'))
        #return redirect('/')


@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
        if code in urls.keys():
            if 'url' in urls[code].keys():
                return redirect(urls[code]['url'])
            else:
                # serve static file, need to store in static dir
                return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
        else:
            return abort(404)
    else:
        return abort(404)

       

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
  
# jsonify turns dicts or lists and puts into json
@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))