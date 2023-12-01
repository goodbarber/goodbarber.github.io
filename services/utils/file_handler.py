import codecs
import pystache


def load_template(filename):
    with codecs.open(filename, "r", "utf-8") as f:
        return pystache.parse(f.read())


def save_html(filename, content):
    with codecs.open(filename, "w", "utf-8") as f:
        f.write(content)
