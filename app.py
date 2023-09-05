from flask import Flask, request, render_template, session, redirect, url_for
from flask_restful import Api, Resource
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_oauthlib.client import OAuth
from PIL import Image
import io

app = Flask(__name__)
# Change this to a strong secret key
app.config['SECRET_KEY'] = 'your-secret-key'
# Replace with your Google OAuth client ID
app.config['GOOGLE_ID'] = '870824753329-kiknf1l597beiuk9661tijiqb1q48mf7.apps.googleusercontent.com'
# Replace with your Google OAuth client secret
app.config['GOOGLE_SECRET'] = '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'
oauth = OAuth(app)
api = Api(app)

# Create a limiter for API rate limiting (5 requests per minute per IP)
# default_limits=["5 per minute"]
# app,
limiter = Limiter(
    key_func=get_remote_address
)

# Google OAuth setup
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@app.route('/')
def home():
    return render_template('index.html')


class ImageUpload(Resource):
    def post(self):
        # Handle image upload logic here
        # You can save the image and return its name
        uploaded_image = request.files['file']
        # Save the image and return its name
        # Example: save_image(uploaded_image)
        return {'message': 'Image uploaded successfully', 'filename': uploaded_image.filename}


api.add_resource(ImageUpload, '/upload')


@app.route('/image/<filename>')
def show_image(filename):
    return render_template('image_zoom.html', filename=filename)


@app.route('/zoom/<filename>')
def zoom_image(filename):
    return render_template('zoom.html', filename=filename)


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

# Google OAuth callback route


@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    print(user_info)
    session['user_info'] = user_info.data

    return redirect(url_for('home'))


# Google OAuth logout route


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('user_info', None)
    return redirect(url_for('home'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# ... (Zoom functionality - see Step 4)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
