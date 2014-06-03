import xml.etree.ElementTree as ET
import sys



if __name__ == "__main__":
    xml_file = sys.argv[1]

    tree = ET.parse(xml_file)
    root = tree.getroot()

    for package in root.iter("package"):
        print "package attributes:" +  str(package.attrib) + ":"
        for klass in package.iter("class"):
            print "\t class attributes: " + str(klass.attrib)
        print "\n\n"







