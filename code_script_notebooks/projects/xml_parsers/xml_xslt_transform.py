import streamlit as st
import xml.dom.minidom
import lxml.etree as ET
from lxml import etree
from pathlib import Path
import logging
from bs4 import BeautifulSoup
import xml.etree.ElementTree as XET

logging.basicConfig(format="%(message)s|%(levelname)s",
                    level=logging.INFO)

st.set_page_config(layout="wide",
                   page_title="xml fiddler")

st.header('Python XML/XSLT Transformer')

file_path = Path(__file__).parent.resolve()


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

parse = st.button("Parse XML")

if parse:
    if xml_file and xslt_file:
        newdom = transform_xml(xml_file.name,
                               xslt_file.name)
        st.code(newdom)
    else:
        newdom = transform_xml(xml_data_worker,
                               city_workers_xslt)
        st.code(newdom)
