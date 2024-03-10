from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import xml.etree.ElementTree as ET
import requests


xml_file = 'notes.xml'
try:
    tree = ET.parse(xml_file)
    root = tree.getroot()
except FileNotFoundError:
    root = ET.Element('notes')
    tree = ET.ElementTree(root)

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def add_note(topic, text, timestamp):
    note = root.find(f"./note[@topic='{topic}']")
    if note is None:
        note = ET.SubElement(root, "note", topic=topic)
    entry = ET.SubElement(note, "entry", timestamp=timestamp)
    ET.SubElement(entry, "text").text = text
    tree.write(xml_file)
    return True

def get_notes(topic):
    notes_list = []
    note = root.find(f"./note[@topic='{topic}']")
    if note is not None:
        for entry in note.findall('entry'):
            notes_list.append({"timestamp": entry.get('timestamp'), "text": entry.find('text').text})
    return notes_list

def query_wikipedia_and_update(topic):
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": topic,
        "limit": 1,
        "namespace": 0,
        "format": "json",
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if data[1]:
        article_title = data[1][0]
        article_url = data[3][0]
        if append_wikipedia_link_to_topic(topic, article_title, article_url):
            return article_url
    return False
def append_wikipedia_link_to_topic(topic, article_title, article_url):
    note = root.find(f"./note[@topic='{topic}']")
    if note is None:
        note = ET.SubElement(root, "note", topic=topic)
    entry = ET.SubElement(note, "entry", timestamp="Wikipedia")
    ET.SubElement(entry, "text").text = f"Wikipedia link: {article_url} - {article_title}"
    tree.write(xml_file)
    return True

server = ThreadedXMLRPCServer(('localhost', 6666))

server.register_function(add_note, 'add_note')
server.register_function(get_notes, 'get_notes')
server.register_function(query_wikipedia_and_update, 'query_wikipedia_and_update')
print("Server running on port 6666...")
server.serve_forever()
