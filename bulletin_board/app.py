from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db.init_app(app)


class AdvertismentModel(db.Model):
    __tablename__ = 'Advs'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50))
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, author, title, description):
        self.author = author
        self.title = title
        self.description = description

    def to_dict(self):
        return {"author": self.author,
                "title": self.title,
                "description": self.description,
                "date": self.date
                }

    def to_dict_wd(self):
        return {"author": self.author,
                "title": self.title,
                "description": self.description,
                }


@app.before_first_request
def create_table():
    db.create_all()


class AdvertismentsView(Resource):

    def get(self):
        advs = AdvertismentModel.query.all()
        return jsonify([adv.to_dict() for adv in advs])

    def post(self):
        data = request.get_json()
        print(data)
        data = request.json
        print(data)
        new_adv = AdvertismentModel(data['author'],
                                    data['title'],
                                    data['description'])
        db.session.add(new_adv)
        db.session.commit()
        return new_adv.to_dict_wd(), 201


class AdvertismentView(Resource):

    def get(self, adv_id):
        adv = AdvertismentModel.query.get(adv_id)
        if adv:
            return jsonify(adv.to_dict())
        return {'message': 'adv not found'}, 404

    def put(self, adv_id):
        data = request.get_json()

        adv = AdvertismentModel.query.get(adv_id)

        if adv:
            adv.title = data["title"]
            adv.description = data["description"]
        else:
            adv = AdvertismentModel(id=adv_id, **data)

        db.session.add(adv)
        db.session.commit()

        return jsonify(adv.to_dict())

    def delete(self, adv_id):
        adv = AdvertismentModel.query.get(adv_id)
        if adv:
            db.session.delete(adv)
            db.session.commit()
            return {'message': 'Deleted'}
        else:
            return {'message': 'adv not found'}, 404


api.add_resource(AdvertismentsView, '/api/v1/advs/')
api.add_resource(AdvertismentView, '/api/v1/adv/<int:adv_id>')

app.debug = True


if __name__ == '__main__':
    app.run(host='localhost', port=5555)
