import json, io

useful_fields = ["WMS_ACAD_YEAR", "OFFERED", "STRM", "CRSE_ID", "SUBJECT",
"CLASS_SECTION", "CATALOG_NBR", "CLASS_NBR", "CONSENT", "GRADING_BASIS", "SSR_COMPONENT",
"DESCR", "COURSE_TITLE_LONG", "WMS_FACIL_DESCR1","WMS_STND_MTG_PAT1", 
"WMS_START_TIME1", "WMS_END_TIME1", "WMS_DISTRIB_NT3", "WMS_DISTRIB_NT1",
"WMS_DISTRIB_NT2", "WMS_RQMT_EVAL", "WMS_ENRL_LIMIT", "WMS_PREREQS", "WMS_ATTR_SRCH",
"WMS_CLASS_FORMAT"]

# Open files
with open("data1920_formatted.json") as json_file:
    data_1920 = json.load(json_file)


with open("data1819_formatted.json") as json_file:
    data_1819= json.load(json_file)


with io.open("data_official.json", 'r', encoding='utf-8-sig') as json_file:
	data_official = json.load(json_file)


# Parse unofficial data to key by unique class
unofficial_dict = {}
for d in data_1920:
	our_id = d["STRM"] + d["SUBJECT"] + d["CATALOG_NBR"] + d["CLASS_SECTION"]
	unofficial_dict[our_id] = d

for d in data_1819:
	our_id = d["STRM"] + d["SUBJECT"] + d["CATALOG_NBR"] + d["CLASS_SECTION"]
	unofficial_dict[our_id] = d


# Array of all classes in both sets
unofficial_joined_data = []

id_counter = 1


# Join the data
for subject in data_official:
	for ocourse in data_official[subject]:
		our_id = ocourse["Term"] + ocourse["Subject"] + ocourse["Catalog"] + ocourse["Section"]
		our_id = our_id.replace(" ", "")
		if our_id in unofficial_dict:
			ucourse = unofficial_dict[our_id]
			for ufield in useful_fields:
				ocourse[ufield] = ucourse[ufield]
			for ofield in ocourse:
				ucourse[ofield] = ocourse[ofield]

			ocourse["optimizer_id"] = id_counter
			id_counter += 1
			unofficial_joined_data.append(ocourse)


# Write to files

with open("data_joined_unofficial.json", "w") as f:
	json.dump(unofficial_joined_data, f, indent=4)

with open("data_joined_official.json", "w") as f:
	json.dump(data_official, f, indent=4)