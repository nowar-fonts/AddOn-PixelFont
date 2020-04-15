import json
import codecs
from functools import reduce
from itertools import product
from types import SimpleNamespace as Namespace

class Config:
	version = "1.000"
	fontRevision = 1.0
	vendor = "Nowar Typeface"
	vendorId = "NOWR"
	vendorUrl = "https://github.com/nowar-fonts"
	copyright = "Copyright © 2019—2020 Cyano Hao and Nowar Typeface. Portions Copyright 2015 Google Inc. Portions © 2014-2019 Adobe (http://www.adobe.com/)."
	designer = "Cyano Hao (character set definition, autohinting & modification for World of Warcraft); Monotype Design Team (Latin, Greek & Cyrillic); Ryoko NISHIZUKA 西塚涼子 (kana, bopomofo & ideographs); Sandoll Communications 산돌커뮤니케이션, Soo-young JANG 장수영 & Joo-yeon KANG 강주연 (hangul elements, letters & syllables); Dr. Ken Lunde (project architect, glyph set definition & overall production); Masataka HATTORI 服部正貴 (production & ideograph elements)"
	designerUrl = "https://github.com/CyanoHao"
	license = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This Font Software is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the SIL Open Font License for the specific language, permissions and limitations governing your use of this Font Software."
	licenseUrl = "https://scripts.sil.org/OFL"

	fontPackWeight = [ 300 ]
	fontPackFeature = []
	instance = [
		('gbk', 'Sans', 'CN', 3),
		('gbk', 'Sans', 'CN', 5),
		('big5', 'Sans', 'TW', 3),
		('big5', 'Sans', 'TW', 5),
		('unspec', 'UI', 'CL', 3),
		('unspec', 'UI', 'CL', 7),
	]

config = Config()

weightMap = {
	100: "Thin",
	200: "ExtraLight",
	300: "Light",
	400: "Regular",
	500: "Medium",
	600: "SemiBold",
	700: "Bold",
	800: "ExtraBold",
	900: "Black",
}

widthMap = {
	3: "Condensed",
	4: "SemiCondensed",
	5: None,
	7: "Extended",
}

notoWidthMap = {
	3: 3,
	5: 4,
	7: 5,
}

morpheusWeightMap = {
	200: 100,
	300: 200,
	400: 500,
	500: 600,
	700: 800,
}

# define font pack orthographies for diffrent WoW language
# Latn -- Chinese characters in European languages, must be defined.
# Hans -- 简体中文; if set to `None`, the font pack will not override 简体中文 font.
# Hans -- 繁體中文, can be `None`.
# ko -- 漢字 in 한국어, can be `None`.
regionalVariant = {
	"CN": {
		"Latn": "CN",
		"Hans": "CN",
		"Hant": "TW",
		"ko": "KR",
	},
	"TW": {
		"Latn": "TW",
		"Hans": "CN",
		"Hant": "TW",
		"ko": "KR",
	},
	"HK": {
		"Latn": "HK",
		"Hans": "CN",
		"Hant": "HK",
		"ko": "KR",
	},
	"JP": {
		"Latn": "JP",
		"Hans": "CN",
		"Hant": "TW",
		"ko": "KR",
	},
	"KR": {
		"Latn": "KR",
		"Hans": "CN",
		"Hant": "TW",
		"ko": "KR",
	},
	"CL": {
		"Latn": "CL",
		"Hans": "CL",
		"Hant": "CL",
		"ko": "CL",
	},
	"GB": {
		"Latn": "GB",
		"Hans": "GB",
		"Hant": "GB",
		"ko": None,
	},
}

# map orthography to source file
regionSourceMap = {
	"CN": "SourceHanSansSC",
	"TW": "SourceHanSansTC",
	"HK": "SourceHanSansHC",
	"JP": "SourceHanSans",
	"KR": "SourceHanSansK",
	"CL": "SourceHanSansK",
	"GB": "SourceHanSansCN",
}

