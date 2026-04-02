import xml.dom.minidom

xml = xml.dom.minidom.parse('results.xml')
pretty_xml_as_string = xml.toprettyxml()
with open('results_pretty.xml', 'w') as f:
    f.write(pretty_xml_as_string)