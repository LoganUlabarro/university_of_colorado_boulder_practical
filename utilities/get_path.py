import os

def getPathToFile(fileName, relativePathInput, fileTypeExtension='csv'):
        uploadDirectory = relativePathInput
        currentDirectory = os.path.dirname(__file__)
        relativePath = os.path.join(currentDirectory, uploadDirectory)
        fileToUpload = os.path.join(relativePath, fileName + '.' + fileTypeExtension)
        cannonFileToUpload = os.path.realpath(fileToUpload)
        return cannonFileToUpload