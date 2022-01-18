# Assesment 2 - Write a script to generate a report that shows number
# of files and folders for each folder under this folder id(recursively)
# and a total of nested folders for the source folder.

from google_functions.get_folder_structure import genFolderStructure
import json

FOLDER_TO_SEARCH = "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"  # folder ID to search


def countChildren(counts, folder, depth):
    """
    Gets each item of dict (folder structure) and expands each child.
    For each child counts the number of files/folders and increase the
    counters.
    """
    childrenFolders = folder.get('childrenFolders', [])
    childrenFiles = folder.get('childrenFiles', [])
    folderID = folder['folderID']
    counts[folderID] = {'folderName': folder['folderName'],
                        'depth': depth,
                        'subFolders': len(childrenFolders),
                        'subFiles': len(childrenFiles)}
    for child in folder.get('childrenFolders', []):
        countChildren(counts, child, depth+1)


def cumulativeCountChildren(counts, folder, depth):
    """
    Cumulative counts per folderID and returns the total counters
    for the number of files and folders within the folderID
    """
    childrenFolders = folder.get('childrenFolders', [])
    childrenFiles = folder.get('childrenFiles', [])
    folderID = folder['folderID']
    counts[folderID] = {'folderName': folder['folderName'],
                        'depth': depth,
                        'subFolders': len(childrenFolders),
                        'subFiles': len(childrenFiles)}
    for child in childrenFolders:
        subFolders, subFiles = cumulativeCountChildren(counts, child, depth+1)
        counts[folderID]['subFolders'] += subFolders
        counts[folderID]['subFiles'] += subFiles
    return (counts[folderID]['subFolders'], counts[folderID]['subFiles'])


# Empty dictionary to store the results of cumulativeCountChildren
countsDict = {}

# We call the genFolderStructure to generate the folder structure dict
filesAndFolders = genFolderStructure(
    [{"id": FOLDER_TO_SEARCH, "name": "Interview"}])

# Call cumulativeCountChildren with folder structure dict and depth=0
totalFolders, totalFiles = cumulativeCountChildren(
    countsDict, filesAndFolders, 0)

# Printing countsDict
print(json.dumps(countsDict, indent=2))
# Printing total # of folders and files
print('Total Folders: {}, Total Files: {}'.format(totalFolders, totalFiles))
