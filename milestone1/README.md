
If surprise libarary is not installed, please install it first:
	
	pip3 install scikit-surprise

# Separate training and prediction

First, train the model with dataset once:

	python3 milestone1_training.py

It will generate a trained model file and combine all training data into a single file.
Then run predictions repeatly by accepting user ids:

	python3 milestone1_prediction.py [user_id]
	
It will print out recommended list of 20 movies
