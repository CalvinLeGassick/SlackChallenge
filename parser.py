# A class that takes in html source code and produces html that will display that source code

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class HTMLViewConstructor(HTMLParser):

    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)

        self.html = ''
        self.stats = {}
        # Needed for handling some special cases
        self.empty_elements = ([
        'link', 'track', 'param', 'area', 'command', 'col',
         'base', 'meta', 'hr', 'source', 'img', 'keygen', 'br',
         'wbr', 'colgroup', 'input'])

    def handle_starttag(self, tag, attrs):
        if self.stats.get(tag) is not None:
            self.stats[tag] += 1
        else:
            self.stats[tag] = 1

        if tag not in self.empty_elements:
            # Create meta tag, everything nested inside
            self.html += '<div><div class = \'meta meta-' + tag +'\'></div>'

        classes = ['spacing', 'start', 'type-start-'+tag]
        if tag in self.empty_elements:
            classes.append('empty')

        # Classes for meta div:
        self.html += '<div><div class =\''
        for c in classes:
            self.html += ' ' + c
        self.html += '\'>'

        # Open the readable tag
        self.html += '&lt' + tag + ' '
        for (name, value) in attrs:
            name = name or u''
            value = value or u''
            self.html += name + '=\'' + value.replace('<',"&lt").replace('>','&gt') + '\' '
        self.html += '&gt' + '</div></div>'

    def handle_endtag(self, tag):
        if self.stats.get(tag) is not None:
            self.stats[tag] += 1
        else:
            self.stats[tag] = 1

        # Close the readable tag
        classes =['end', 'type-end-'+tag]
        self.html += '<div><div class =\''
        for c in classes:
            self.html += ' ' + c
        self.html += '\'>'
        self.html += '&lt/' + tag + '&gt' + '</div></div>'

        if tag not in self.empty_elements:
            # Close the meta tag
            self.html += '</div>'

    def handle_data(self, data):
        # Don't add a content div if there is no data inside the tag
        if len(data.strip()):
            # Remove all '<' and '>' so the browser doesn't get confused
            self.html += ('<div class = \'content\' >'
                + data.replace('<',"&lt").replace('>', "&gt").replace('\/','/')
                + '</div>')

    # Return our newly formatted html
    def reformat(self):
        self.close()
        return self.html

    # Clear all data
    def clear(self):
        self.close()
        self.html = ''
        self.stats = {}

parser = HTMLViewConstructor()