regionNameMap = {
	"CN": "CN",
	"TW": "TW",
	"HK": "HK",
	"JP": "JP",
	"KR": "KR",
	"CL": "Classical",
	"GB": "GB18030",
}

tagNameMap = dict(regionNameMap)
tagNameMap.update({
	"OSF": "Oldstyle",
	"SC": "Smallcaps",
	"RP": "Roleplaying",
})

# set OS/2 encoding to make Windows show font icon in proper language
encoding = [
	"unspec", # 文字美
	"gbk",    # 简体字
	"big5",   # 繁體字
	"jis",    # あア亜
	"korean", # 한글
]

def GetRegion(p):
	if hasattr(p, "region"):
		return p.region
	else:
		return ""

def LocalizedFamily(p):
	if "nameList" not in LocalizedFamily.__dict__:
		LocalizedFamily.nameList = {
			"Sans": {
				0x0409: "War Pixel",
			},
			"UI": {
				0x0409: "War Pixel UI",
			},
		}

	if p.family == "Latin":
		return {
			0x0409: "War Pixel UI LCG",
		}

	isLocalized = {
		0x0804: bool(regionalVariant[p.region]["Hans"]),
		0x0404: bool(regionalVariant[p.region]["Hant"]),
		0x0C04: bool(regionalVariant[p.region]["Hant"]),
		0x0411: bool(regionalVariant[p.region]["Hans"]),
		0x0412: bool(regionalVariant[p.region]["ko"]),
	}

	result = dict(LocalizedFamily.nameList[p.family])
	result.update({ lang: result[0x0409] for lang, local in isLocalized.items() if not local })
	return result

def GetTagList(p):
	if p.family == "Latin":
		tagList = p.feature
	else:
		tagList = [ p.region ] + p.feature
	return tagList

def GetTagStr(p):
	tagList = GetTagList(p)
	return ",".join(tagList)

def TagListToStr(lst):
	return ",".join(lst)

def TagStrToList(s):
	return s.split(",")

def GenerateFamily(p):
	localizedFamily = LocalizedFamily(p)
	tagList = GetTagList(p)
	if len(tagList):
		return {
			lang: localizedFamily[lang] + " " + " ".join([ tagNameMap[tag] for tag in tagList ])
			for lang in localizedFamily
		}
	else:
		return localizedFamily

def GenerateSubfamily(p):
	width = widthMap[p.width]
	weight = weightMap[p.weight]
	if hasattr(p, "italic") and p.italic:
		if p.weight == 400:
			return width + " Italic" if width else "Italic"
		else:
			return ("{} {}".format(width, weight) if width else weight) + " Italic"
	else:
		if p.weight == 400:
			return width if width else "Regular"
		else:
			return "{} {}".format(width, weight) if width else weight

def GenerateFriendlyFamily(p):
	return { k: "{} {}".format(v, GenerateSubfamily(p)) for k, v in GenerateFamily(p).items() }

def GenerateLegacySubfamily(p):
	width = widthMap[p.width]
	weight = weightMap[p.weight]
	if hasattr(p, "italic") and p.italic:
		if p.weight == 400:
			return width or "", "Italic"
		elif p.weight == 700:
			return width or "", "Bold Italic"
		else:
			return "{} {}".format(width, weight) if width else weight, "Italic"
	else:
		if p.weight == 400 or p.weight == 700:
			return width or "", weight
		else:
			return "{} {}".format(width, weight) if width else weight, "Regular"

def GenerateFilename(p):
	if p.family in [ "Sans", "UI", "WarcraftSans", "WarcraftUI" ]:
		encodingPrefix = p.encoding + "-"
		nameList = {
			"Sans": "WarPixel",
			"UI": "WarPixelUI",
		}
		familyName = nameList[p.family] + "-" + GetTagStr(p)
	elif p.family == "Latin":
		encodingPrefix = ""
		nameList = {
			"Latin": "WarPixelLCG",
		}
		familyName = nameList[p.family] + "-" + GetTagStr(p)
	else:
		encodingPrefix = ""
		nameList = {
			"Noto": lambda p: "NotoSans",
			"Source": lambda p: p.region,
		}
		familyName = nameList[p.family](p)
	return encodingPrefix + familyName + "-" + GenerateSubfamily(p).replace(" ", "")

