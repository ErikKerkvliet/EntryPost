import globalvar

globalvar = globalvar.Globalvar()

class Bigfile():
    
    def __init__(self):
        pass
    
    def login(self, browser, account):
        url = "https://www.bigfile.to/login.php"
        browser.visit(url)
        
        if not browser.is_text_present('Forgot Password'):
            print('Already logged in at BigFile.to')
            
            return True
    
        globalvar.getElement(browser, 'name', 'userName').fill(account['username'])
        globalvar.getElement(browser, 'name', 'userPassword').fill(account['password'])
    
        # Find and click the 'search' button
        button = globalvar.getElement(browser, 'id', 'loginFormSubmit')
        # Interact with elements
        button.click()
    
        globalvar.sleep(10, 20)
    
        if browser.url == "https://www.bigfile.to/indexboard.php" or browser.url == "https://www.bigfile.to/uploadremote.php":
            print("Logged in on to Bigfile")
            
            return True
        else:
            print("Bigfile login failed")
    
            return False
    
    def upload(self, browser, files, account):
    #upload all given files to BigFile and return the file urls
        urls = []
        print('files will now be uploaded to BigFile.to')
        
        for f in files:
            while True:
                self.login(browser, account)
                
                url = "https://www.bigfile.to/index.php"
                browser.visit(url)
            
                upload_textfield = browser.driver.find_element_by_id('uploadFiles1')
                upload_files = browser.driver.find_element_by_id('fakeUploadFiles1')
        
                upload_textfield.send_keys(f) 
                upload_files.send_keys(f) 
        
                globalvar.getElement(browser, 'xpath', '//div[@class="checkbox"]//input').first.click() 
            
                browser.execute_script("copyFileName();")
        
                browser.driver.find_element_by_id('uploadButton').click()
                
                globalvar.sleep(10, 20)
                cont = False
                
                uploading = 0
                while browser.is_text_not_present('Upload Successful'):
                    globalvar.sleep(10, 20)
                    
                    uploading += 1
                    
                    print('Uploading...')
                    
                    if uploading == 40:
                        print('upload failed')
                        
                        cont = True
                        break
                
                if cont:
                    continue
                            
                print('Finished uploading')
            
                link_field = globalvar.getElement(browser, 'id', 'shareLinks')
                
                field_value = link_field.value
                
                url = field_value.split('\n')
                
                if len(url) > 0 and url[-1] == '':
                    del url[-1]
                    
                if len(url) > 0 and url[0] != '' and url[0] != 'undefined':
                    urls.append(url[0])
                    
                    print('uploaded: {0}'.format(urls[-1]))
                    break
            
        return urls

