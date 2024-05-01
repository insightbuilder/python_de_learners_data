import streamlit as st
import xml.dom.minidom
import lxml.etree as ET
from pathlib import Path
from io import StringIO
import logging
from rich import print

logging.basicConfig(format="%(message)s|%(levelname)",
                    level=logging.INFO)

st.set_page_config(layout="wide",
                   page_title="xml fiddler")


file_path = Path(__file__).parent.resolve()


# Define the function to pretty print XML
def pretty_print_xml(xml_str):
    """Pretty prints XML."""
    dom = xml.dom.minidom.parseString(xml_str)
    return dom.toprettyxml()


def transform_xml(xml_file, xslt_file):
    """xml transformed based on xslt"""
    dom = ET.parse(xml_file)
    xslt = ET.parse(xslt_file)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    return pretty_print_xml(ET.tostring(newdom))

left, right = st.columns(2)

xml_file = left.file_uploader(label='xml_file',)
xslt_file = right.file_uploader(label='xslt_file')

# Pretty print the XML data
if xml_file is not None:
    xml_strings = xml_file.getvalue().decode('utf-8')
    pretty_xml = pretty_print_xml(xml_strings)
    left.write(pretty_xml)
    # left.write(xml_strings)
else:
    with open('city_workers.xml', 'r') as city:
        xml_c = city.read()
        pretty_xml = pretty_print_xml(xml_c)
        left.write(pretty_xml)

if xslt_file is not None:
    xsl_strings = xslt_file.getvalue().decode('utf-8')
    pretty_xsl = pretty_print_xml(xsl_strings)
    right.write(pretty_xsl)
    # right.write(xsl_strings)

else:
    with open('city_workers.xslt', 'r') as citx:
        xsl_c = citx.read()
        pretty_xsl = pretty_print_xml(xsl_c)
        right.write(pretty_xsl)

parse = st.button("Parse XML")

if parse:
    if xml_file and xslt_file:
        newdom = transform_xml(xml_file.name,
                               xslt_file.name)
        st.write(newdom)
    else:
        newdom = transform_xml('city_workers.xml',
                               'city_workers.xslt')
        st.write(newdom)
