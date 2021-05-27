# CuriousCatArchiver
A tool to archive and view public [CuriousCat](https://curiouscat.qa/) answer feeds

## Archiver


### Dependancies
	Python 3.7.9
    Requests Module

### Usage

    usage: python curiouscatarchive.py [-h] [-f] [-v] [-l] [-n THREADS] Username
    Create a local json archive of CuriousCat accounts.
    
    positional arguments:
      Username              The Username of the account to archive, or file containing usernames
    
    optional arguments:
      -h, --help            show this help message and exit
      -f, --file            use a file containing a list of usernames on seperate lines instead
      -v, --verbose         Display verbose Output
      -l, --local           Automatically Download Local Copys
      -n THREADS, --concurrentDownloads THREADS           Number of Accounts To Download At Once (Default: 5)
## Viewer
The viewer can be opened in a browser and used to browse Json files just like the regular CuriousCat interface, If opening a json file with media stored locally the directory structure must be as shown.
```
├── viewer.html
├── CCArchive<USERNAME>
    ├── <Archive>.json
    └── Media
        ├── file1
        ├── file1
        ├── file3
        ⋮
