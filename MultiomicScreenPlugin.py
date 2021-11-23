import PyPluMA

class MultiomicScreenPlugin:
    def input(self, filename):
       infile = open(filename, 'r')
       csvfile = open(PyPluMA.prefix()+"/"+infile.readline().strip(),'r')
       self.typeA = infile.readline().strip()
       self.typeB = infile.readline().strip()
       self.header = csvfile.readline().strip()
       self.taxa = self.header.split(',')
       self.ADJ = []
       self.ADJ.append(self.taxa)
       for line in csvfile:
          contents = line.strip().split(',')
          for i in range(1, len(contents)):
              contents[i] = float(contents[i])
          self.ADJ.append(contents)

    def run(self):
       for i in range(1, len(self.ADJ)):
           for j in range(1, len(self.ADJ[i])):
               if (self.typeA == "microbe" and self.typeB == "microbe"):
                   if (self.taxa[i].startswith("\"x") or self.taxa[j].startswith("\"x")):
                       self.ADJ[i][j] = 0.0
               elif ((self.typeA == "microbe" and self.typeB == "metabolite") or
                     (self.typeA == "metabolite" and self.typeB == "microbe")):
                   if ((self.taxa[i].startswith("\"x") and self.taxa[j].startswith("\"x")) or
                           ((not self.taxa[i].startswith("\"x")) and (not self.taxa[j].startswith("\"x")))):
                       self.ADJ[i][j] = 0.0
               else:
                   if ((not self.taxa[i].startswith("\"x")) or (not self.taxa[j].startswith("\"x"))):
                       self.ADJ[i][j] = 0.0
               if (self.ADJ[i][j] != 0):
                   if (i < j):
                       print(self.taxa[i]+"-"+self.taxa[j]+": "+str(self.ADJ[i][j]))


    def output(self, filename):
        outfile = open(filename, 'w')
        for i in range(len(self.ADJ)):
            for j in range(len(self.ADJ[i])):
               outfile.write(str(self.ADJ[i][j]))
               if (j != len(self.ADJ[i])-1):
                   outfile.write(',')
               else:
                   outfile.write('\n')
