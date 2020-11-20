import xml.etree.cElementTree as xmlTree
from xml.etree import ElementTree
from event import Message, WServiceCheckerException
from pathlib import Path
from wservice import WService


CSV_SUFFIX = '.csv'
XML_SUFFIX = '.xml'


def _get_service_data(rows):
    for row in rows:
        if isinstance(row, str):
            columns = row.split(',')
            description = columns[1:-3]
            description = ','.join(description)
            yield columns[0], description, columns[-2]
        elif isinstance(row, ElementTree.Element):
            yield row.attrib.get('name'), row.text, row.attrib.get('startup')
        else:
            yield '', '', ''


def from_file(filename, suffix):
    with open(filename, 'r') as f:
        rows = []
        if suffix == CSV_SUFFIX:
            rows = f.readlines()
        elif suffix == XML_SUFFIX:
            xmlDoc = ElementTree.parse(f)
            root = xmlDoc.find('WServiceList')
            rows = root.findall('WService')

        return [WService(name, description, startup)
                for name, description, startup
                in _get_service_data(rows)]


def verify_path(filename, suffixes):
    path = Path(filename)
    if not path.is_file() or not path.exists() or path.suffix not in suffixes:
        raise WServiceCheckerException(f'''File not exists or type not supported.
                                       Extensions allowed: {suffixes}''')
    return path


# command
def export_xml(args):
    path = verify_path(args[0], [CSV_SUFFIX])
    service_list = from_file(args[0], CSV_SUFFIX)
    service_list.pop(0)  # remove headers row

    root = xmlTree.Element('WServiceList')
    for service in service_list:
        xmlTree.SubElement(root,
                           'WService',
                           name=service.name,
                           startup=service.startup).text = service.description

    xmlDoc = xmlTree.ElementTree(root)
    xmlDoc.write(f'./{path.stem}{XML_SUFFIX}')
    Message.create(f'''Format completed!
                   You can check file: {path.stem}{XML_SUFFIX}''',
                   Message.INFORMATION)
