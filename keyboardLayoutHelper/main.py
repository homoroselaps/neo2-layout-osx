import xml.etree.ElementTree
import re

file_path = "neo.keylayout"
data = {}
keymap = {}

ascii = {


}


def get_attr_value(elem, attr_name):
    output = None
    try:
        output = dict(elem.items())[attr_name]
    finally:
        return output

def find_usage(query):
    return [k for k, v in keymap.items() if v[0] == query]


def load_ascii():
    with open('ascii.csv','r') as f:
        for line in f:
            parts = line.split('<>')
            ascii[parts[1]] = (parts[0], parts[2])


def main():
    load_ascii()
    keyLayer = 0
    for (ev,el) in xml.etree.ElementTree.iterparse(file_path):
        if el.tag == 'keyMap':
            keyLayer = int(get_attr_value(el, 'index'))+1
        if el.tag == 'key':
            is_action = True if get_attr_value(el, 'action') else False
            keymap[(keyLayer, get_attr_value(el, 'code'))] = (get_attr_value(el, 'action') if is_action else get_attr_value(el, 'output'), is_action)
        if el.tag == 'action':
            data[get_attr_value(el, 'id')] = \
                (get_attr_value(el.find('when'), 'output'),
                 xml.etree.ElementTree.tostring(el, encoding='utf8', method='xml'))

    while True:
        query = input()
        results = []
        if query in data.keys():
            print("action:{0} output:{1} layer:{3}\n {2}".format(query, data[query][0], data[query][1].decode('utf8'), find_usage(query)))
        for k,v in [(k, v) for k, v in data.items() if v[0] == query]:
            print("action:{0} output:{1} layer:{3}\n {2}".format(k, v[0], v[1].decode('utf8'), find_usage(k)))
        for k,v in [(k, v) for k, v in keymap.items() if v[0] == query]:
            print("layer:{0} code:{1} {2}:{3}".format(k[0], k[1], 'action' if v[1] else 'output', v[0]))
        for k,v in [(k, v) for k, v in keymap.items() if k[1] == query]:
            print("layer:{0} code:{1} {2}:{3}".format(k[0], k[1], 'action' if v[1] else 'output', v[0]))
        for k,v in [(k, v) for k, v in ascii.items() if k == query or v[0] == query]:
            print("ascii:{0} symbol:{1} {2}".format(k, v[0], v[1]))


main()