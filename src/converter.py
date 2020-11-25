from xml.etree import ElementTree
from event import Message, WServiceCheckerException
from pathlib import Path
from wservice import WService


CSV_SUFFIX = '.csv'
XML_SUFFIX = '.xml'


def _get_service_data(rows):
    """Get an iterable data collection of WService (only primitive values).

    Args:
        rows (list(obj)): Object list where extract data for WService.

    Yields:
        tuple(str, str, str): Data for WService(name, description, startup).
    """
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
    """Get WService object list from a source.

    Args:
        filename (str): Path to file where extract service list.
        suffix (str): File suffix for manipulate data.

    Returns:
        list(WService): Service list extracted.
    """
    with open(filename, 'r') as f:
        rows = []
        if suffix == CSV_SUFFIX:
            rows = f.readlines()
            rows.pop(0)  # remove headers row
        elif suffix == XML_SUFFIX:
            xmlDoc = ElementTree.parse(f)
            root = xmlDoc.getroot()
            rows = root.findall('WService')

        return [WService(name, description, startup)
                for name, description, startup
                in _get_service_data(rows)]


def verify_path(filename, suffixes):
    """Verify is a file exists and suffix is valid.

    Args:
        filename (str): Path to file to verify.
        suffixes (list(str)): Suffixes valid for file

    Raises:
        WServiceCheckerException: If file not exists or suffix not valid

    Returns:
        Path: Object Path generated when verify file
    """
    path = Path(filename)
    if not path.is_file() or not path.exists() or path.suffix not in suffixes:
        raise WServiceCheckerException(f'''File not exists or type not supported.
                                       Extensions allowed: {suffixes}''')
    return path


# command
def export_xml(args):
    """Exports a CSV file of Windows service list to a XML easily readable file.

    Args:
        args (list(str)): Args command to process.
    """
    path = verify_path(args[0], [CSV_SUFFIX])
    service_list = from_file(args[0], CSV_SUFFIX)

    root = ElementTree.Element('WServiceList')
    for service in service_list:
        ElementTree.SubElement(root, 'WService', name=service.name,
                               startup=service.startup).text = service.description

    xmlDoc = ElementTree.ElementTree(root)
    xmlDoc.write(f'./{path.stem}{XML_SUFFIX}')
    Message.create(f'''Format completed!
                   You can check file: {path.stem}{XML_SUFFIX}''',
                   Message.INFORMATION)
