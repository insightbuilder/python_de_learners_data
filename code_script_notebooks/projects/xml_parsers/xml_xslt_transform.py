import streamlit as st
import xml.dom.minidom
import lxml.etree as ET

st.
# Define the function to pretty print XML
def pretty_print_xml(xml_str):
    """Pretty prints XML."""
    dom = xml.dom.minidom.parseString(xml)
    return dom.toprettyxml()


def transform_xml(xml_file, xslt_file):
    """xml transformed based on xslt"""
    dom = ET.parse(xml_file)
    xslt = ET.parse(xslt_file)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    return ET.tostring(newdom)

# Pretty print the XML data
pretty_xml = pretty_print_xml(xml_data)

# Display the pretty printed XML data in Streamlit
st.write(pretty_xml)
