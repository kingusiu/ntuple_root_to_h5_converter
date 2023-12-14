import os
import src.reader as read

class Generator:

    def __init__(self, sample_dir_path:string, feature_names:list):
        """docstring for init"""
        self.feature_names = feature_names
        self.sample_dir_path = sample_dir_path

    def generate(self,N:int) -> np.ndarray:
    	
    	reader = read.reader(feature_names=self.feature_names)

    	files = os.listdir(self.sample_dir_path).sort()

    	# keep data in lists for performance
    	samples_concat = []

    	# iterate through all files
    	for ff in files:
    		
    		# read samples from a single file
    		samples = reader.read_file(file_path=ff)
    		# apply selection cuts
    		selected_samples = selection.select(samples)
    		samples_concat.extend(selected_samples)

    		# yield next chunk of N
    		while (len(samples_concat) >= N):
    			# slice chunk
    			samples_chunk = samples_concat[:N]
    			samples_concat = samples_concat[N:]
    			# yield numpy array of size N x num_features
    			yield np.asarray(samples_chunk)



