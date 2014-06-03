import sys
import os
import xml.etree.ElementTree as ET
import json

class JavaFile(object):
    def __init__(self, fileName):
        self.line_coverage = 0
        self.branch_coverage = 0
        self.imports = []
        f = open(fileName)
        try:
            self.fileName = f.name.split("/")[-1]
            lines = 0
            for line in f:
                lines += 1
                packageIndex = line.find("package")
                if packageIndex!= -1:
                    self.packageName = line[packageIndex + 7 : -1].strip()[:-1]

                importIndex = line.find("import")
                if importIndex != -1:
                    self.imports.append(line[importIndex + 6 : -1].strip()[:-1])

            self.numOfLines = lines
            

        finally:
            f.close()

    def getPackageName(self):
        return self.packageName

    def getNumOfLines(self):
        return self.numOfLines

    def getImports(self):
        return self.imports

    def getFileName(self):
        return self.fileName

    def __repr__(self):
        return self.getFileName() + ", size: " + str(self.getNumOfLines()) + "," + "line: " + str(self.line_coverage) + ", branch:" + str(self.branch_coverage)
    
    def setLineCoverage(self, line_coverage):
        self.line_coverage = line_coverage

    def setBranchCoverage(self, branch_coverage):
        self.branch_coverage = branch_coverage



class JavaPackage(object):
    def __init__(self, package_name):
        self.numOfLines = 0
        self.name = package_name
        self.line_coverage = 0
        self.branch_coverage = 0

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

    results = {}
    build(dir_name, results)

    root = ET.parse(cobertua_file).getroot()

    for packageDom in root.iter("package"):
        #packageAttributes = package.attrib
        (package, filelist) = results.get(packageDom.attrib["name"], (None, None))

        if package is not None:
            package.setLineCoverage(float(packageDom.attrib["line-rate"]))
            package.setBranchCoverage(float(packageDom.attrib["branch-rate"]))

        if filelist is not None:
            for classDom in packageDom.iter("class"):
                for i in range(len(filelist)):
                    if classDom.attrib["filename"].split("/")[-1] == filelist[i].getFileName():
                        filelist[i].setLineCoverage(float(classDom.attrib["line-rate"]))
                        filelist[i].setBranchCoverage(float(classDom.attrib["branch-rate"]))
                        break


    packagelist = list(results.keys())
    table = [[0] * len(packagelist)] * len(packagelist) # two dimensional array

    for i in range(len(packagelist)):
        filelist = results[packagelist[i]][1]
        for j in range(len(packagelist)):
            for file_ in filelist:
                for imports in file_.getImports():
                    if imports.find(packagelist[j]) != -1:
                        table[i][j] += 1


    packages = []
    for packagename in packagelist:
        package = results[packagename][0]
        m = {}
        m["name"] = package.getName()
        m["size"] = package.getNumOfLines()
        m["line-rate"] = package.getLineCoverage()
        m["branch-rate"] = package.getBranchCoverage()
        packages.append(m)

    links = []
    for i in range(len(packagelist)):
        for j in range(len(packagelist)):
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


