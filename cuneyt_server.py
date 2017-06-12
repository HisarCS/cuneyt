from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/assistant',methods=['POST'])
def assistant_command():
  try:
    print request.data
  except Exception as e:
    print e
  return "baban"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
