# TL;DR Generates a folder structure dict based on a folder ID
#
# Breadth-first search recursively will use a FIFO list called
# listFilesFolders which contains a dictionary. Once the dictionary
# is set it will return the node (dictionary itself) unless
# there are more folders to "expand". The function will return a
# dict with all the folders (w/ subfolders) and files inside the parent folder


from google_prv import google_service
import logging

FOLDER_MIMETYPE = "application/vnd.google-apps.folder"
QUERY_WTH_FOLDER = "'{}' in parents and mimeType='{}'"
QUERY_WITHOUT_FOLDER = "'{}' in parents and not mimeType='{}'"


def getChildrenFoldersByfolderID(folderID):
    """Based on a folderID, get all children folders
    Returns a dictionary with all children folders
    """
    folderquery = QUERY_WTH_FOLDER.format(
        folderID,
        FOLDER_MIMETYPE)
    childrenFoldersDict = (
        google_service.drive_service()
        .files()
        .list(q=folderquery, spaces="drive",
              fields="files(id, name, mimeType)")
        .execute()
    )

    return childrenFoldersDict["files"]


def getChildrenFilesById(folderID):
    """Based on a folderID, gets all the files inside of it
    Returns a dictionary wth the name and id of each files
    """
    queryWithoutFolder = QUERY_WITHOUT_FOLDER.format(
        folderID, FOLDER_MIMETYPE
    )
    childrenFilesDict = (
        google_service.drive_service()
        .files()
        .list(q=queryWithoutFolder, spaces="drive",
              fields="files(name, id, mimeType)")
        .execute()
    )
    logging.debug('folderID {} has the childres: {}'.format(
        folderID, childrenFilesDict))
    return childrenFilesDict["files"]


def getParentName(folderID):
    """Retrieves parent name from folderID and returns it """
    parentfolder = google_service.drive_service()\
        .files()\
        .get(fileId=folderID).\
        execute()
    parentname = "Title: {}".format(parentfolder["name"])
    parenttype = (parentfolder["mimeType"])
    logging.debug('Parent name:{}\nFolderID:{}'.format(parentname,
                                                       folderID))
    return parentname, parenttype


def genFolderStructure(queue=[]):
    """Based on a folderID, get all children files and folders.
    Returns a list with the structure of the parent folderID.
    """
    listFilesFolders = {}
    while len(queue) > 0:
        currentFolder = queue.pop()
        childrenFolders = getChildrenFoldersByfolderID(currentFolder["id"])
        childrenFiles = getChildrenFilesById(currentFolder["id"])
        parentName, parentType = getParentName(currentFolder["id"])
        listFilesFolders["folderName"] = currentFolder["name"]
        listFilesFolders["folderID"] = currentFolder["id"]
        listFilesFolders["parentName"] = parentName
        listFilesFolders["mimeType"] = parentType
        if len(childrenFiles) > 0:
            listFilesFolders["childrenFiles"] = childrenFiles

        if len(childrenFolders) <= 0:
            return listFilesFolders

        listFilesFolders["childrenFolders"] = []
        for child in childrenFolders:
            queue.append(child)
            listFilesFolders["childrenFolders"].append(
                genFolderStructure(queue))
    logging.debug('ListFileFolder: {}'.format(listFilesFolders))
    return listFilesFolders
