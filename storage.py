import webapp2
#from google.appengine.api import app_identity
from google.appengine.api import files, app_identity
from google.appengine.ext import blobstore, db
from google.appengine.ext.webapp import blobstore_handlers
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
            extensions=['jinja2.ext.autoescape'],
            autoescape=True)

#BUCKET = '/gs/cs553storage'
BUCKET = '/gs/' + app_identity.get_default_gcs_bucket_name()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        allobj = listing()
        template_values = {
                'listing' : allobj
                }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

#class FileUpload(blobstore_handlers.BlobstoreUploadHandler):
class FileUpload(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('upload.html')
        self.response.write(template.render())

    def post(self):
        filename = self.request.get('filename')
        fileblob = self.request.get('fileToUpload')
        if filename != "" and fileblob != None:
            file_insert(filename, fileblob)

class FileGet(webapp2.RequestHandler):
    def get(self):
        filename = self.request.get('name')
        self.response.headers['Content-Type'] = 'text/plain'
        content = find(filename)
        self.response.write(content)

class FileInfo(webapp2.RequestHandler):
    def get(self):
        filename = self.request.get('name')
        template_info = { 'file' : filename }
        template = JINJA_ENVIRONMENT.get_template('fileinfo.html')
        self.response.write(template.render(template_info))

class FileDelete(webapp2.RequestHandler):
    def get(self):
        filename = self.request.get('name')
        self.response.headers['Content-Type'] = 'text/plain'
        if check(filename):
            remove(filename)
            self.response.write("deleted %s" % filename)
        else:
            self.response.write("File does not exist")

class FileCheck(webapp2.RequestHandler):
    def post(self):
        filename = self.request.get('fname')
        if check(filename):
            self.response.write("File Exists")
        else:
            self.response.write("File Does Not Exist")

application = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/upload',FileUpload),
        ('/read',FileGet),
        ('/check',FileCheck),
        ('/delete',FileDelete),
        ('/file',FileInfo),
        ], debug=True)

def file_insert(key, value):
    FILEPATH = BUCKET + '/' + key
    write_path = files.gs.create(FILEPATH, mime_type='text/plain',
                                             acl='public-read')
    # Write to the file.
    with files.open(write_path, 'a') as fp:
        fp.write(value)

    # Finalize the file so it is readable in Google Cloud Storage.
    files.finalize(write_path)


def check(key):
    path = BUCKET + '/' + key
    try:
        fh = files.open(path, 'r')
    except files.ExistenceError:
        return False
    return True

def find(key):
    path = BUCKET + "/" + key
    response = ''
    with files.open(path, 'r') as fp:
        buf = fp.read(1000000)
        while buf:
            response += buf
            buf = fp.read(1000000)
    return response



def remove(key):
    path = BUCKET + "/" + key
    files.delete(path)

def listing():
    filelist = files.listdir(BUCKET)
    flist = []
    for f in filelist:
        pref, fname = f.split(BUCKET+'/')
        flist.append(fname)
    return flist
