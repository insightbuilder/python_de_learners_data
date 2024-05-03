import streamlit as st
import xml.dom.minidom
import lxml.etree as ET
from lxml import etree
from pathlib import Path
import logging
from bs4 import BeautifulSoup
import xml.etree.ElementTree as XET
from io import StringIO
import json
from dict2xml import dict2xml
import pandas as pd

logging.basicConfig(format="%(message)s|%(levelname)s",
                    level=logging.INFO)

st.set_page_config(layout="wide",
                   page_title="xml fiddler")

st.header('Python XML/XSLT Transformer')

file_path = Path(__file__).parent.resolve()


def extract_field_names(obj):
    """Extracts all field names from a nested JSON object.
    Args:
        obj: A JSON object.
    Returns:
        A list of all field names in the JSON object.
    """

    field_names = []

    def _extract_field_names(obj, field_names):
        if isinstance(obj, dict):
            for key, value in obj.items():
                field_names.append(key)
                _extract_field_names(value, field_names)
        elif isinstance(obj, list):
            for item in obj:
                _extract_field_names(item, field_names)

    _extract_field_names(obj, field_names)
    return field_names


# Define the function to pretty print XML
def pretty_print_xml(xml_str):
    """Pretty prints XML."""
    dom = xml.dom.minidom.parseString(xml_str)
    return dom.toprettyxml()


def pretty_bs4(xml_file):
    """Using BS4 to prettify the xml"""
    temp = BeautifulSoup(open(xml_file), "xml")
    new_xml = temp.prettify()
    return new_xml


def pretty_etree(xml_file):
    """Using lxml etree to parse and pretty print"""
    temp = etree.parse(xml_file)
    new_xml = etree.tostring(temp, pretty_print=True,)
    return new_xml


def pretty_xet(xml_str):
    element = XET.XML(xml_str)
    XET.indent(element)
    return XET.tostring(element, encoding='unicode')


def remove_col_space(cols_list):
    new_cols = []
    for cols in cols_list:
        new_cols.append(cols.replace(" ", ""))
    print(new_cols)
    return new_cols


def transform_xml(xml_file, xslt_file):
    """xml transformed based on xslt"""
    dom = ET.parse(xml_file)
    xslt = ET.parse(xslt_file)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    return pretty_print_xml(ET.tostring(newdom))


left, right = st.columns(2)

xml_data_worker = file_path / 'xml_data_worker.xml'
city_workers_xslt = file_path / 'city_workers.xslt'

logging.info(city_workers_xslt)

xml_file = left.file_uploader(label='Your XML',)
xslt_file = right.file_uploader(label='Your XSLT')

# Pretty print the XML data
if xml_file is not None:
    xml_strings = xml_file.getvalue().decode('utf-8')
    pretty_xml = pretty_xet(xml_strings)
    left.code(pretty_xml)
    # left.write(xml_strings)
else:
    with open(xml_data_worker, 'r') as city:
        xml_c = city.read()
        pretty_xml = pretty_xet(xml_c)
        left.code("Sample xml")
        left.code(pretty_xml,)

if xslt_file is not None:
    xsl_strings = xslt_file.getvalue().decode('utf-8')
    pretty_xsl = pretty_xet(xsl_strings)
    right.code(pretty_xsl)
    # right.write(xsl_strings)

else:
    with open(city_workers_xslt, 'r') as citx:
        xsl_c = citx.read()
        pretty_xsl = pretty_xet(xsl_c)
        right.code("Sample xslt")
        right.code(pretty_xsl)

xml_text = left.text_area(label="Paste XML Here")
xsl_text = right.text_area(label="Paste XSL Here", height=100)

parse = st.button("Parse XML")

if parse:
    if xml_file and xslt_file:
        st.write("Using the file data.")
        xml_file = file_path / xml_file.name
        xslt_file = file_path / xslt_file.name
        newdom = transform_xml(xml_file,
                               xslt_file)
        st.code(newdom)
    elif xml_text and xsl_text:
        # st.code(xml_text)
        st.write("Using the text data.")
        try:
            parsed_xml = ET.parse(StringIO(xml_text))
            parsed_xsl = ET.parse(StringIO(xsl_text))
            transform = ET.XSLT(parsed_xsl)
            newdom = transform(parsed_xml)
            st.code(newdom)
        except Exception as e:
            st.write(f'There is issue with the text data..., {e}')

    else:
        st.write("Using the inbuilt files")
        newdom = transform_xml(xml_data_worker,
                               city_workers_xslt)
        st.code(newdom)

json_file = left.file_uploader(label="Json_file")

jsontoxml = left.button("Json => Xml")
jsonfields = left.button("Json => DF")

if jsontoxml and json_file:
    json_data = json_file.getvalue().decode('utf-8')
    dict_data = json.loads(json_data)
    left.write("Json Data:")
    left.write(dict_data)
    xml_data = dict2xml(dict_data)
    left.write("XML Parsed:")
    left.code(xml_data)

if jsonfields and json_file:
    json_data = json_file.getvalue().decode('utf-8')
    dict_data = json.loads(json_data)
    # field_names = extract_field_names(dict_data)
    df = pd.json_normalize(dict_data)
    left.dataframe(df)
    cols_data = df.columns
    left.write(cols_data)

csv_file = right.file_uploader(label="csv_file")

csvtoxml = right.button("Parse_csv")

if csvtoxml and csv_file:
    dataf = pd.read_csv(csv_file)
    right.write("CSV Data:")
    new_cols = remove_col_space(dataf.columns)
    dataf.columns = new_cols
    right.dataframe(dataf)
    xml_csv_data = dataf.to_xml()
    right.write("XML Parsed:")
    right.code(xml_csv_data)
