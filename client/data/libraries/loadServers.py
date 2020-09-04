class serversManagment():

    def load(self,file_path):
        self.file_path = file_path
        try:
            with open(file_path, "r") as f:
                data = f.read()
                f.close()
        except FileNotFoundError:
            open(file_path, "w").close()
            data = ""
        
        self.data = data.split("\n")
    
    def add(self,link):
        if link not in self.data and link!="":
            with open(self.file_path,"a") as f:
                f.write(link+"\n")
                f.close()
            self.data.append(link)
    
    def digest(self):
        return self.data[:]


    def remove(self,link):
        try:
            self.data.remove(link)
            with open(self.file_path, "w") as f:
                f.write("\n".join(self.data)+"\n")
                f.close()
        except:
            pass