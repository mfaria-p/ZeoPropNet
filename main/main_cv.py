
import sys  # For accessing command-line arguments
import time
import os
from os import path
import numpy as np
import datetime

sys.path.append('/main')
from model import build_model
from data import get_data_one
from model import train_model, save_model, test_model

#You can use this to write Python programs which can be customized by end users easily.
def read_config(file_path):
    import configparser  # For reading and parsing the configuration file
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def input_to_bool(txt):
	#This function converts a raw_input string to a booolean
	return txt.lower() in ['yes', 'true', 'y', 't', '1']

########### RECEIVING THE ARGUMENTS FROM THE COMMAND LINE ##########################################
if __name__ == '__main__':#to designate a section of code that should only be executed 
	#when the script is run directly, not when it is imported as a module in another script.
	if len(sys.argv) < 2:
		print('Usage: {} "settings.cfg"'.format(sys.argv[0])) #ve se tem dois args
		#aka mostra o usage dos argumentos quando se corre o codigo, my script nd the configuration file
		print(sys.argv[0])
		quit(1)

	# Load settings
	try:
	#Once the configuration file is read, the ConfigParser object (config) stores the data in a dictionary-like structure. 
    #Sections in the configuration file are represented as keys, and the settings within each section are stored as nested dictionaries.
		config = read_config(sys.argv[1])
	except:
		print('Could not read config file {}'.format(sys.argv[1]))
		quit(1)

	# Get model label
	#I think this is where the output of the model will put
	#or maybe where the model will get its input
	try:
		fpath = config['IO']['model_fpath']
	except KeyError:
		print('Must specify model_fpath in IO in config')
		quit(1)
	
	########## DEFINE THE DATA ##############################################
	data_kwargs = config['DATA']
	#Some configuration libraries (e.g., configparser in Python) might include the section name (__name__) under each key 
    # when parsing a config file. This key typically isn't needed when working with the actual configuration parameters 
    # and might be removed to avoid issues or conflicts when the data_kwargs dictionary is used later in the code.
	if '__name__' in data_kwargs:
		del data_kwargs['__name__'] #  from configparser
	if 'batch_size' in config['TRAINING']:
		data_kwargs['batch_size'] = config['TRAINING']['batch_size']
	if 'shuffle_seed' in data_kwargs:
	#If shuffle_seed is provided in the configuration, it is converted to an integer and used.
	#If shuffle_seed is not provided, the current time (in seconds since the epoch) is used as a seed. 
	#This ensures that each run uses a different seed, leading to different shuffles each time.
		data_kwargs['shuffle_seed'] = data_kwargs['shuffle_seed']
	else:
		data_kwargs['shuffle_seed'] = str(time.time())
	
	if 'cv_folds' in data_kwargs:
		try:
			#create the directory specified by the directory part of fpath.
			os.makedirs(os.path.dirname(fpath))
		except: # folder exists
			pass
		if '<this_fold>' in data_kwargs['cv_folds']:#checks if the string '<this_fold>' is present in the value associated with the key 'cv_folds'.
			cv_folds = data_kwargs['cv_folds']
			#Splits the cv_folds string by the '/' character.
			#Takes the second part of the split (index [1]), which represents the total number of folds.
			total_folds = int(cv_folds.split('/')[1])
			#Uses a list comprehension to generate a list of strings in the format 1/total_folds, 2/total_folds, ..., total_folds/total_folds.
			all_cv_folds = ['{}/{}'.format(i + 1, total_folds) for i in range(total_folds)]
		else:
			all_cv_folds = [data_kwargs['cv_folds']]

	# Iterate through all folds
	ref_fpath = fpath
	for cv_fold in all_cv_folds:

		###################################################################################
		### BUILD MODEL
		###################################################################################

		print('...building model')
		try:
			kwargs = config['ARCHITECTURE']
			if '__name__' in kwargs: del kwargs['__name__'] #  from configparser
			if 'batch_size' in config['TRAINING']:
				#se houver mais do que um batch (ou seja processarmos um numero de amostras do total a testar por vez),
				#entao o padding (some adjustments) é necessario
				kwargs['padding'] = str(int(config['TRAINING']['batch_size']) > 1) 
			if 'sum_after' in kwargs:
				kwargs['sum_after'] = str(input_to_bool(kwargs['sum_after']))

			model = build_model(**kwargs)
			print('...built untrained model {}'.format(cv_fold))

		except KeyboardInterrupt:
			print('User cancelled model building')
			quit(1)

		print('Using CV fold {}'.format(cv_fold))
		data_kwargs['cv_folds'] = cv_fold
		#updates the file path fpath by replacing the placeholder '<this_fold>' with the actual fold number.
		fpath = ref_fpath.replace('<this_fold>', cv_fold.split('/')[0])
		#get data for current fold
		data = get_data_one(**data_kwargs)

		###################################################################################
		### LOAD WEIGHTS?
		###################################################################################

		if 'weights_fpath' in config['IO']:
			weights_fpath = config['IO']['weights_fpath']
		else:
			weights_fpath = fpath + '.weights.h5'

		try:
			use_old_weights = input_to_bool(config['IO']['use_existing_weights'])
		except KeyError:
			print('Must specify whether or not to use existing model weights')
			quit(1)

		if use_old_weights and os.path.isfile(weights_fpath):
			model.load_weights(weights_fpath)
			print('...loaded weight information')

			# Reset final dense?
			if 'reset_final' in config['IO']:
				if config['IO']['reset_final'] in ['true', 'y', 'Yes', 'True', '1']:
					layer = model.layers[-1]
					layer.W.set_value((layer.init(layer.W.shape.eval()).eval()).astype(np.float32))
					layer.b.set_value(np.zeros(layer.b.shape.eval(), dtype=np.float32))

		elif use_old_weights and not os.path.isfile(weights_fpath):
			print('Weights not found at specified path {}'.format(weights_fpath))
			quit(1)
		else:
			pass

		###################################################################################
		### TRAIN THE MODEL
		###################################################################################

		# Train model
		try:
			print('...training model')
			kwargs = config['TRAINING']
			if '__name__' in kwargs:
				del kwargs['__name__'] #  from configparser
			(model, loss, val_loss) = train_model(model, data, **kwargs)
			print('...trained model')
		except KeyboardInterrupt:
			pass
	
		###################################################################################
		### SAVE MODEL
		###################################################################################

		# Get the current time
		tstamp = datetime.datetime.utcnow().strftime('%m-%d-%Y_%H-%M')
		print('...saving model')
		save_model(model, 
			loss,
			val_loss,
			fpath = fpath,
			config = config, 
			tstamp = tstamp)
		print('...saved model')

		###################################################################################
		### TEST MODEL
		###################################################################################

		print('...testing model')
		data_withresiduals = test_model(model, data, fpath, tstamp = tstamp,
			batch_size = int(config['TRAINING']['batch_size']))
		print('...tested model')