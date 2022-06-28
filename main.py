from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# initialise app and wrap it in API object
app = Flask(__name__)
api = Api(app)

# configure and initialise database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False) # 100 is max name length, nullable=False makes this a required field
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name={name}, views={views}, likes={likes})"

# create database
# ONLY TO BE RUN ONCE
#db.create_all()

# initialise a request parser and add required arguments
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of video is required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)

# define resource fields
resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

# define the Video resource to add to the API
class Video(Resource):

	# define GET request response behaviour
	@marshal_with(resource_fields) # needed to serialize instance of VideoModel
	def get(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		
		# check if video is not in db and abort if so
		if not result:
			abort(404, message="Video id not found!")
		return result

	# define PUT request response behaviour
	@marshal_with(resource_fields) # needed to serialize instance of VideoModel
	def put(self, video_id):
		args = video_put_args.parse_args()
		
		# check if video already exists and abort if so
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video id taken!")

		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		db.session.add(video) # adds this VideoModel to the db session
		db.session.commit() # commits db session to permanency
		return video, 201

	def patch(self, video_id):
		pass

	# define DELETE request response behaviour 
	def delete(self, video_id):
		abort_video_not_found(video_id)
		del videos[video_id]
		return "", 204


# add the Video resource to API
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)