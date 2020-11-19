import xml.etree.cElementTree as xmlTree
from xml.etree import ElementTree
from event import Message, WServiceCheckerException
from pathlib import Path
from wservice import WService


def get_service_data(rows):
    for row in rows:
        columns = row.split(',')
        description = columns[1:-3]
        description = ','.join(description)
        yield columns[0], description, columns[-2]


def from_csv(filename):
    with open(filename, 'r') as f:
        return [WService(name, description, startup)
                for name, description, startup
                in get_service_data(f.readlines())]


def export_xml(args):
    path = Path(args[0])
    if not path.is_file() or not path.exists() or not path.suffix == '.csv':
        raise WServiceCheckerException('File not exists or not supported')

    service_list = from_csv(args[0])
    service_list.pop(0)  # remove headers row
    root = xmlTree.Element('WServiceList')
    for service in service_list:
        xmlTree.SubElement(root,
                           'WService',
                           name=service.name,
                           startup=service.startup).text = service.description
    xmlDoc = xmlTree.ElementTree(root)
    xmlDoc.write(f'./{path.stem}.xml')
    Message.create(f'Format completed! You can check file: {path.stem}.xml',
                   Message.INFORMATION)


def read_xml(filename):
    with open(filename, 'r') as f:
        xmlDoc = ElementTree.parse(f)
        root = xmlDoc.find('WServiceList')
        return [WService(node.attrib.get('name'),
                         node.text,
                         node.attrib.get('startup'))
                for node in root.findall('WService')]
