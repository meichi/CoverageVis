import sys
import os
import xml.etree.ElementTree as ET
import json


class Project(object):
    def __init__(self, line_coverage = 0, branch_coverage = 0):
        self.line_coverage =  line_coverage
        self.branch_coverage = branch_coverage
        self.packages = []

    def addPackages(self, package):
        self.packages.append(package)

    def getPackages(self):
        return self.packages





class JavaFile(object):
    def __init__(self, name, pathName, line_coverage = 0.0, branch_coverage = 0.0, numOfLines = 0):
        self.name = name
        self.pathName = pathName
        self.line_coverage = line_coverage
        self.branch_coverage = branch_coverage
        self.imports = []
        self.numOfLines = numOfLines

    def getPathName(self):
        """return absolute name like: org/apache/commons/MyClass.java"""
        return self.pathName
    
    def getFileName(self):
        """return just file name like: ArrayList.java """
        return self.pathName.split("/")[-1];


    def parseFile(self, dir_name):
        if dir_name[-1] != "/":
            dir_name = dir_name + "/"

        f = open(dir_name + self.getPathName())
        lines = 0
        try:
            for line in f:
                lines += 1
                importIndex = line.find("import")
                if importIndex != -1:
                    self.addImport(line[importIndex + 6: -1].strip()[:-1])
            self.numOfLines = lines

        finally:
            f.close()


    def addImport(self, import_):
        self.imports.append(import_)

    def getPackageName(self):
        return self.packageName

    def getNumOfLines(self):
        return self.numOfLines

    def getImports(self):
        return self.imports


    def __repr__(self):
        return self.getFileName() + ", size: " + str(self.getNumOfLines()) + "," + "line: " + str(self.line_coverage) + ", branch:" + str(self.branch_coverage)
    
    def setLineCoverage(self, line_coverage):
        self.line_coverage = line_coverage

    def setBranchCoverage(self, branch_coverage):
        self.branch_coverage = branch_coverage



class Package(object):
    def __init__(self, name = None, line_coverage = 0, branch_coverage = 0, numOfLines = 0):
        self.numOfLines = numOfLines
        self.name = name
        self.line_coverage = line_coverage
        self.branch_coverage = branch_coverage
        self.files = []

    def addFile(self, javaFile):
        self.files.append(javaFile)

    def getFiles(self):
        return self.files

    def getName(self):
        return self.name

    def getNumOfLines(self):
        return self.numOfLines

    def addLines(self, lines):
        self.numOfLines += lines

    def __repr__(self):
        return self.getName() + ":" + str(self.getNumOfLines()) + ", line:" + str(self.line_coverage) + ", branch:" + str(self.branch_coverage)

    def setLineCoverage(self, line_coverage):
        self.line_coverage = line_coverage

    def setBranchCoverage(self, branch_coverage):
        self.branch_coverage = branch_coverage

    def getLineCoverage(self):
        return self.line_coverage

    def getBranchCoverage(self):
        return self.branch_coverage





def build(dir_name, package_to_files):
    print dir_name
    if not os.path.exists(dir_name):
        return

    if os.path.isfile(dir_name):
        if dir_name[-4:] != "java":
            return

        new_file = JavaFile(dir_name)
        packageName = new_file.getPackageName()
        if packageName in package_to_files:
            pair = package_to_files[packageName]
            pair[0].addLines(new_file.getNumOfLines())
            pair[1].append(new_file)
        else:
            #create package
            new_package = JavaPackage(new_file.getPackageName())
            new_package.addLines(new_file.getNumOfLines())
            #create tuple
            pair = (new_package, [ new_file ])
            #add tuple to map
            package_to_files[new_package.getName()] = pair
        return


    for cur_file in os.listdir(dir_name):
        build(dir_name + "/" +  cur_file, package_to_files)



if __name__ == "__main__":
    dir_name = sys.argv[1]
    cobertua_file = sys.argv[2]



#    results = {}
#    build(dir_name, results)

    root = ET.parse(cobertua_file).getroot()

    project = Project(float(root.attrib["line-rate"]), float(root.attrib["branch-rate"]))

    for packageDom in root.iter("package"):
        cur_package = Package(name = packageDom.attrib["name"], line_coverage = float(packageDom.attrib["line-rate"]), branch_coverage = float(packageDom.attrib["branch-rate"]) )
        project.addPackages(cur_package)
        for classDom in packageDom.iter("class"):
            if os.path.exists(dir_name + classDom.attrib["filename"]):
                cur_class = JavaFile(name = classDom.attrib["name"], pathName = classDom.attrib["filename"], line_coverage = float(classDom.attrib["line-rate"]), branch_coverage = float(classDom.attrib["branch-rate"]))
                cur_package.addFile(cur_class)
                cur_class.parseFile(dir_name)
                cur_package.addLines(cur_class.getNumOfLines())
        if cur_package.getNumOfLines() == 0:
            del project.getPackages()[-1]


    """
    for p in project.getPackages():
        print "package name: " + p.getName() + ", num of lines: " + str(p.getNumOfLines()) + ", num of classes: " + str(len(p.getFiles()))
        for klass in p.getFiles():
            print "\t" + klass.getFileName() + ", import:" + str(klass.getImports())
        print "\n\n"
    """

    packagelist = project.getPackages()
    package_len = len(packagelist)
    table = [[0] * package_len] * package_len # two dimensional array

    for (i, row_package) in enumerate(packagelist):
        filelist = row_package.getFiles()
        for (j, col_package) in enumerate(packagelist):
            for file_ in filelist:
                for imports in file_.getImports():
                    if imports.find(col_package.getName()) != -1:
                        table[i][j] += 1

    packages = []
    for package in packagelist:
        m = {}
        m["name"] = package.getName()
        m["size"] = package.getNumOfLines()
        m["line-rate"] = package.getLineCoverage()
        m["branch-rate"] = package.getBranchCoverage()
        packages.append(m)

    links = []
    for i in range(package_len):
        for j in range(package_len):
            m = {}
            m["source"] = i
            m["target"] = j
            m["dependency"] = table[i][j]
            links.append(m)


    jsonObj = {}
    jsonObj["packages"] = packages
    jsonObj["links"] = links

    
    with open('myjson.json', "w") as outfile:
        json.dump(jsonObj, outfile)

    #print results
    #for (packagename, (package, filelist)) in results.items():
    #    print "packageName: " + packagename + "," + "size: " + str(package.getNumOfLines()) + ", lineC: " + str(package.getLineCoverage()) + ", branC:" + str(package.getBranchCoverage())
    #    for file_ in filelist:
    #        print file_
    #        print file_.getImports()
    #        print

    #    print "\n\n"


