from flask import Flask, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configure Rate Limiting
# app,
#     default_limits=["5 per minute"]
limiter = Limiter(

    key_func=get_remote_address
)

# Routes for the interface


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/image_upload', methods=['POST'])
@limiter.limit("5 per minute")
def image_upload():
    if 'image' in request.files:
        image = request.files['image']
        # Process the image here
        return render_template('image_result.html', image_name=image.filename)
    return "Image not found.", 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    # app.run(debug=True)
