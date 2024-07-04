import subprocess
from flask import Flask, jsonify, render_template
import os ;
from flask import request

#app = Flask(__name__)

#@app.route('/')
#def home():
#    return render_template('index.html')

#if __name__ == '__main__':
#    app.run(debug=True)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')





@app.route('/gitlab')
def gitlab():
    return render_template('gitlab.html')

@app.route('/env-cnx')
def envcnx():
    return render_template('conex-env.html')



@app.route('/run_script', methods=['POST'])
def run_script():
    token = request.form.get('token')
    url = request.form.get('url')
    project_title = request.form.get('projectTitle')
    group = request.form.get('group')

  
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'gitlab_repo.py')
    try:
        try:
            result = subprocess.run([ script_path, '-t', token, '-u', url, '-p', project_title, '-g', group], capture_output=True, text=True, check=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.stderr}"
    
        return jsonify({'output': output})
    except Exception as e:
       
        return jsonify({'error': str(e)}), 500

@app.route('/add_users', methods=['POST'])
def add_users():
    token = request.form.get('token')
    url = request.form.get('url')
    project_title = request.form.get('projectTitle')
    emails = request.form.get('emails')
    roles = request.form.get('roles')

  
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'add_users_project.py')
    try:
        try:
            result = subprocess.run([ script_path, '-t', token, '-u', url, '-p', project_title, '-e', emails , '-r' , roles], capture_output=True, text=True, check=True)
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.stderr}"
    
        return jsonify({'output': output})
    except Exception as e:
     
        return jsonify({'error': str(e)}), 500
    
@app.route('/test_ssh', methods=['POST'])
def test_ssh():
    host = request.form.get('host')
    port = request.form.get('port')
    username = request.form.get('username')
    password = request.form.get('password')

    script_path = os.path.join(os.path.dirname(__file__), 'scripts','test_ssh_con.py')
    try:
        try:
            result = subprocess.run(
                [ script_path, '-s', host, '-u', username, '-p', password, '-d', port],
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.stderr}"

        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/versions', methods=['GET'])
def get_versions():
    php_versions = ["php5.6", "php7.0", "php7.1", "php7.2", "php7.3", "php7.4", "php8.0", "php8.1" ,"php8.2","php8.3"]
    
    composer_versions = [
        "2.0.0", "2.0.1", "2.0.2", "2.0.3", "2.0.4", "2.0.5", "2.0.6", "2.0.7", "2.0.8", "2.0.9", "2.0.10", 
        "2.1.0", "2.1.1", "2.1.2", "2.1.3", "2.1.4", "2.1.5", "2.1.6", "2.1.7", "2.1.8", "2.1.9", "2.1.10",
        "2.2.0", "2.2.1", "2.2.2", "2.2.3", "2.2.4", "2.2.5", "2.2.6", "2.2.7", "2.2.8", "2.2.9", "2.2.10", 
        "2.3.0", "2.3.1", "2.3.2", "2.3.3", "2.3.4", "2.3.5", "2.3.6", "2.3.7", "2.3.8", "2.3.9", "2.3.10",
        "2.4.0", "2.4.1", "2.4.2", "2.4.3", "2.4.4", "2.4.5", "2.4.6", "2.4.7", "2.4.8", "2.4.9", "2.4.10",
        "2.5.0", "2.5.1", "2.5.2", "2.5.3", "2.5.4", "2.5.5", "2.5.6", "2.5.7", "2.5.8", "2.5.9", "2.5.10",
        "2.6.0", "2.6.1", "2.6.2", "2.6.3", "2.6.4", "2.6.5", "2.6.6", "2.6.7", "2.6.8", "2.6.9", "2.6.10",
        "2.7.0", "2.7.1", "2.7.2", "2.7.3", "2.7.4", "2.7.5", "2.7.6", "2.7.7"
    ]
    web_servers =["apache" , "nginx"]
    return jsonify({"php_versions": php_versions, "composer_versions": composer_versions , "web_servers" : web_servers})














if __name__ == '__main__':
    app.run(debug=True)