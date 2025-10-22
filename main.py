from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="name of the video is required", required=True)
video_put_args.add_argument(
    "views", type=int, help="views of the video are required", required=True)
video_put_args.add_argument(
    "likes", type=int, help="likes on the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument(
    "name", type=str, help="name of the video", required=False)
video_update_args.add_argument(
    "views", type=int, help="views of the video", required=False)
video_update_args.add_argument(
    "likes", type=int, help="likes on the video", required=False)

videos = {}


def abort_video_id_doesnt_exists(video_id):
    if video_id not in videos:
        abort(404, message="video id does not exists..")


def abort_if_video_exists(video_id):
    if video_id in videos:
        abort(409, message="video with that id already exists..")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Vidoes does not exists with that id')
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id is taken...")
        video = VideoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Vidoes does not exists with that id')
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        db.session.commit()
        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Vidoes does not exists with that id')
        db.session.delete(result)
        db.session.commit()
        return '', 204


api.add_resource(Video, "/video/<int:video_id>")


# @app.route("/")
# def home():
#     return "home"


# @app.route("/get-user/<user_id>")
# def get_user(user_id):
#     user_date = {
#         "name": "Jhon Does",
#         "email": "jhon.doe@gmail.com",
#         "user_id": user_id
#     }
#     extra = request.args.get("extra")
#     if extra:
#         user_date["extra"] = extra
#         return jsonify(user_date), 200
#     else:
#         return jsonify({"error": "Invalid query string params"}), 400


# @app.route("/create-user", methods=["POST"])
# def create_user():
#     data = request.get_json()
#     if data:
#         return jsonify(data), 200
#     else:
#         return jsonify({"error": "user data in body is empty"}), 400


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
