from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask import render_template
from flask import send_from_directory
import DatabaseModels
import DatabaseSession

MAX_NUMBER_OF_NODES = 20

app = Flask(__name__)
api = Api(app)


all_people = {"name": "People",
              "img": "/static/people.jpg",
              "children": [
                  {
                      "name": "Known People",
                      "img": "/static/known.png",
                      "children": []
                  },
                  {
                      "name": "Unknown People",
                      "img": "/static/unknown.jpg",
                      "children": []
                  },
                  {
                      "name": "Unknown Groups",
                      "img": "/static/group.jpg",
                      "children": []
                  }
              ]}
for row in DatabaseSession.session.query(DatabaseModels.Knows).all():
    exists = False
    tmpPerson = {"name": row.name,
                 "img": "http://localhost:5001/image" + row.path,
                 "video":row.video.video_path,
                 "children": []}
    for person in all_people["children"][0]["children"]:
        if person["name"] == row.name:
            exists = True
            if len(person["children"]) > MAX_NUMBER_OF_NODES:
                break
            person["children"].append(tmpPerson)
            break
    if not exists:
        all_people["children"][0]["children"].append(tmpPerson)

for row in DatabaseSession.session.query(DatabaseModels.Unknows).all():
    if len(all_people["children"][1]["children"]) > MAX_NUMBER_OF_NODES:
        break
    all_people["children"][1]["children"].append({"name": row.alias,
                            "img": "http://localhost:5001/image" + row.path,
                            "video":row.video.video_path})

for row in DatabaseSession.session.query(DatabaseModels.Wishper).all():
    exists = False
    tmpPerson = {"name": "Group: " + row.group + " Alias: " + row.alias,
                 "img": "http://localhost:5001/image" + row.path,
                 "video":row.video.video_path,
                 "group":row.group,
                 "children": [],
                 "_children": []}

    for person in all_people["children"][2]["children"]:
        if person["group"] == row.group:
            exists = True
            if len(person["children"]) > MAX_NUMBER_OF_NODES:
                break
            person["children"].append(tmpPerson)
            break
    if not exists:
        all_people["children"][2]["children"].append(tmpPerson)

@app.route('/image/<path:filename>')
def image(filename):
    # Change this!!!!!!!!
    # PATH Trasversal VULNERABILITY
    return send_from_directory("/", filename)


class User(Resource):
    def get(self):
        return all_people, 200

class Home(Resource):
    def get(self):
        resp = app.make_response(render_template('index.html', name="Unknows"))
        resp.mimetype = "text/html"
        return resp

api.add_resource(User, "/data")
api.add_resource(Home, "/")


app.run(host='127.0.0.1',port=5001,  debug=True)
