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
    i = '\n' + level * '  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
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
    file = os.path.split(filepath)[-1]

    # Create brunch tags.
    item = Element('Item')
    src  = Element('Source')
    dest = Element('Destination')

    # Add subtags.
    SubElement(item, 'Version').text         = '5'
    SubElement(item, 'Id').text              = '{' + str(uuid.uuid4()).upper() + '}'
    SubElement(item, 'Type').text            = '1' # 1: File 2: Folder Format not consider.
    SubElement(item, 'Size').text            = str(os.path.getsize(filepath)) # If file must have. Value not consider.
    SubElement(item, 'Operation').text       = '1' # No matter.
    SubElement(item, 'OperationScope').text  = '1' # No matter.
    SubElement(item, 'Synchronization').text = '1' # 1: Rule 2: OFF
    SubElement(item, 'FileExistAction').text = '1' # 1: Replace 2: Rule
    SubElement(item, 'TransferType').text    = '2' # No matter.
    SubElement(src, 'Type').text             = '1' # 1: Local 2: Cloud
    SubElement(src, 'Path').text             = filepath
    SubElement(dest, 'Type').text            = '2'
    SubElement(dest, 'FavoriteId').text      = favoriteID
    SubElement(dest, 'Path').text            = gdpath + folder + file # No ExFld Freez. If file, Last / 'l be name either end with /.

    # Modify tags for folder.
    if os.path.isdir(filepath):
        item.remove(item.find('Size'))
        item.find('Type').text           = '2'
        item.find('OperationScope').text = '2'

    # Concatenate.
    item.append(src)
    item.append(dest)
    root.append(item)

if __name__ == '__main__':
    # ----------------------------------------------------------------
    # xmlpath    : Path to save xml.
    # basepath   : Uploading folder.
    # movepath   : Path to move for exist files.
    # mygdfs     : Google Drive File Stream path. (Check exist files.)
    # mydrive    : Destination path of mydrive.
    # teamdrive  : Destination path of teamdrive. (Back Up.)
    # favoriteID : UUID of SmartFTP connection.
    # 
    # <Way to find FavoriteID>
    # 1) File > Settings > History > {}.Properties > General
    # 2) File > Connection > Quick Connect > {}.Properties > General
    # ----------------------------------------------------------------
    xmlpath    = r'C:\Users\user\Documents\SmartFTP_Queue_{}.xml'.format(datetime.now().isoformat()[:19].replace(':', '：'))
    basepath   = r'H:\source'
    movepath   = r'H:\duplicated'
    mygdfs     = r'G:\mydrive\...'
    mydrive    = '/mydrive/.../'
    teamdrive  = '/teamdrives/.../'
    favoriteID = '{1A23B45C-9A91-2D3D-4577-A824F416DC84}'

    # Create root.
    root = Element('Items')

    # Processing.
    for file in os.listdir(basepath):
        word   = file[file.find('[') + 1:file.find(']')].split(' ')[0]
        bucket = ''
        folder = ''

        # Combine gdfs folders.
        for circle in os.listdir(mygdfs):
            bucket += circle + '|'

        # Search target folder.
        if word in bucket:
            start  = bucket.find(word)
            end    = bucket.find('|', start)
            folder = bucket[start:end]

        # Modify paths.
        filepath = os.path.join(basepath, file)
        gdfsdest = os.path.join(mygdfs, folder, file)
        folder   = (lambda x: x + '/' if len(x) else x)(folder)

        # Add tags.
        if not os.path.exists(gdfsdest):
            addElem(root, filepath, mydrive, folder)
            addElem(root, filepath, teamdrive, folder)
        else:
            existfile = os.path.join(movepath, file)
            shutil.move(filepath, existfile)

    # Align xml.
    indent(root)

    # Report.
    itemcnt = len(root.findall('Item'))
    filecnt = len(os.listdir(basepath))
    movecnt = len(os.listdir(movepath))
    print('Item :', itemcnt)
    print('File :', filecnt)
    print('Move :', movecnt)

    # Save.
    ElementTree(root).write(xmlpath, encoding='utf-8')
