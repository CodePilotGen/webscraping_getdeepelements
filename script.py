from selenium import webdriver
from tkinter import *
from pynput import mouse
from pynput.mouse import Listener

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Browser window position calculation script
coordinate_script = """
            var X, Y;
            if (window.screenY)
            { 
                X = window.screenX; 
                Y = window.screenY + 124; 
            } 
            else
            { 
                var  Elem = document.documentElement;          
                if (!Elem.clientHeight) Elem = document.body;
                X = Elem.scrollLeft; 
                Y = Elem.scrollTop; 
            } 
            return new Array(X, Y);
        """

def CheckRightClick(x, y, button, pressed):
    if button == mouse.Button.right:
        if pressed:
            print('Getting element')
            driver.switch_to.default_content()
            winPos = driver.execute_script(coordinate_script)
            # actual element position in browser
            x -= winPos[0]     
            y -= winPos[1]
            # xpath = "//iframe[contains(@src,\"product=prod_7hhq9qcuyhralg\")]"
            # xpath = "//iframe[@title='Add Cards Against Humanity to cart']"
            # iframe = WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath(xpath))
            # iframe = driver.find_element_by_xpath(xpath)
            # print(iframe)
            # driver.switch_to.frame(iframe)
            driver.implicitly_wait(30)
            element = driver.execute_script("""
                    return document.elementFromPoint(arguments[0], arguments[1]);
                """, x, y)
            # element = findElement(x, y)
            deepestElement = None
            if element is None:
                print('current cursor position might be wrong')
                return
            if element is not None:
                print(" id=> ", element.get_attribute("id"), "\n tagName=> <", element.tag_name, ">", "\n text=> ", element.text, "\n\r")
            if element.tag_name == "iframe":
                # get iframe element position. it will return {top: , left:, x: , y: , width: , height}
                elementPos = driver.execute_script("""
                    var element = document.elementFromPoint(arguments[0], arguments[1]);
                    if(element !== null)
                        return element.getBoundingClientRect();
                    else 
                        return null;
                """, x, y)
                # actual element postion in the iframe.
                x -= elementPos['left']
                y -= elementPos['top']
                driver.switch_to.frame(element)
                deepestElement = driver.execute_script("""
                    return document.elementFromPoint(arguments[0], arguments[1]);
                """, x, y)
            else:
                deepestElement = element
            if deepestElement is not None:
                print("deepest element:\n id=> ", deepestElement.get_attribute("id"), "\n tagName=> <", deepestElement.tag_name, ">", "\n text=> ", deepestElement.text, "\n\r")
            print('Element at cursor is ', deepestElement, "\n\r")
            # click_window.event_generate("<<quit>>")

# At first, I thought it's driver handler problem. so, I made it. but no matter it, still didn't work in iframe.
def findElement(x, y , iframeIndex = -1):
    driver.switch_to.default_content()
    iframes = driver.find_elements_by_tag_name('iframe')
    # print(x, y, iframeIndex, len(iframes))
    if iframes is not None and iframeIndex >= len(iframes):
        return None
    if iframeIndex > -1:
        driver.switch_to.frame(iframes[iframeIndex])
    element = driver.execute_script("""
                    return document.elementFromPoint(arguments[0], arguments[1]);
                """, x, y)
    if element is not None:
        return element
    if len(iframes) == 0:
        return None
    return findElement(x, y, iframeIndex + 1)


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, executable_path=r'./chromedriver_90.exe')
# driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\Shane\Desktop\Python\chromedriver_win32'r'\chromedriver.exe')

url = 'http://store.cardsagainsthumanity.com/'
driver.get(url)

time.sleep(10)

# check iframes in this site
# iframes = driver.find_elements_by_tag_name('iframe')
# for iframe in iframes:
#     print(iframe.get_attribute("src"), iframe.tag_name)

click_window = Tk()
click_prompt = Label(click_window, text='Right click somewhere')
click_prompt.grid(row=3, column=3)
click_window.bind("<<quit>>", lambda *args: click_window.destroy())
listener = Listener(on_click=CheckRightClick)
listener.start()
click_prompt.mainloop()
listener.stop()
