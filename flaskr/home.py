from flask import Flask, render_template, flash, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow import keras
from werkzeug import secure_filename
from keras.preprocessing.image import ImageDataGenerator    
import numpy as np
import os 

UPLOAD_FOLDER = '/home/amel/Documents/Move later/flask_project/web_choco_rec/flaskr/test'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
model = tf.keras.models.load_model('model.h5')
app = Flask(__name__)
# model = keras.models.load_model("assets/price_prediction_model.h5")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/uploader', methods = ['POST'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        test_dir = os.path.join(UPLOAD_FOLDER , f.filename)
        images = []
        images.append(f)
        predict_class(model, images, True)
        return predict_class

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            images = []
            images.append(filename)
            predict_class(model, images, True)
            return predict_class
            # return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
        '''          

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_class(model, images, show = True):
  for img in images:
    img = image.load_img(img, target_size=(299, 299))
    img = image.img_to_array(img)                    
    img = np.expand_dims(img, axis=0)         
    img /= 255.                                      

    pred = model.predict(img)
    index = np.argmax(pred)
    food_list = ['apple_pie','baby_back_ribs','baklava','beef_carpaccio','beef_tartare','beet_salad'
                'beignets','bibimbap','bread_pudding','breakfast_burrito','bruschetta','caesar_salad','cannoli'
                'caprese_salad','carrot_cake','ceviche','cheese_plate','cheesecake','chicken_curry','chicken_quesadilla'
                'chicken_wings','chocolate_cake','chocolate_mousse','churros','clam_chowder',
                'club_sandwich','crab_cakes','creme_brulee','croque_madame','cup_cakes','deviled_eggs','donuts','dumplings','edamame','eggs_benedict',
                'escargots','falafel','filet_mignon','fish_and_chips','foie_gras','french_fries','french_onion_soup','french_toast','fried_calamari','fried_rice'
                'frozen_yogurt','garlic_bread','gnocchi','greek_salad','grilled_cheese_sandwich','grilled_salmon','guacamole','gyoza','hamburger','hot_and_sour_soup',
                'hot_dog','huevos_rancheros','hummus','ice_cream','lasagna','lobster_bisque','lobster_roll_sandwich','macaroni_and_cheese','macarons'
                'miso_soup','mussels','nachos','omelette','onion_rings','oysters','pad_thai','paella','pancakes','panna_cotta','peking_duck'
                'pho','pizza','pork_chop','poutine','prime_rib','pulled_pork_sandwich','ramen','ravioli','red_velvet_cake','risotto','samosa','sashimi','scallops'
                'seaweed_salad','shrimp_and_grits','spaghetti_bolognese','spaghetti_carbonara','spring_rolls','steak','strawberry_shortcake','sushi'
                'tacos','takoyaki','tiramisu','tuna_tartare','waffles']
    food_list.sort()
    pred_value = food_list[index]
    return pred_value
    # if show:
    #     plt.imshow(img[0])                           
    #     plt.axis('off')
    #     plt.title(pred_value)
    #     plt.show()


if __name__ == '__main__':
    app.debug = True
    app.run()    