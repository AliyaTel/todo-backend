from flask import Flask, request
from resources import EntryManager, Entry

app = Flask(__name__)


FOLDER = r"C:\Users\Aliya\Documents"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/entries/")
def get_entries():
    entry1 = EntryManager(FOLDER)
    entry1.load()
    list_entries = []
    for i in entry1.entries:
        list_entries.append(i.json())

    return list_entries


@app.route('/api/save_entries/', methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    dict_of_entries = request.get_json()
    for i in dict_of_entries:
        ok = Entry.from_json(i)
        entry_manager.entries.append(ok)

    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)