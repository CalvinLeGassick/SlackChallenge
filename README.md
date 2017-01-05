This folder contains the code for the Slack Challenge, built by Calvin LeGassick.

### Set up
Ensure you are in the Slack directory, and that you have pip and virtualenv installed.
For the first time running the application, we need to run the following lines of code:
<pre>
<code>
   virtualenv env 
   source env/bin/activate
   pip install -r requirements.txt
</code>
</pre>

Once we have activated the virtual environment and installed all of the requirements:

<code>python slack_app.py</code>

Will start the program on port 5000.

virtualenv & pip:
* pip: http://python-packaging-user-guide.readthedocs.org/en/latest/installing/#use-pip-for-installing
* virtualenv: http://virtualenv.readthedocs.org/en/latest/installation.html

### Functionality
This application is capable of taking in urls from the client, and then sending back a representation of the source code at that url that can be rendered in the browser. The brunt of this work is in dismantling the source code and bringing it back together in a meaningful structure. The client receives a visualization of the source code, and has the ability to see the each kind of opening + closing tag used in the source, as well as the total count for each kind of tag. Clicking on the tags in the list highlights all tags of that kind is a slack-tastic color!

### Deploylemt
The app is currently deployed to Heroku.