import sys
import time
sys.path.append('../scr') #changes based on location of files
from behave import *
from app import *
from selenuim.webdriver.common.keys import Keys

@given(u'we are at altoc.pythonaywhere.com')#need the site name
def step_impl(context):
    browser = webdriver.Chrome()
    context.browser = browser
    browser.get("altoc.pythonaywhere.com") #need the site name
    time.sleep(5)
    assert "altoc.pythonaywhere.com" in browser.title #need the site name
	
@given(u'we are at altoc.pythonanywhere.com')#need the site name
def step_impl(context):
    browser1 = webdriver.Chrome()
    context.browser = browser1
    browser1.get("altoc.pythonanywhere.com") #need the site name
    time.sleep(5)
    assert "SpeakEasy" in browser1.title #need the site name


@when(u'we type a "{message}"')
def step_impl(context, message):
    browser = context.browser
    textbox = browser.find_element_by_name("chat_text")
    textbox.clear()
    textbox.send_keys(message)
    textbox.send_keys(Keys.RETURN)
    time.sleep(5)
    assert "altoc.pythonaywhere.com" in browser.title #need the site name

@when(u'we click send')
def step_impl(context):
    browser = context.browser
    sendbutton = browser.find_element_by_name("chat_btn") #not sure if right
    sendbutton.click()
    time.sleep(5)
    assert "altoc.pythonaywhere.com" in browser.title #need the site name
	
@when(u'a "{message}" is sent from another instance')
def step_impl(context, message):
    #opening another instance of Speakeasy
    browser2 = webdriver.Chrome()
    context.browser = browser2
    browser2.get("altoc.pythonaywhere.com")
    time.sleep(5)
    assert "SpeakEasy" in browser2.title
    #sending message from second instance
    textbox = browser2.find_element_by_name("chat_text")
    textbox.clear()
    textbox.send_keys(message)
    textbox.send_keys(Keys.RETURN)
    time.sleep(5)
    assert "SpeakEasy" in browser.title #need the site name
    sendbutton = browser2.find_element_by_name("chat_btn") #not sure if right
    sendbutton.click()
    time.sleep(5)
    assert "SpeakEasy" in browser.title

@then(u'we should see the "{message}" in the chat')
def step_impl(context, message):
    browser = context.browser
    assert message in browser.pagesource("msg_list") #need the name of messagebox not sure if .pagesource is what is needed
    time.sleep(5)
    browser.close()

@then(u'we should see the "{message}" in the chat')
def step_impl(context, message):
    browser1 = context.browser
    assert message in browser.page_source("msg_list") #need the name of messagebox not sure if .pagesource is what is needed
    time.sleep(5)
    browser1.close()
    browser2.close()

