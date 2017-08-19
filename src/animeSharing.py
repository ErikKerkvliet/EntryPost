import globalvar
import random

globalvar = globalvar.Globalvar()

class AnimeSharing():
    
    def __init__(self):
        pass
        
    def login(self, browser, account):
        url = "http://www.anime-sharing.com/forum/login.php?do=login"
        browser.visit(url)
        
        globalvar.sleep(3, 5)
        
        if browser.is_text_present('My Profile') and browser.is_text_present('yuuichi_sagara'):
            print('Already logged in')
    
            return
    
        if browser.url == 'http://www.anime-sharing.com/forum/index.php':
            globalvar.getElement(browser, 'xpath', '//input[@class="fixed_header_login_button"]').first.click()
        
        globalvar.sleep(3, 5)
    
        globalvar.getElement(browser, 'id', 'vb_login_username').fill(account['username'])
        globalvar.getElement(browser, 'id', 'vb_login_password').fill(account['password'])
    
        globalvar.getElement(browser, 'xpath', '//div[@class="blockfoot actionbuttons"]//input[@value="Log in"]').first.click()
        
        globalvar.sleep(3, 5)
        
    def createPost(self, browser, post, entryType, account):
        
        self.login(browser, account)
        
        if entryType == 'ova':
            urlnr = '36'
        else:
            urlnr = '38' 
    
        url = "http://www.anime-sharing.com/forum/newthread.php?do=newthread&f=" + urlnr
        browser.visit(url)
    
        globalvar.sleep(5, 10)
        
        dropdown = globalvar.getElement(browser, 'id', "prefixfield").first
    
        dropdown.select('japanese')
    
        globalvar.sleep(3, 5)
    
        postParts = post.split("?!|]")
    
        subject = postParts[1]
        message = postParts[2]
        tags = postParts[0]
    
        splittedTags = tags.split(',')
    
        if len(splittedTags[-1]) > 30:
            splittedTags[-1] = splittedTags[-1][:30]
            tags = ', '.join(splittedTags)
            
            
        globalvar.getElement(browser, 'id', 'subject').first.fill(subject)
    
        globalvar.sleep(1, 5)
    
        textfields = globalvar.getElement(browser, 'css', 'textarea')
    
        for textfield in textfields:
            if textfield['class'] == 'cke_source cke_enable_context_menu':
                textfield.fill(message)
    
        globalvar.getElement(browser, 'id', 'tagpopup_ctrl').first.fill(tags)
        
    def submit(self, browser):
        
        while True:  
            buttons = globalvar.getElement(browser, 'name', 'sbutton') 
            
            for button in buttons:
                
                print('Finding and clicking the submit button')
                
                if button['value'] == 'Submit New Thread':
                      
                        button.click()
                            
                        globalvar.sleep(30, 60)
                        
                        if browser.is_text_present('This forum requires that you wait 3600 seconds'):
                            print('Post was to soon, must wait 3600 seconds')
                            
                            nr = random.randint(12, 20)
                            for i in range(0, nr):
                                print('sleep {0} of {1}'.format(i+1, nr))
                                
                                globalvar.sleep(100)
                            
                            break
                        else:
                            print('Post was submitted')
    
                            globalvar.sleep(60, 120)
                            
                            return True
                
    def uploadImages(self, browser, images):
        url = "http://i.want.tf/to/"
        
        globalvar.sleep(3, 5)
        
        browser.visit(url)
    
        button = globalvar.getElement(browser, 'id', 'select-remote')
        # Interact with elements
        button.click()
    
        globalvar.sleep(3, 5)
    
        if browser.is_text_present('enter the images URLs you would like to upload', 20):
            
            for image in images:
    
                globalvar.getElement(browser, 'id', 'url').fill(image)
                globalvar.sleep(2, 5)
    
            button = globalvar.getElement(browser, 'id', 'upload-button')
            button.click()
            
            sleep = (len(images) * 10 + 11)
            
            times = 0
            while browser.is_text_not_present('Just uploaded '):
                globalvar.sleep(1)
                times += 1
                
                if times > sleep:
                    import sys
                    sys.exit()
            
            globalvar.sleep(2)
            
            if len(images) == 1:
                url = browser.url
                splitted = url.split('/')
                field_name = 'direct-link-{0}'.format(splitted[-1])
                textarea = globalvar.getElement(browser, 'id', field_name)
            else:
                textarea = globalvar.getElement(browser, 'id', 'direct-links')
    
            urls = textarea.value
    
            return urls