# All paths are relative to train_val.py file
config = {
	'images_path': 'train_val_data/Flickr8k_Dataset/', #Make sure you put that last slash(/)
	'train_data_path': 'train_val_data/Flickr_8k.trainImages.txt',
	'val_data_path': 'train_val_data/Flickr_8k.devImages.txt',
	'captions_path': 'train_val_data/Flickr8k.token.txt',
	'tokenizer_path': 'model_data/tokenizer.pkl',
	'model_data_path': 'model_data/', #Make sure you put that last slash(/)
	'model_load_path': 'model_data/model_inceptionv3_epoch-20_train_loss-2.3365_val_loss-2.8391.hdf5',
	'num_of_epochs': 20,
	'max_length': 40, #This is set manually after training of model and required for test.py
	'batch_size': 64,
	'beam_search_k':3,
	'test_data_path': 'test_data/', #Make sure you put that last slash(/)
	'model_type': 'inceptionv3', # inceptionv3 or vgg16
	'random_seed': 1035,
	'errmsg_imgopen' : "오류: 이미지를 불러올 수 없습니다. 이미지 경로와 확장자가 맞는지 확인해주세요.",
}

rnnConfig = {
	'embedding_size': 300,
	'LSTM_units': 256,
	'dense_units': 256,
	'dropout': 0.3
}