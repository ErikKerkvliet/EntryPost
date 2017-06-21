import globalvar

globalvar = globalvar.Globalvar()

class Rapidgator():
    
    def __init__(self):
        pass
    
    #login on to rapidgator.net
    def login(self, browser, account):
    
        # Go to the rapidgator homepage
        url = 'https://rapidgator.net'
        browser.visit(url)
        
        # get all links on the page
        elements = globalvar.getElement(browser, 'tag', 'a')
    
        # check if an profile related link excists. If so: The logging in can be stopped
        for element in elements:
            if element['innerHTML'].strip(' ') == 'My account':
                print('Already logged in on to rapidgator.net')
                
                return
    
        # click on the login link
        globalvar.getElement(browser, 'xpath', '/html/body/div[1]/div[1]/div[2]/ul/li[1]/a').click()
        
        globalvar.sleep(4, 5)
        
        # fill the login data with the yuuichi sagara account information
        login_field = globalvar.getElement(browser, 'id', 'LoginForm_email')
        
        if login_field['value'] == '':
            login_field.fill('yuuichi.sagara@gmail.com')
        else:
            # if something already has been inserted it is probably account info from a logged in account. 
            # Meaning the logging in can be stopped
            print('already logged in')
            
            return
            
        password_field = globalvar.getElement(browser, 'id', 'LoginForm_password')
        password_field.fill('kdRwvg')
        
        # click the submit link to finalize the login
        link = globalvar.getElement(browser, 'xpath', '//*[@id="registration"]/ul/li[5]/a[1]')
        
        link.click()
        
        globalvar.sleep(4, 6)
    
        
    #download all given rapidgator urls
    def download(self, browser, urls, account):
        
        self.login(browser, account)   
    
        for url in urls:
            browser.visit(url)
            
            globalvar.sleep(4, 5)
    
            while not globalvar.getElement(browser, 'css', '.btn.btn-download'):
                browser.visit(url)
                
            globalvar.getElement(browser, 'css', '.btn.btn-download').click()
            
                
                
            globalvar.sleep(10, 20)
        