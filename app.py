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

if __name__ == '__main__':
    app.run(debug=True)