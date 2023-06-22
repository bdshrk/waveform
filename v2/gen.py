import os
import shutil

# num of samples for visualisation
samples=200

# sample rate of mp3
hz_sample_rate=44100

# audio files input directory
dir_input = os.path.join(os.getcwd(), "input")

# components
dir_comp = os.path.join(os.getcwd(), "components")

# output directory
dir_out = os.path.join(os.getcwd(), "output")

valid_files = []

# load template files
header = open(os.path.join(dir_comp, "header.html"), "r").read()
item = open(os.path.join(dir_comp, "item.html"), "r").read()
footer = open(os.path.join(dir_comp, "footer.html"), "r").read()

# recursively search input directory for valid files
for sub_dir, dirs, files in os.walk(dir_input):
	for file in files:
		if file.endswith(".mp3"):
			valid_files.append(os.path.join(sub_dir, file))

# clean up and create folders
if os.path.exists(dir_out):
    shutil.rmtree(dir_out)
os.makedirs(os.path.join(dir_out, "assets"), exist_ok=True)
os.makedirs(os.path.join(dir_out, "assets/data"), exist_ok=True)
os.makedirs(os.path.join(dir_out, "assets/audio"), exist_ok=True)

# create output html
out_index = open(os.path.join(dir_out, "index.html"), "a")
out_index.write(header)

for file in valid_files:
	# get filename
	filename = os.path.splitext(os.path.basename(file))[0]
	
	# populate command for compressing the input audio for web use
	text_compress = f'ffmpeg -n -i "{file}" "{os.path.join(os.path.join(dir_out, "assets/audio"), filename + ".mp3")}"'

	# length calculation command
	com_length = f'ffprobe -i "{file}" -show_entries format=duration -v quiet -of csv="p=0"'
	length = float(os.popen(com_length).read())

	# calculate samplerate given length an no. of samples
	sample_rate = length/samples * hz_sample_rate

	# rms calculation command
	com_rms = f'ffmpeg -v quiet -i "{file}" -af aresample={hz_sample_rate},asetnsamples={sample_rate},astats=metadata=1:reset=1:length=0.05,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=- -f null -'
	rms = os.popen(com_rms).read()

	# create output data file
	data_file = open(os.path.join(os.path.join(dir_out, "assets/data"), filename + ".txt"), "a")

	# extract only numeric value from output
	rms_string = ""
	for line in rms.splitlines():
		if line.count("RMS_level") == 0:
			continue
		rms_string += (line.split("=")[1] + "\n")
	
	# remove final newline
	rms_string = rms_string[:-1]
	data_file.write(rms_string)
	data_file.close()

	# copy audio to output
	shutil.copy(file, os.path.join(os.path.join(dir_out, "assets/audio"), filename + ".mp3"))
	
	# populate item html template and append to output html
	out_index.write(item.replace("FILENAME", filename))

# finalise html and close
out_index.write(footer)
out_index.close()

# copy script
shutil.copy(os.path.join(dir_comp, "player.js"), os.path.join(dir_out, "player.js"))

print("Done!")