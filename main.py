import src.generator as gen

if __name__ == '__main__':
	
	feature_names = ['el_e',
					'mu_e'
					]

	sample_dir_path = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2/mc20_Run2/Ntuples/PeriodE/ZJets_MG'

	generator = gen.Generator(sample_dir_path=sample_dir_path, feature_names=feature_names)

	samples = gen.generate(N=None)
