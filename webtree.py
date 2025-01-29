import requests
from bs4 import BeautifulSoup
import urllib3
import logging
import datetime
import os
import click
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(filename=os.path.join(os.getcwd(), f'webtree.log'), level=logging.INFO, format='')

class Node:
    # node_type: 0=root, 1=file, 2=directory, 3=failure
    def __init__(self, name, node_type, predecessor):
        self.name = name
        self.node_type = node_type
        self.predecessor = predecessor
        self.successors = list()

    def add_successor(self, successor):
        self.successors.append(successor)

def traverse(node):
    request_url = build_url(node)
    logging.info(request_url)
    fetch_result = fetch_url(request_url)
    if not fetch_result[0]:
        node.add_successor(Node("? FAILED TO FETCH ?", 3, node))
        return node
    soup = BeautifulSoup(fetch_result[1], 'html5lib')
    all_links = soup.find_all("a")   
    for link in all_links:
        href = str(link.attrs['href'])
        if(href.startswith('?') or href.startswith('/') or href.startswith('../')):
            # link is for sorting or parent
            continue
        elif(href.endswith('/')):
            # link is to directory
            successor = Node(href, 2, node)
            node.add_successor(traverse(successor))
        else:
            # is file
            node.add_successor(Node(href, 1, node))
    return node


def fetch_url(url):
    for i in range(1,3):
        try:
            resp = requests.get(url, verify=False)
            if resp.status_code == 200:
                return (True, resp.content)
        except:
            pass
    return (False, "")

    
# Builds url from a node and its assigned predecessors
def build_url(node):
    url = ""
    current_node = node
    while current_node.predecessor is not None:
        url = f"{current_node.name}{ '/' if not current_node.name.endswith('/') else ''}{url}"
        current_node = current_node.predecessor
    url = f"{current_node.name}{ '/' if not current_node.name.endswith('/') else ''}{url}"
    return url


def print_tree(node, prefix=''):
    output = f'{prefix}{node.name}\n'
    for child in node.successors:
        output = output + print_tree(child, "|  " + prefix)
    return output    

@click.command()
@click.argument('url')
@click.argument('outfile')
def entrypoint(url, outfile):
    """Recursively explores the directory listing at URL and writes the resulting tree to OUTFILE"""
    logging.info(f'Starting new run at: {datetime.datetime.now()}')
    root = Node(url, 0, None)
    root= traverse(root)

    visualization = print_tree(root)
    with open(outfile, 'w+') as f:
        f.write(visualization)
    print(visualization)
    logging.info(f'Finished current run at: {datetime.datetime.now()}')


if __name__ == "__main__":
    entrypoint()
   