import sys
from pykml import parser
import pandas as pd
from gpx_converter import Converter
import logging

# Handling Program Arguments
n = len(sys.argv)
print("Total arguments passed:", n)
# Arguments passed
print("\nName of Python script:", sys.argv[0])
file_path = sys.argv[1]

# Check whether the path has been provided or not
if len(file_path) == 0:
    logging.error("kml_to_gpx.py: Program arguments missing")
    raise ValueError("kml_to_gpx.py: Program arguments missing")
logging.info("Reading File: {}".format(file_path))
# Reading kml file
with open(file_path) as f:
    doc = parser.parse(f)
# Extracting the Coordinates - Latitudes & Longitudes
root = doc.getroot()
document = root.Document
pm = document.Placemark
line_str = pm.LineString
corr = line_str.coordinates
corr_text = corr.text
corr_text = corr_text.replace(' ', '')
res_list = corr_text.splitlines()
# Data
lats = []
lngs = []
data_dict = {}
for res in res_list:
    new_res = res.split(',')
    if len(new_res) < 2:
        continue
    lngs.append(new_res[0])
    lats.append(new_res[1])
data_dict['lats'] = lats
data_dict['lngs'] = lngs

file_name = 'output_' + file_path.replace(' ', '_').split('.kml')[0] + '.gpx'
logging.info("Output Filename: {}".format(file_name))

# Conversion of dictionary to df and calling the respective function of Converter class
data_df = pd.DataFrame(dict(data_dict))
try:
    Converter.dataframe_to_gpx(input_df=data_df,
                               lats_colname='lats',
                               longs_colname='lngs',
                               output_file=file_name)
except Exception as e:
    print(e)
