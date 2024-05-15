from pyarabic.araby import strip_tashkeel, normalize_hamza, strip_diacritics
from flask import *
from json import load, dumps
from re import sub, search

with open("Warsh.json","rb") as f:
	c = load(f)

replacement = {
	"Normal": {
		"ے": "ي",
		" +": " ",
		"ٞ": "",
		"۞": ""
	},
	"Top": {
		"ۥ": "",
		"ۦ": "",
		"(يٰ |يٗۖ|يٰۖ|يٰٓ|يٗ)": "ى ",
		"يَٰ": "يا",

		"ذَٰلِك":"ذَلِك",
		"هَٰذ":"هَذ",

		"ـَٔ": "أ",
		"َٰ": "ا",
		"َٓٔ": "ء",
	}
}

app = Flask(__name__)

def replace_s(txt, all=False):
	_l = ["Normal"]
	if all:
		_l.append("Top")

	for x in _l:
		for k,v in replacement[x].items():
			txt = sub(k,v,txt)

	return txt

def _search_s(t):
	_l = []

	for surah in c["السور"]:
		_n = 1
		for ayah in surah["الآيات بالترقيم"]:
			_n +=1
			if search(t, strip_diacritics(strip_tashkeel(replace_s(ayah, True)))):
				_l.append((surah["السورة"], _n, replace_s(ayah)))
				#_l.append((surah["السورة"], _n, replace_s(ayah, True)))
				#_l.append((surah["السورة"], _n, strip_diacritics(strip_tashkeel(replace_s(ayah, True)))))

	return _l


@app.route('/')
def index():
	return send_from_directory(".", "index.html")

@app.route('/search',  methods=["POST"])
def search_s():
	print((request.form))
	if "search" in request.form:
		return dumps(_search_s(request.form["search"]))

	abort(400)

#resources
@app.route("/<path:folder>/<path:path>")
def loads_resource(folder, path):
	if folder in ["fonts"]:
		return send_from_directory(folder, path)
	else:
		abort(404)

app.run(debug=True, host="0.0.0.0", port=8888)