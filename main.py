import src.generator as gen
import src.selection as sel


if __name__ == '__main__':
	
	feature_names = ['el_e',
					'mu_e',
					'jet_e'
					]

	sample_dir_path = '/eos/atlas/atlascerngroupdisk/perf-flavtag/calib/negtag/Rel24_GN2/mc20_Run2/Ntuples/PeriodE/ZJets_MG'

	# read single file

	# generator = gen.Generator(sample_dir_path=sample_dir_path, feature_names=feature_names)
	# samples = gen.generate(N=None)

	samples_lightjet = sel.select(samples)