def ResolveDependency(p):
	result = {
		"Latin": Namespace(
			family = "Noto",
			width = notoWidthMap[p.width],
			weight = p.weight
		)
	}
	if p.family in [ "WarcraftSans", "WarcraftUI" ]:
		result["Numeral"] = Namespace(
			family = "Noto",
			width = 3,
			weight = p.weight
		)
	if p.family in [ "Sans", "UI", "WarcraftSans", "WarcraftUI" ]:
		result["CJK"] = Namespace(
			family = "Source",
			weight = p.weight,
			width = 5,
			region = regionSourceMap[p.region]
		)
	return result

def GetMorpheus(weight, feature):
	return Namespace(
		weight = morpheusWeightMap[weight],
		width = 3,
		family = "Latin",
		feature = feature,
	)

def GetSkurri(weight, feature):
	return Namespace(
		weight = weight,
		width = 7,
		family = "Latin",
		feature = feature,
	)

def GetLatinFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 7,
		family = "UI",
		region = regionalVariant[region]["Latn"],
		feature = feature,
		encoding = "unspec"
	)

def GetLatinChatFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 3,
		family = "UI",
		region = regionalVariant[region]["Latn"],
		feature = feature,
		encoding = "unspec"
	)

def GetHansFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 5,
		family = "WarcraftSans",
		region = regionalVariant[region]["Hans"],
		feature = feature,
		encoding = "gbk"
	)

def GetHansCombatFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 7,
		family = "Sans",
		region = regionalVariant[region]["Hans"],
		feature = feature,
		encoding = "gbk"
	)

def GetHansChatFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 3,
		family = "Sans",
		region = regionalVariant[region]["Hans"],
		feature = feature,
		encoding = "gbk"
	)

def GetHantFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 5,
		family = "WarcraftSans",
		region = regionalVariant[region]["Hant"],
		feature = feature,
		encoding = "big5"
	)

def GetHantCombatFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 7,
		family = "Sans",
		region = regionalVariant[region]["Hant"],
		feature = feature,
		encoding = "big5"
	)

def GetHantNoteFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 5,
		family = "Sans",
		region = regionalVariant[region]["Hant"],
		feature = feature,
		encoding = "big5"
	)

def GetHantChatFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 3,
		family = "Sans",
		region = regionalVariant[region]["Hant"],
		feature = feature,
		encoding = "big5"
	)


def GetKoreanFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 5,
		family = "UI",
		region = regionalVariant[region]["ko"],
		feature = feature,
		encoding = "korean"
	)

def GetKoreanCombatFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 7,
		family = "UI",
		region = regionalVariant[region]["ko"],
		feature = feature,
		encoding = "korean"
	)

def GetKoreanDisplayFont(weight, region, feature):
	return Namespace(
		weight = weight,
		width = 3,
		family = "UI",
		region = regionalVariant[region]["ko"],
		feature = feature,
		encoding = "korean"
	)

def ParamToArgument(conf):
	js = json.dumps(conf.__dict__, separators=(',',':'))
	return "'{}'".format(js)

