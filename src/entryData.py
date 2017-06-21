import globalvar

import urllib2

globalvar = globalvar.Globalvar()
    
class Config:
    def __init__(self):
        pass
    
    def readConfig(self, browser):
        entry = 0
        latest = 0
        toDoNrs = []
    
        response = urllib2.urlopen('http://hcapital.tk/sitemap.xml')
        text = response.read()
        splitted = text.split('id=')[-1]
        last = splitted.split('</loc>')[0]
    
        lastEntry = int(last)
        
        entry_add = 1
        latest_add = 1
        while True: 
            entry = 0
            latest = 0
            
            lineNr = 0  
            with open(globalvar.config_file, 'r') as f:
                for line in f:
                    lineNr += 1
                    line.split('\n')
                    if lineNr == 1:
                        entry = int(line)
                    elif lineNr == 2:
                        latest = int(line)
                    elif lineNr == 3:
                        toDoNrs = line.split(',')
                        if len(toDoNrs) > 0:
                            if toDoNrs[0] == '':
                                del toDoNrs[0]
                                
                            if toDoNrs[0] != '':
                                entryNr = int(toDoNrs[0])
                            
                new_entry = entry + entry_add
                new_latest = latest + latest_add
                
                if new_latest > lastEntry and len(toDoNrs) == 0:
                    entryNr = new_entry
                    entry = entryNr
                    entry_add += 1
                elif new_latest <= lastEntry and len(toDoNrs) == 0:
                    entryNr = new_latest
                    latest = entryNr
                    latest_add += 1
                        
                if entry == lastEntry - 50:
                    entry = 1
                    entryNr = 1
    
            url = "http://hcapital.tk/?show=entry&id={0}".format(entryNr)
    
            browser.visit(url)
            
            #check if the browser is on the correct page, if so: break        
            if browser.is_text_present('Released'):
                if browser.is_text_not_present('Not Yet Released'):
                    if browser.is_text_not_present('Crack is needed'):
                        if browser.is_text_not_present('crack is needed'):   
                            if browser.is_text_present('http://rapidgator.net/file/'):   
                                break
    
        return [entryNr, entry, latest]
    
    def writeConfig(self, data):
        entry = data[1]
        latest = data[2]
        
        #post is succesfully done so change the "current" file
        with open(globalvar.config_file, 'rw+') as f:
            lineNr = 0
            toDoNrs = []
            
            for line in f:
                lineNr += 1
    
                if lineNr == 3:   
                    toDoNrs = line.split(',')
                    if len(toDoNrs) > 0:
                        del toDoNrs[0]
                    if len(toDoNrs) > 0 and toDoNrs[0] == '':
                        del toDoNrs[0]
            
            print('editing the config file:\nCurrent entry = {0}\nLatest entry = {1}'.format(entry, latest))
                
            f.seek(0)
            f.truncate() 
              
            f.write(str(entry))
            f.write('\n')
            f.write(str(latest))
            
            if len(toDoNrs) > 0:
                f.write('\n')
                
                toDo = ','.join(toDoNrs)
                
                f.write(toDo)
            
            f.close()
        
