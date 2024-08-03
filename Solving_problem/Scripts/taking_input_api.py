from bottle import Bottle, run, template, request, post, get

app = Bottle()


@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)


@app.get('/get_data')  # or @route('/login')
def get_data():
    return '''
        <form action="/see_data" method="post">
            name: <input name="name" type="text" />
            age: <input name="age" type="text" />
            <input value="Send Data" type="submit" />
        </form>
    '''


@app.post('/see_data')  # here we input data
def see_data():
    name = request.forms.get('name') 
    age = request.forms.get('age') 
    return f"<p> Your information is: {name} and {age}"


run(app, host='localhost', port=8080)
