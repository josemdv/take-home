# Assesment 1 - Write a script to generate a report that shows number
# of files and folders in total for the source folder.

from google_functions.get_folder_structure import genFolderStructure
import json

FOLDER_TO_SEARCH = "1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V"  # folder ID to search


# Flattening the dict to search for different mimeTypes
filesAndFolders = json.dumps(genFolderStructure(
    [{"id": FOLDER_TO_SEARCH, "name": "Interview"}]))

# If you feel like getting a full representation of the dict containing all
# files, folders and subfolders, uncomment this line.
# print(filesAndFolders)

# We load the different mimeTypes that we can search for
with open('mimetypes.json') as json_file:
    mimeTypes = json.load(json_file)

# Now that we have a flatten list of the structure and all the
# mimeTypes that Google Drive can return, we print them
for mimeType, humanReadableType in mimeTypes.items():
    print('The searched folder contains {} {}'.format(
        filesAndFolders.count(mimeType),
        humanReadableType))

# Note that the report counts the parent folder
