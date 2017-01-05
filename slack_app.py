import urllib2

from flask import Flask
from flask import render_template
from flask import url_for
from flask import jsonify
from flask import request

from parser import parser

app = Flask(__name__)

# Get the source code for a given url
def getSource(url):
    usock = urllib2.urlopen(url)
    data = usock.read()
    usock.close()
    return data

# Returns html that displays the source code of a given url
@app.route('/getHTML/', methods=["POST"])
def getHTML():
    try:
        url = request.form.get('url')
        if url is None or len(url) < 12 or (url[0:11] != 'http://www.'):
            return_json = {'html': '', 'stats': '', 'success': False}
            return jsonify(**return_json)

        #Get the source code
        data = getSource(url)

        # Get html to send back from parser
        parser.feed(data.decode('utf-8', 'ignore'))
        parsed = parser.reformat()
        stats = parser.stats
        stats = [(k, stats[k]) for k in stats.keys()]

        # Clear the parser for future requests
        parser.clear()

        return_json = {'html': parsed, 'stats': stats, 'success': True}
        return jsonify(**return_json)

    # Inform client of Failure
    except Exception as e:
        parser.clear()
        return_json = {'html': '', 'stats': '', 'success': False}
        return jsonify(**return_json)

# Route for rendering the main page
@app.route('/')
def challenge():
    return render_template('challenge.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')