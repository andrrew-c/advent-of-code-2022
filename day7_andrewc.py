import re
# Update the day number
dayN = 'day7'

# Day N data
data_path = f'andrewc_2022/data/{dayN}_input.txt'

with open(data_path, 'rt') as f: file = f.read()

# Initialise folder structure
fs = {}

# Current folder
cf = {}

#######################################
## Define a set of regular expressions
#######################################
# Is this line a command (B = Boolean)?
rgx_cmdB = re.compile(r'^\$')

# Get command (R = return)
rgx_cmdR = re.compile(f'(?<=^\$ )[a-z]+', re.MULTILINE)

# Extract file size
rgx_fsize = re.compile(r'^[0-9]+')

# Get folder for cd command
rgx_folder = re.compile(r'(?<=^\$ cd ).+')

# Get name of directories (after calling 'ls' command)
rgx_dir = re.compile(r'(?<=dir )[a-z0-9\.]+$', re.MULTILINE)
 
# File sizes 
rgx_fsize = re.compile(r'^[0-9]+', re.MULTILINE)

# Parse ls command
rgx_parsels = re.compile(r'(?<=\$ ls\n)', re.MULTILINE)

# Get all folder names for changes
rgx_cdnames = re.compile(r'(?<=^\$ cd )[a-z\/]+$',  re.MULTILINE)

# Find everything after an ls command but before the next command starts
rgx_ls = re.compile('(?<=\$ ls\n)[0-9a-z\n\s\.]+(?=^\$)?', re.MULTILINE)

###########################################
## End: Define a set of regular expressions
###########################################

class Folder():

    all_folders = []

    def __init__(self, name, parent):

        self.name = name
        self.parent = parent

        self.files = []

        # Child folders/file sizes
        self.children = None

    def getChild(self, name):

        """ Return the folder that matches this name"""
        # Extract folder objects (ignore integer children)
        # folders = [folder for folder in self.children if type(folder) != int]
        return [folder for folder in self.children if folder.name==name][0]

    def getChildrenNames(self):

        """Return list of all children (folders)""" 

        return [child.name for child in self.children]

    def sumValues(self):

        """ For a given folder return the total size of files and files within all sub-folders"""

        # If this folder only contains files - return the size of those files
        if self.children is None:
            return sum(self.files)

        # Else, there's at least one file directory
        else:
            return sum(self.files) + sum([child.sumValues() for child in self.children])




# Initialise parent at None
currentFolder = None
parent = None

# Read a line
line = file.split('\n')

import pdb
pos = 0
# cpos = 0
folders = []
verbose= False
while pos < len(file):

    # What is happpening
    if verbose:
        print(f"*** File position {pos:,}")
        print(f"File left pos+10 {file[pos:pos+10]}")

    # Get next command
    cmd_ = rgx_cmdR.search(file[pos:])
    if cmd_ is None:
        if verbose: print(f"No more commands - pos is {pos:,}")
        pass

        
    cmd = cmd_.group()
     
    if verbose: print(f"***** Command is {cmd}")

    if cmd == 'cd':

        # What is the folder we're changing to?
        folderName = rgx_folder.search(file[pos:]).group()

        # move up one level
        if folderName == '..':

            if verbose: print(f"..... Moving up from '{currentFolder.name}' to '{currentFolder.parent.name}'")
            # Move up one level from current
            currentFolder = currentFolder.parent
            pos += rgx_cmdR.search(file[pos+1:]).span()[0]-1

        # Else changing folder within the current working directory
        else:

            if verbose: print(f"----> Add folder called {folderName}")

            # If not current folder - just add the root folder
            if currentFolder is None:
                root = Folder(folderName, parent=currentFolder)
                currentFolder = root
                currentFolder.all_folders.append(currentFolder)
            
            else:
                # Get the child
                currentFolder = currentFolder.getChild(folderName)
                
            pos += rgx_cmdR.search(file[pos+1:]).span()[0]-1
            if verbose: print(f"pos is now {pos}")
            # # Create a folder
            # folders.append(Folder(folderName, parent=currentFolder))
                
            # currentFolder = folders[-1]

            # Move pos to next command

    elif cmd == 'ls':

        # Get contents of ls
        ls_contents = rgx_ls.search(file[pos:])

        if verbose: print(f"<><><> Contents of {currentFolder.name} are:\n{ls_contents.group()}")
        
        ##############
        # Directories
        ##############

        # Directories
        dirs = rgx_dir.findall(ls_contents.group())

        # File sizes (integers)
        currentFolder.files = rgx_fsize.findall(ls_contents.group())
        currentFolder.files = [int(child) for child in currentFolder.files]

        # Get contents of folder
        if len(dirs) > 0: 
            # Add children to current folder
            currentFolder.children = ([Folder(dir, currentFolder) for dir in dirs]) 
            currentFolder.all_folders.extend(currentFolder.children)
        # Update position after getting contents
        pos += ls_contents.span()[1]

########################################################
## Part 1: Find all of the directories with a total size of at most 100000. 
# ## What is the sum of the total sizes of those directories?
########################################################

maxVal = 100000
all_sizes = [folder.sumValues() for folder in root.all_folders]

# Keep sizes within limit
all_sizes1 = [val for val in all_sizes if val <= maxVal]
print(f"Part 1 answer: {sum(all_sizes1):,}")

############################################################
## Part 2: Find the smallest directory that, if deleted, 
## would free up enough space on the filesystem to run the update. What is the total size of that directory?
####################################################################################################################################################################################

# Total size 
totSize = 70000000
minforUpdate = 30000000

# Space needed
minSpaceNeed = abs(totSize - minforUpdate - root.sumValues() )
minSpaceNeed

# Which folders would free up enough space?
foldersFree = [val for val in all_sizes if val >= minSpaceNeed]
 
# What is the smallest folder we can delete
print(f"Part 2: {min(foldersFree)}")