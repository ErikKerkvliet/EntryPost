import globalvar
import rapidgator
import bigfile
import katfile
import entryData
import animeSharing
import hcapital
import getAccount

from splinter import Browser

globalvar = globalvar.Globalvar()
rapidgator = rapidgator.Rapidgator()
bigfile = bigfile.Bigfile()
katfile = katfile.Katfile()
entryData = entryData.Config()
animeSharing = animeSharing.AnimeSharing()
hcapital = hcapital.Hcapital()
getAccount = getAccount.GetAccount()

class Main():
    def __init__(self):
        self.hosting = 'katfile'
    
    def main(self, browser, entry):
        rapidgatorAccount = getAccount.getAccount('rapidgator', 1)
        bigfileAccount = getAccount.getAccount('bigfile')
        katfileAccount = getAccount.getAccount('katfile')
        animeSharingAccount = getAccount.getAccount('animesharing')
        
        url = 'http://hcapital.tk/?show=entry&id={0}'.format(entry) 
        browser.visit(url)
    
        title = globalvar.getElement(browser, 'id', 'info_title')['innerHTML']
                
        if 'Vol. ' in title:
            entryType = 'ova'
        else:
            entryType = 'game'
        
    
        #get image urls from hcapital
        imgUrls = hcapital.getImagesHcapital(browser)
            
        print('Getting the images succeeded')
    
        # get the rapidgator links  
        rapidUrls = hcapital.getRapidgatorUrls(browser, entry)
        
        print('Getting the rapidgator urls succeeded')
            
        hostingUrls = []
        
        if len(rapidUrls[0]) == 0:
            hostingUrls.append([])
            
        for i in range(0, len(rapidUrls)):
            # get the name all the files have to be like
            go_on = False
            
            filename = 'Back to previous page'
            
            while filename == 'Back to previous page':
                if len(rapidUrls) > 0 and len(rapidUrls[i]) > 0:
                    filename = hcapital.getFilename(browser, rapidUrls[i][0])
                
                else:
                    go_on = True
                    break
            
            if go_on == True:
                continue 
                
            print('The filename of this entry is: {0}'.format(filename))
    
            print('Downloading files')
    
            rapidgator.download(browser, rapidUrls[i], rapidgatorAccount)
            
            downloading = 0
            while globalvar.checkDownloadStatus(filename) != len(rapidUrls[i]):
                globalvar.sleep(200)
                
                downloading += 1
                
                if downloading == 20:
                    print('Downloading failed')
                    
                    globalvar.removeFiles(filename)
                    
                    rapidgator.download(browser, rapidUrls[i], rapidgatorAccount)
                    
                print('downloading...')
                
            print('Files downloaded')
    
            files = globalvar.getFilesFromFolder(filename)
           
            while True:
                if self.hosting == 'katfile':
                    urls = katfile.upload(browser, files, katfileAccount)
                    if urls == 0:
                        self.hosting = 'bigfile'
                        continue
                    else:
                        hostingUrls.append(urls)
                else:
                    hostingUrls.append(bigfile.upload(browser, files, bigfileAccount))
    
                if len(hostingUrls[i]) != len(rapidUrls[i]):
                    print('Uploaded file amount doesn\'t match with the expected amount')
        
                    print('bigfile: {0} files, Rapidgator: {1} files'.format(len(hostingUrls[i]), len(rapidUrls[i])))
                                     
                    del hostingUrls[-1]
                else:
                    break
                    
            
                
            print('removing files from download folder')
            
            globalvar.removeFiles(filename)
        
        print('Uploading images so they can be used for the post')
        
        images = animeSharing.uploadImages(browser, imgUrls)
            
        print('Getting the post data')
    
        post = hcapital.editEntryAndGetPost(browser, entry, entryType, images, hostingUrls, rapidUrls)           
        
        globalvar.sleep(3, 5)
        
        print('Creating the post on anime-sharing')
    
        animeSharing.createPost(browser, post, entryType, animeSharingAccount)
    
        return 0
    
globalvar.removeAllFiles()

postsMade = 1

prof = {}
prof["browser.download.folderList"] = 2
prof["browser.download.manager.showWhenStarting"] = False
prof["browser.download.dir"] = globalvar.download_folder
prof["browser.helperApps.neverAsk.saveToDisk"] = "application/octet-stream"

with Browser('firefox', profile_preferences=prof) as browser:
    
    browser.driver._is_remote = False

    while postsMade < 11:
    
        print('=================== Start preparing the new submit ================={0}=='.format(globalvar.getTime()))
    
        # get entry and latest
        data = entryData.readConfig(browser)

        entry = data[0]
        
        print('The entry nr that will be handled = {0}'.format(entry))
           
        main = Main()
        
        state = main.main(browser, entry)
    
        if state == None:
            print('state was incorrect')
    
            continue
        else:
            
            while True:
                if animeSharing.submit(browser):
                    break
                else:
                    globalvar.sleep(1000, 1800)
    
            print('========= Post nr: {0} ========='.format(postsMade))
    
        
        entryData.writeConfig(data)
        
        print('============================={0}============================'.format(globalvar.getTime()))
        
        postsMade += 1
        
        
