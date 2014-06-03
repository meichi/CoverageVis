import sys
import os

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
        return self.getFileName() + ":" + str(self.getNumOfLines())


    



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
        return self.getName() + ":" + str(self.getNumOfLines())



def build(dir_name, package_to_files):
    if not os.path.exists(dir_name):
        return

    if os.path.isfile(dir_name):
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

#    print results


    for (k, v) in results.items():
        print "packageName: " + k + ","
        for file_ in v[1]:
            print file_.getFileName() + ":" + str(file_.getImports())
            print

        print "\n\n"


