# Assesment 3 - Write a script to copy the content (nested files/folders)
# of the source folder to the destination folder.

# TL;DR We copy the existing files and folders to the destination
# folder and while we do it, we create a mapping of the old ids
# including the new parent ids. Finally, we organize all items
#
# 1.- We iterate through every existing folder and we create a new one in the
# destination folder. At the same time, we create a dict with a mapping of the
# old and the new ids including the previous parent/s ids
#
# 2.- We iterate through every existing file and we create a copy one in the
# destination folder. At the same time, we create a dict with a mapping of the
# old and the new ids including the previous parent/s ids
#
# 3.- With the mappings created, we call the Drive API update method to removed
# the old parents and add the new ones in the destination folder

from google_prv.google_service import drive_service
from google_functions.get_folder_structure import genFolderStructure

import logging

folderChildMapping = []
fileChildMapping = []
countsDict = {}

# My personal destination folder
DESTINATION_FOLDER = '1npzHyVo3xq8FjprCLDHgCNb6dxI9BOO0'
# Folder mimeType
FOLDER_MIMETYPE = 'application/vnd.google-apps.folder'
# Folder to search
FOLDER_TO_SEARCH = "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"  # folder ID to search

# Dict with the mapping of destination folder information
destination_folder_dict = {'id': '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V',
                           'copy_id': '1npzHyVo3xq8FjprCLDHgCNb6dxI9BOO0',
                           'parent_id': 'Root folder',
                           'name': 'Destination folder'}


def createFolderMapping(counts, folder, depth, folderChildMapping):
    """Generate the folder folder mapping and create new folders """
    service = drive_service()
    folderID = folder['folderID']
    counts[folderID] = {'folderName': folder['folderName'],
                        'subFolders': 0, 'subFiles': 0, 'depth': depth}
    for child in folder.get('childrenFiles', []):
        counts[folderID]['subFiles'] += 1
    for child in folder.get('childrenFolders', []):
        copy_id = service.files()\
            .create(body={'name': child.get('folderName'), 'parents': [
                DESTINATION_FOLDER],
                'mimeType': FOLDER_MIMETYPE}).execute()['id']
        mappingdict = {'id': child.get('folderID'),
                       'copy_id': copy_id,
                       'parent_id': folder.get('folderID'),
                       'name': child.get('folderName')}
        folderChildMapping.append(mappingdict.copy())
        counts[folderID]['subFolders'] += 1
        createFolderMapping(counts, child, depth+1, folderChildMapping)
    return folderChildMapping


def createFileMapping(counts, folder, depth, fileChildMapping):
    """Generate the file folder mapping and copy new files to dest folder"""
    service = drive_service()
    folderID = folder['folderID']
    counts[folderID] = {'folderName': folder['folderName'],
                        'subFolders': 0, 'subFiles': 0, 'depth': depth}
    for child in folder.get('childrenFiles', []):
        copy_id = service.files().copy(
            fileId=child.get('id'),
            body={'name': child.get('name'),
                  'parents': [DESTINATION_FOLDER]}).execute()['id']
        mappingdict = {'id': child.get('id'),
                       'copy_id': copy_id,
                       'parent_id': folder.get('folderID'),
                       'name': child.get('name')}
        fileChildMapping.append(mappingdict.copy())
        counts[folderID]['subFiles'] += 1
    for child in folder.get('childrenFolders', []):
        counts[folderID]['subFolders'] += 1
        createFileMapping(counts, child, depth+1, fileChildMapping)
    return fileChildMapping


# I need to complete this function - running out of time #
# ----------------------------------------------------- #
def organizeFolders(folderMapping):
    try:
        service = drive_service()
        for element in folderMapping:
            logging.debug('Moving folder ID:{}'.format(element.get('id')))
            file = service.files()\
                .get(fileId=element.get('id'), fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))

            file = drive_service.files().update(
                fileId=element.get('id'),
                addParents=element.get('parent_id'),
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
        logging.info('Succesfully organized folders')
        return True
    except NameError:
        logging.error('Error while organizing folders{}'.format(NameError))


# We store the folder structure
folderStructure = genFolderStructure(
    [{"id": FOLDER_TO_SEARCH, "name": "Interview"}])
print(folderStructure)

# Generate the folder mapping while creating the new folders in the dest folder
folderMapping = createFolderMapping(
    countsDict, folderStructure, 0, folderChildMapping)
# Generate the file mapping while copying the new files to the dest folder
fileMapping = createFileMapping(
    countsDict, folderStructure, 0, fileChildMapping)

# organizeFolders(folderStructure)
# organizeFiles(folderStructure)

# I ran out of time in this section but the logic is there. Since
# we have all the mappings and the folder structure, we just to use
# the Drive API update method to remove the old parent and add the new
# parent ID based on the mappings to all files and folders.
# We need to do it recursively and starting from the highest depth of the tree
