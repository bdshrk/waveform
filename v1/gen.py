import os
import shutil

# audio files input directory
inputdir = os.path.join(os.getcwd(), "input")

# components
componentsdir = os.path.join(os.getcwd(), "components")

# output directory
outdir = os.path.join(os.getcwd(), "output")

validfiles = []

# load template files
header = open(os.path.join(componentsdir, "header.html"), "r").read()
item = open(os.path.join(componentsdir, "item.html"), "r").read()
footer = open(os.path.join(componentsdir, "footer.html"), "r").read()

# recursively search input directory for valid files
for subdir, dirs, files in os.walk(inputdir):
	for file in files:
		if file.endswith(".mp3"):
			validfiles.append(os.path.join(subdir, file))

# clean up and create folders
if os.path.exists(outdir):
    shutil.rmtree(outdir)
os.makedirs(os.path.join(outdir, "assets"), exist_ok=True)
os.makedirs(os.path.join(outdir, "assets/images"), exist_ok=True)
os.makedirs(os.path.join(outdir, "assets/audio"), exist_ok=True)

# create output html
outindex = open(os.path.join(outdir, "index.html"), "a")
outindex.write(header)

for file in validfiles:
	# get filename
	filename = os.path.basename(file).split(".")[0]
	
	# populate command for compressing the input audio for web use
	text_compress = f'ffmpeg -n -i "{file}" "{os.path.join(os.path.join(outdir, "assets/audio"), filename + ".mp3")}"'
	
	# populate command for generating waveform
	text_image = f'ffmpeg -n -i "{file}" -filter_complex "compand=gain=4,showwavespic=s=640x64:colors=white|white[fg];color=black:640x64[bg];[bg][fg]overlay=format=auto,drawbox=x=(iw-w)/2:y=(ih-h)/2:w=iw:h=1:color=white" -frames:v 1 "{os.path.join(os.path.join(outdir, "assets/images"), filename + ".png")}"'
	
	# execute the commands
	os.system(text_compress)
	os.system(text_image)
	
	# populate item html template and append to output html
	outindex.write(item.replace("FILENAME", filename))

# finalise html and close
outindex.write(footer)
outindex.close()