if __name__ == "__main__":
	makefile = {
		"variable": {
			"VERSION": config.version,
			"IDH_JOBS?": 8,
		},
		"rule": {
			".PHONY": {
				"depend": [
					"all",
					"hint2",
				] + [
					"hint2-{}".format(w) for w in config.fontPackWeight
				],
			},
			"all": {
				"depend": [],
			},
			"clean": {
				"command": [
					"-rm -rf build/",
					"-rm -rf out/??*-???/",
				],
			},
		},
	}

	hintInstance = []
	unique = lambda l: reduce(lambda l, x: l + [ x ] if x not in l else l, l, [])
	powerset = lambda lst: reduce(lambda result, x: result + [subset + [x] for subset in result], lst, [[]])

	for w, (e, f, r, wd) in product(config.fontPackWeight, config.instance):
		param = Namespace(
			family = f,
			weight = w,
			width = wd,
			region = r,
			feature = [],
			encoding = e,
		)
		font = "out/{}.ttf".format(GenerateFilename(param)[len(e)+1:])

		makefile["rule"]["all"]["depend"].append(font)
		makefile["rule"][font] = {
			"depend": [ "build/nowar/{}.ttf".format(GenerateFilename(param)) ],
			"command": [
				"mkdir -p out/",
				"cp $^ $@",
			],
		}
		hintInstance.append(param)

	hintGroup = {
		"Latin": []
	}
	hintGroup.update({
		w: [] for w in config.fontPackWeight
	})
	for f in hintInstance:
		if f.family == "Latin":
			hintGroup["Latin"].append(f)
		else:
			f.encoding = "unspec"
			hintGroup[f.weight].append(f)
	for k, v in hintGroup.items():
		hintGroup[k] = unique(v)

	# IDH
	makefile["rule"]["hint2"] = {
		"depend": [ "hint2-{}".format(w) for w in config.fontPackWeight ],
	}
	for w in config.fontPackWeight:
		for f in hintGroup[w]:
			makefile["rule"]["hint2-{}".format(w)] = {
				"depend": [ "build/hint2/{}.otd".format(GenerateFilename(f)) for f in hintGroup[w] ],
				"command": [
					"node node_modules/@chlorophytum/cli/bin/_startup hint -c source/idh/{0}.json -h cache/idh-{0}.gz -j ${{IDH_JOBS}} ".format(w) +
					" ".join([ "build/hint2/{0}.otd build/hint2/{0}.hint.gz".format(GenerateFilename(f)) for f in hintGroup[w] ])
				],
			}
			makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(f))] = {
				"depend": [ "build/nowar/{}.otd".format(GenerateFilename(f)) ],
				"command": [ "otfccbuild -q -O3 --stub-cmap4 --keep-average-char-width $< -o $@" ],
			}
			makefile["rule"]["build/nowar/{}.otd".format(GenerateFilename(f))] = {
				"depend": [ "build/hint2/{}.instr.gz".format(GenerateFilename(f)) ],
				"command": [
					"mkdir -p build/nowar/",
					"node node_modules/@chlorophytum/cli/bin/_startup integrate -c source/idh/{0}.json build/hint2/{1}.instr.gz build/hint2/{1}.otd build/nowar/{1}.otd".format(w, GenerateFilename(f)),
				],
			}
			makefile["rule"]["build/hint2/{}.instr.gz".format(GenerateFilename(f))] = {
				"depend": [ "build/hint2/{}.hint.gz".format(GenerateFilename(f)) ],
				"command": [
					"node node_modules/@chlorophytum/cli/bin/_startup instruct -c source/idh/{0}.json build/hint2/{1}.otd build/hint2/{1}.hint.gz build/hint2/{1}.instr.gz".format(w, GenerateFilename(f)),
				],
			}
			makefile["rule"]["build/hint2/{}.hint.gz".format(GenerateFilename(f))] = {
				"depend": [ "hint2" ],
			}
			makefile["rule"]["build/hint2/{}.otd".format(GenerateFilename(f))] = {
				"depend": [ "build/hint1/{}.ttf".format(GenerateFilename(f)) ],
				"command": [
					"mkdir -p build/hint2/",
					"otfccdump $< -o $@",
				],
			}

	# TTFautohint
	for f in hintGroup["Latin"]:
		makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(f))] = {
			"depend": [ "build/unhinted/{}.ttf".format(GenerateFilename(f)) ],
			"command": [
				"mkdir -p build/nowar/",
				"ttfautohint -a qqq -c -D latn -f latn -G 0 -l 7 -r 48 -n -x 0 -v $< $@",
			],
		}
	for w in config.fontPackWeight:
		for f in hintGroup[w]:
			makefile["rule"]["build/hint1/{}.ttf".format(GenerateFilename(f))] = {
				"depend": [ "build/unhinted/{}.ttf".format(GenerateFilename(f)) ],
				"command": [
					"mkdir -p build/hint1/",
					"ttfautohint -a qqq -c -D latn -f latn -G 0 -l 7 -r 48 -n -x 0 -v $< $@",
				],
			}

	# Sans, UI
	for f, w, wd, r, fea in product([ "Sans", "UI" ], config.fontPackWeight, [3, 5, 7], regionNameMap.keys(), powerset(config.fontPackFeature)):
		param = Namespace(
			family = f,
			weight = w,
			width = wd,
			region = r,
			feature = fea,
			encoding = "unspec",
		)
		makefile["rule"]["build/unhinted/{}.ttf".format(GenerateFilename(param))] = {
			"depend": ["build/unhinted/{}.otd".format(GenerateFilename(param))],
			"command": [ "otfccbuild -q -O3 --stub-cmap4 --keep-average-char-width $< -o $@" ]
		}
		dep = ResolveDependency(param)
		makefile["rule"]["build/unhinted/{}.otd".format(GenerateFilename(param))] = {
			"depend": [
				"build/noto/{}.otd".format(GenerateFilename(dep["Latin"])),
				"build/shs/{}.otd".format(GenerateFilename(dep["CJK"])),
			],
			"command": [ 
				"mkdir -p build/unhinted/",
				"python merge.py {}".format(ParamToArgument(param)),
			]
		}
		makefile["rule"]["build/noto/{}.otd".format(GenerateFilename(dep["Latin"]))] = {
			"depend": [ "source/noto/{}.ttf".format(GenerateFilename(dep["Latin"])) ],
			"command": [
				"mkdir -p build/noto/",
				"otfccdump --glyph-name-prefix latn --ignore-hints $< -o $@",
			]
		}
		makefile["rule"]["build/shs/{}.otd".format(GenerateFilename(dep["CJK"]))] = {
			"depend": [ "source/shs/{}.ttf".format(GenerateFilename(dep["CJK"])) ],
			"command": [
				"mkdir -p build/shs/",
				"otfccdump --glyph-name-prefix hani --ignore-hints $< -o $@"
			],
		}

		# set encoding
		for e in [ "gbk", "big5", "jis", "korean" ]:
			enc = Namespace(
				family = f,
				weight = w,
				width = wd,
				region = r,
				feature = fea,
				encoding = e,
			)
			makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(enc))] = {
				"depend": ["build/nowar/{}.otd".format(GenerateFilename(enc))],
				"command": [ "otfccbuild -q -O3 --stub-cmap4 --keep-average-char-width $< -o $@" ]
			}
			makefile["rule"]["build/nowar/{}.otd".format(GenerateFilename(enc))] = {
				"depend": ["build/nowar/{}.otd".format(GenerateFilename(param))],
				"command": [ "python set-encoding.py {}".format(ParamToArgument(enc)) ]
			}

	# dump `makefile` dict to actual “GNU Makefile”
	makedump = ""

	for var, val in makefile["variable"].items():
		makedump += "{}={}\n".format(var, val)

	for tar, recipe in makefile["rule"].items():
		dep = recipe["depend"] if "depend" in recipe else []
		makedump += "{}: {}\n".format(tar, " ".join(dep))
		com = recipe["command"] if "command" in recipe else []
		for c in com:
			makedump += "\t{}\n".format(c)

	with codecs.open("Makefile", 'w', 'UTF-8') as mf:
		mf.write(makedump)
