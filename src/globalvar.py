from random import uniform

from os.path import expanduser
from datetime import datetime

import time
import os
import subprocess
import re

class Globalvar():
    
    def __init__(self):
        self.home = expanduser("~")

        self.download_folder = '{0}/EntryPost/'.format(self.home)
        self.config_file = '{0}/EntryPost/config'.format(self.home) 

    def getTime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def sleep(self, start, to=0):
        if to != 0:
            sleep = uniform(start, to)
        else:
            sleep = start
    
        time.sleep(sleep)
    
    def getFilesFromFolder(self, filename):
        files = os.listdir(self.download_folder)
    
        uploadable = []
    
        for f in files:
            if filename in f:
                f = '{0}{1}'.format(self.download_folder, f)
                uploadable.append(f)
        
        return uploadable
    
    def get_active_window_title(self):
        windows = subprocess.Popen("xdotool getwindowfocus getwindowname", stdout=subprocess.PIPE, shell="FALSE")
        
        print root.communicate()[0]


    def removeAllFiles(self):
        files = os.listdir(self.download_folder)
            
        for f in files:
            if f not in ['.', '..', 'src', 'config']:
                f = f.replace(' ', '\ ')
                command = 'rm {0}{1}'.format(self.download_folder, f)
                
                os.system(command)
                
    def checkDownloadStatus(self, filename):
        files = os.listdir(self.download_folder)
        
        downloaded = 0
        
        for f in files:
            if 'rar.part' in f:
                return 0
            
            name = f.split('.')[0]
            if filename == name:
                downloaded += 1
        
        return downloaded
    
    def removeFiles(self, filename):
        files = os.listdir(self.download_folder)
            
        for f in files:
            
            name = f.split('.')[0]
            if filename == name:
                f = f.replace(' ', '\ ')
                command = 'rm {0}{1}'.format(self.download_folder, f)
                
                os.system(command)
                
    def gotoUrl(self, url, browser, times=0):
        
        browser.visit(url)
    
        error_strings = []
        
        error_strings.append('server not found')
        error_strings.append('404 error')
        error_strings.append('page not found')
        error_strings.append('maintenance')
        error_strings.append('connection has timed out')
        
        for error in error_strings:
            if browser.is_text_present(error):
                if times == 1:
                    return False
                    
                self.gotoUrl(browser, url, 1)
        
        return True

    def getElement(self, browser, by, str, time = 0, depth = 0):
        if depth == 5:
            print("Can't find element '{0}', even after searching a long time".format(str))
            
            return 0
        
        element = None
        
        if by == 'id':
            if browser.is_element_present_by_id(str, wait_time=time):
                element = browser.find_by_id(str)
                
        elif by == 'css':
            if browser.is_element_present_by_css(str, wait_time=time):
                element = browser.find_by_css(str)
                
        elif by == 'xpath':
            if browser.is_element_present_by_xpath(str, wait_time=time):
                element = browser.find_by_xpath(str)
                
        elif by == 'tag':
            if browser.is_element_present_by_tag(str, wait_time=time):
                element = browser.find_by_tag(str)
                
        elif by == 'name':
            if browser.is_element_present_by_name(str, wait_time=time):
                element = browser.find_by_name(str)
                
        elif by == 'text':
            if browser.is_element_present_by_text(str, wait_time=time):
                element = browser.find_by_text(str)
                
        elif by == 'value':
            if browser.is_element_present_by_value(str, wait_time=time):
                element = browser.find_by_value(str)
        
        if type(element).__name__ != 'ElementList': 
            element = self.getElement(browser, by, str, 5, depth+1)
        
        return element
    