from app import app

@app.route('/test-page-many-files')
def index():
    return 'Hello World!'