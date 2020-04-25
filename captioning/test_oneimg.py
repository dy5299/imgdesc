import numpy as np
from pickle import load
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from utils.model import CNNModel, generate_caption_beam_search
import os

from config import config



# for thread error
import keras.backend.tensorflow_backend as tb
tb._SYMBOLIC_SCOPE.value = True


# for initialize memory
# status initialize
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0' # 초기화할 GPU number
# out of memory
import tensorflow as tf
with tf.Graph().as_default():
  gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)


"""
    *Some simple checking
"""
assert type(config['max_length']) is int, 'Please provide an integer value for `max_length` parameter in config.py file'
assert type(config['beam_search_k']) is int, 'Please provide an integer value for `beam_search_k` parameter in config.py file'

# Extract features from each image in the directory
def extract_features(filename, model, model_type):
	if model_type == 'inceptionv3':
		from keras.applications.inception_v3 import preprocess_input
		target_size = (299, 299)
	elif model_type == 'vgg16':
		from keras.applications.vgg16 import preprocess_input
		target_size = (224, 224)
	# Loading and resizing image
	try: image = load_img(filename, target_size=target_size)
	except: return []
	# Convert the image pixels to a numpy array
	image = img_to_array(image)
	# Reshape data for the model
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
	# Prepare the image for the CNN Model model
	image = preprocess_input(image)
	# Pass image into model to get encoded features
	features = model.predict(image, verbose=0)
	return features

def run_captioning(image_file):
#	import datetime
#	today = datetime.date.today()
#	image_file = '/home/lab02/imgdesc/django/media/' + '{:/%Y%m/%d/}'.format(today) + image_file_name
	# Load the tokenizer
	tokenizer_path = config['tokenizer_path']
	tokenizer = load(open(tokenizer_path, 'rb'))

	# Max sequence length (from training)
	max_length = config['max_length']

	# Load the model
	caption_model = load_model(config['model_load_path'])

	image_model = CNNModel(config['model_type'])

	# Load and prepare the image
#	if (image_file.split('.')[1] == 'jpg' or image_file.split('.')[1] == 'jpeg'):
	try:
		# Encode image using CNN Model
		image = extract_features(image_file, image_model, config['model_type'])

	except:
		return (config['errmsg_imgopen'] + '.')
	try:

		if len(image) == 0:
			return(config['errmsg_imgopen'] + '')
		# Generate caption using Decoder RNN Model + BEAM search
		generated_caption = generate_caption_beam_search(caption_model, tokenizer, image, max_length,
														 beam_index=config['beam_search_k'])
	except:
		return (config['errmsg_imgopen'] + '..')
	try:
		# Remove startseq and endseq
		desc_en = generated_caption.split()[1].capitalize()
		for x in generated_caption.split()[2:len(generated_caption.split()) - 1]:
			desc_en = desc_en + ' ' + x
		desc_en += '.'

	except:
		return (config['errmsg_imgopen'] + '...')
	try:
		# Show image and its caption
		print('BEAM Search with k=', config['beam_search_k'])
		return (desc_en)
	#	print(desc_ko,'\n\n')
	except:
		return(config['errmsg_imgopen']+'....')

# Translation
import urllib.request
def translation(input):
	client_id = "9eIZqLhZraxAoH9VlCNL"  # 개발자센터에서 발급받은 Client ID 값
	client_secret = "DtPF330iLN" # 개발자센터에서 발급받은 Client Secret 값
	encText = urllib.parse.quote(input)
	data = "source=en&target=ko&text=" + encText
	url = "https://openapi.naver.com/v1/papago/n2mt"
	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id",client_id)
	request.add_header("X-Naver-Client-Secret",client_secret)
	response = urllib.request.urlopen(request, data=data.encode("utf-8"))
	rescode = response.getcode()
	if(rescode==200):
		response_body = response.read()
		return(response_body.decodepppp('utf-8'))
	else:
		return("Error Code:" + rescode)

def testimport(input):
	output=input+' and nice'
	return(output)

if __name__ == '__main__':
	import argparse
	ap = argparse.ArgumentParser()
	ap.add_argument('-i', '--image', required=True, help="Image Path")
	args = vars(ap.parse_args())
	img_path = args['image']

	myresult=run_captioning(img_path)
	print(myresult)
#	print(translation(myresult))
