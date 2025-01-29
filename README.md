# WebTree

WebTree helps you to fully flatten a web directory listing into a file tree. Just like the `tree` command on linux would do. 
To achieve this it recursively parses the directory listing from the given base URL downwards (links upwards are ignored).

It was created in the course of a project parsing leak pages of ransomware groups in the Tor network. It was therefore tested in combination with the `torsocks` utility. 

## Usage

`webtree.py <URL> <OUTFILE>`

The script requires the target URL to the directory listing that should be parsed recursively as well as the path/ name to the output file.


