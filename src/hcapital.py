import globalvar
import pyperclip

globalvar = globalvar.Globalvar()

class Hcapital():
    def __init__(self):
        pass
    
    def getFilename(self, browser, url):
        browser.visit(url)
        
        globalvar.sleep(2, 4)
        
        linkName = globalvar.getElement(browser, 'xpath', '//div[@class="in"]//a').first.text
        
        filename = linkName.split('.')[0]
    
        return filename
    
    def getRapidgatorUrls(self, browser, entry):
        url = "http://hcapital.tk/?show=edit&id={0}".format(entry)
        browser.visit(url)
        rapidUrls = []
    
        rapidValue = globalvar.getElement(browser, 'id', 'rapidlinks').value
        
        urls = rapidValue.split('\n')
    
        for url in urls:
            if len(rapidUrls) == 0:
                rapidUrls.append([])
                
            if url == '':
                continue
            
            rapidUrls[0].append(url)
    
    
        for i in range(1, 9):
            fieldId = 'other{0}links'.format(i)
    
            textfield = globalvar.getElement(browser, 'id', fieldId)
            textfieldValue = textfield.value
    
            urls = textfieldValue.split('\n')
            
            if len(urls) > 0 and urls[0] != '':
                rapidUrls.append([])
    
            for url in urls:
                if url == '-' or url == '':
                    break
    
                rapidUrls[i].append(url)     
        
        return rapidUrls
    
    def getImagesHcapital(self, browser):
        
        imgUrls = []
        elements = browser.find_by_xpath('//div[@id="single_image_rows"]//img[@id="img"]')
        
        for element in elements:
            imgUrls.append(element['src'])
            
        cover = globalvar.getElement(browser, 'xpath', '//img[@id="cover"]').first
        
        imgUrls.append(cover['src'])
        
        return imgUrls
    
    def editEntryAndGetPost(self, browser, entry, entryType, images, bigfileUrls, rapidUrls):
    
        url = "http://hcapital.tk/?show=edit&id={0}&type={1}".format(entry, entryType)
        browser.visit(url)
        
        globalvar.sleep(2, 4)
        
        bigfileUrlsText = '\n'.join(bigfileUrls[0])
        
        globalvar.getElement(browser, 'id', 'biglinks').first.fill(bigfileUrlsText)
        
        if len(rapidUrls) > 1:
            browser.check('other')
            
            globalvar.sleep(2, 4)
    
            for i in range(1, len(rapidUrls)):
                rapidUrlText = '\n'.join(rapidUrls[i])
                bigfileUrlsText = '\n'.join(bigfileUrls[i])
                text = rapidUrlText + '\n-\n' + bigfileUrlsText
        
                textfieldId = 'other{0}links'.format(i)
                
                globalvar.getElement(browser, 'id', textfieldId).first.fill(text)
            
        globalvar.getElement(browser, 'name', 'sharing').first.fill(images)
    
        globalvar.getElement(browser, 'id', 'submit').first.click()
    
        globalvar.sleep(2, 4)
    
        clipHolder = pyperclip.paste()
        globalvar.getElement(browser, 'id', 'copy_button').first.click()
        
        post = pyperclip.paste()
        pyperclip.copy(clipHolder)
    
        globalvar.sleep(2, 4)
        
        post = post.replace('&nbsp;', ' ')
        
        return post


