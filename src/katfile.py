import globalvar
import pykeyboard
import os

globalvar = globalvar.Globalvar()

class Katfile():
    
    def __init__(self):
        self.k = pykeyboard.PyKeyboard()

    #login on to rapidgator.net
    def login(self, browser, account):
        
        # Go to the rapidgator homepage
        url = 'http://katfile.com'
        browser.visit(url)
        
        if browser.is_text_present('Login'):
            url = 'http://katfile.com/login.html'
            browser.visit(url)
            
            login_field = globalvar.getElement(browser, 'name', 'login')

            login_field[0].fill(account['username'])
            
            password_field = globalvar.getElement(browser, 'name', 'password')

            password_field[0].fill(account['password'])
        
            submit_button = globalvar.getElement(browser, 'name', 'submit')
        
            submit_button.first.click()
        
    def upload(self, browser, files, account):
    
        self.login(browser, account)
            
        url = 'http://katfile.com/?op=upload'
        browser.visit(url)
            
        for f in files: 
            browser.driver.find_element_by_id('file_0').send_keys(f) 
            globalvar.sleep(10)
           
        filename_fields = globalvar.getElement(browser, 'xpath', '//table[@id="files_list"]//font[@class="xfname"]')
        delete_btns = globalvar.getElement(browser, 'xpath', '//table[@id="files_list"]//img')
        
        filenames = []
        for i in range(0, len(delete_btns)):
            filename = filename_fields[i]['innerHTML']
            
            if filename not in filenames:
                filenames.append(filename)
            else:
                delete_btns[i].click()
             
        upload_btn = globalvar.getElement(browser, 'xpath', '//*[@id="upload_controls"]/input[1]')
        upload_btn.click()
            
        times = 0
        while browser.is_text_not_present('Files Uploaded'):
            times += 1
            globalvar.sleep(10)		
    
            print('uploading {0}'.format(times))
            
            if times >= 100:
                
                active_window = globalvar.get_active_window_title()
                
                command = 'wmctrl -a KatFile'
                os.system(command)
                
                self.k.press_key('Return')
                self.k.release_key('Return')
            
                command = 'wmctrl -a {0}'.format(active_window)
                os.system(command)
                
                return 0
                
        textarea = globalvar.getElement(browser, 'xpath', '//*[@id="container"]/div/div[2]/div/div[1]/textarea')
            
        url_text = textarea.value
        
        urls = url_text.split('\n')
        
        for url in urls:
            print (url)
        
        if urls[-1] == '':
            del urls[-1]
    
        return urls
            
            
            
            
            
            