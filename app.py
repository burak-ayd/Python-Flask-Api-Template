import os
import uuid
from flask import Flask, request, jsonify, abort
import urllib.request
import generate_api_key
from functools import wraps

app = Flask(__name__)

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
host=external_ip
PROJECT_HOME = '/var/www/html'
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def get_api_key():
    return generate_api_key()

def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.args.get('api_key') and request.args.get('api_key') == get_api_key():
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1.0/get_all/api', methods=['GET'])
@require_appkey
def get():
    pass

@app.route('/api/v1.0/post/api', methods=['POST'])
@require_appkey
def post():
    pass

@app.route('/api/v1.0/get/<int:id>/api', methods=['GET'])
@require_appkey
def get_post(id):
    pass
@app.route('/api/v1.0/put/<int:id>/api', methods=['PUT'])
@require_appkey
def put_post(id):
    pass
@app.route('/api/v1.0/delete/<int:id>/api', methods=['DELETE'])
@require_appkey
def delete_post(id):
    pass

app.route('/api/v1.0/upload/api', methods=['POST', 'GET'])
@require_appkey
def upload_file():
    if request.method =='POST':
        try:
            file = request.files.get('files[]')
            _tmp=str(uuid.uuid4())
            ext=file.filename.rsplit('.', 1)[1].lower()
            new_image='http://'+host+'/uploads/'+_tmp+"."+ext
            errors = {}
            success = False     
            if file and allowed_file(file.filename):
                
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], _tmp+"."+ext))
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'
            if success and errors:
                errors['message'] = 'File(s) successfully uploaded'
                resp = jsonify(errors)
                resp.status_code = 500
                return resp
            if success:
                resp = jsonify({'message' : 'Files successfully uploaded'})
                resp.status_code = 201
                return resp
            else:
                resp = jsonify(errors)
                resp.status_code = 500
                return resp
        except Exception as e:
            print(e)
        
    if request.method == 'GET':
        return jsonify({'message' :app.config['UPLOAD_FOLDER']}), 200
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)