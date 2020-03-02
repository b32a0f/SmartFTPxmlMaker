# -*- coding: utf-8 -*-

# indent          http://effbot.org/zone/element-lib.htm#prettyprint
# UUID(GUID) Info https://blog.naver.com/drvoss/220760761375
# Queue Item Info https://www.smartftp.com/en-us/support/kb/2683

from datetime import datetime
import os
import shutil
import uuid
from xml.etree.ElementTree import Element, SubElement, ElementTree, dump

def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def addElem(root, filepath, gdpath, folder=''):
    # Extract file name.
    file   = os.path.split(filepath)[-1]
    folder = folder + '/'

    # Create brunch tags.
    item   = Element('Item')
    source = Element('Source')
    dest   = Element('Destination')

    # Add subtags.
    SubElement(item, 'Version').text         = '5'
    SubElement(item, 'Id').text              = '{' + str(uuid.uuid4()).upper() + '}'
    SubElement(item, 'Type').text            = '1'
    SubElement(item, 'Size').text            = str(os.path.getsize(filepath))
    SubElement(item, 'Operation').text       = '1'
    SubElement(item, 'OperationScope').text  = '1'
    SubElement(item, 'Synchronization').text = '1'
    SubElement(item, 'FileExistAction').text = '1'
    SubElement(item, 'TransferType').text    = '2'
    item.append(source)
    SubElement(source, 'Type').text          = '1'
    SubElement(source, 'Path').text          = filepath
    item.append(dest)
    SubElement(dest, 'Type').text            = '2'
    SubElement(dest, 'FavoriteId').text      = favoriteID
    SubElement(dest, 'Path').text            = gdpath + folder + file

    # Add item to root.
    root.append(item)

if __name__ == '__main__':
    # xmlpath    : Path to save xml.
    # basepath   : Uploading folder.
    # movepath   : If exists file, to move. User must considers hands on these.
    # mygdfs     : Drive File Stream path. Regarding to Backup to teamdrive.
    # mydrive    : Path of destination for mydrive. NOT Recommeneded upload to root.
    # teamdrive  : Path of destination for teamdrive. NOT Recommeneded upload to root.
    # favoriteID : UUID of Google Drive Connection. It will be find out from Exported Queue xml.
    xmlpath    = r'C:\Users\user\Documents\SmartFTP_Queue_{}.xml'.format(datetime.now() \
                                                                                 .isoformat()[:19] \
                                                                                 .replace(':', '：'))
    basepath   = r'H:\source'
    movepath   = r'H:\duplicated'
    mygdfs     = r'G:\mydrive\...'
    mydrive    = '/mydrive/.../'
    teamdrive  = '/teamdrives/.../'
    favoriteID = '{1A23B45C-9A91-2D3D-4577-A824F416DC84}'

    # Create root.
    root = Element('Items')

    # Add tags.
    for file in os.listdir(basepath):
        folder   = '' #file[file.find('[') + 1:file.find(']')]
        filepath = os.path.join(basepath, file)
        mydest   = os.path.join(mygdfs, folder, file)

        # Skip folder.
        if os.path.isfile(filepath):
            if not os.path.exists(mydest):
                addElem(root, filepath, mydrive, folder)
                addElem(root, filepath, teamdrive, folder)
            else:
                existfile = os.path.join(movepath, file)
                shutil.move(filepath, existfile)

    indent(root)
    print('File : {}\nItem : {}'.format(len(root.findall('Item')) // 2, len(root.findall('Item'))))

    # Save.
    ElementTree(root).write(xmlpath, encoding='utf-8')
