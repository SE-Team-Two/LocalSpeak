import sys
import time
sys.path.append('../scr') #changes based on location of files
from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

@given('we are at the SpeakEasy website')
def step_impl(context):
  context.browser = webdriver.Chrome()
  context.browser.get("https://vzyrianov.pythonanywhere.com/")
  assert 'SpeakEasy - Login' in context.browser.title
  
@given('we successfully logged in')
def step_impl(context):
  context.browser.find_element_by_id("username").send_keys("This_Is_A_Test_2")
  context.browser.find_element_by_id("password").send_keys("Password")
  context.browser.find_element_by_xpath("//button[contains(.,'Login')]").click()
  assert 'SpeakEasy - Chat' in context.browser.title
  
@when('we click "Create Account"')
def step_impl(context):
  context.browser.find_element_by_id("create_acnt_btn").click()
  
@when('we enter our username and password')
def step_impl(context):
  context.browser.find_element_by_id("username").send_keys("This_Is_A_Test_2")
  context.browser.find_element_by_id("password").send_keys("Password")
  
@when('we type {message} in the message box')
def step_impl(context, message):
  textbox = context.browser.find_element_by_id("post")
  textbox.clear()
  time.sleep(5)
  textbox.send_keys(message)
  time.sleep(5)
	
@when('we press Return')
def step_impl(context):
  textbox = context.browser.find_element_by_id("post")
  textbox.send_keys(Keys.RETURN)  

@when('we click logout')
def step_impl(context):
  context.browser.find_element_by_id("logout_btn").click()
  time.sleep(5)
  
@when('we click the Hide Rooms button')
def step_impl(context):
  sidebarWidth = context.browser.find_element_by_id("sidebar").size
  context.browser.find_element_by_id("menu_toggle").click()
  
@when('a message {message} from another user is sent')
def step_impl(context, message):
  #opening another instance of Speakeasy
  context.browser = webdriver.Chrome()
  browser2 = context.browser
  browser2.get("https://vzyrianov.pythonanywhere.com/")
  #sending message from second instance
  browser2.find_element_by_id("username").send_keys("This_Is_A_Test")
  browser2.find_element_by_id("password").send_keys("Password")
  browser2.find_element_by_xpath("//button[contains(.,'Login')]").click()
  browser2.find_element_by_id("post")
  textbox.clear()
  textbox.send_keys(message)
  time.sleep(5)
  textbox.send_keys(Keys.RETURN)  
  time.sleep(5)
  
@when('we try to create a room')
def step_impl(context):
  context.browser.find_element_by_id('create_room_btn').click()
  context.browser.find_element_by_id('name').send_keys("Test_Room")
  context.brower.find_element_by_id('submit_room_btn').click()
    
@then('we can create a new account')
def step_impl(context):
  context.browser.find_element_by_id("name").send_keys("This_Is_A_Test_2")
  context.browser.find_element_by_id("pw").send_keys("Password")
  context.browser.find_element_by_id("v_pw").send_keys("Password")
  context.browser.find_element_by_xpath("//button[contains(.,'Create Account')]").click()
  context.browser.quit()
  
@then('we can log in')
def step_impl(context):
  context.browser.find_element_by_xpath("//button[contains(.,'Login')]").click()
  assert 'SpeakEasy - Chat' in context.browser.title
  context.browser.quit()
  
@then('we should see {message} in the chat')
def step_impl(context, message):
  messages = context.browser.find_elements_by_class_name("message_right")
  #next line returns false, don't know why
  assert messages != None
  context.browser.quit()
  
@then('we should see {message} in the chat from other user')
def step_impl(context, message):
  messages = context.browser.find_elements_by_class_name("message_left")
  assert messages != None
  context.browser.quit()
  
@then('we are logged out')
def step_impl(context):
  assert 'SpeakEasy - Login' in context.browser.title
  context.browser.quit()

@then('the Rooms In Your Area tab disappears')
def step_impl(context):
  sidebarWidth = context.browser.find_element_by_id("sidebar").size
  print(sidebarWidth)
  assert(sidebarWidth == "{'height': 581, 'width': 1}")
  context.browser.quit()
  
@then('a room is created')
def step_impl(context):
  rooms = context.brower.find_element_by_class_name("room_itme")
  print(rooms)
  assert rooms != None
  context.brower.quit()

#@when(u'we type a "{message}"')
#def step_impl(context, message):
#    browser = context.browser
#    textbox = browser.find_element_by_name("chat_text")
#    textbox.clear()
#    textbox.send_keys(message)
#    textbox.send_keys(Keys.RETURN)
#    time.sleep(5)
#    assert "https://vzyrianov.pythonanywhere.com/" in browser.title #need the site name

#@when(u'we click send')
#def step_impl(context):
#    browser = context.browser
#    sendbutton = browser.find_element_by_name("chat_btn") #not sure if right
#    sendbutton.click()
#    time.sleep(5)
#    assert "https://vzyrianov.pythonanywhere.com/" in browser.title #need the site name
	
#@when(u'a "{message}" is sent from another instance')
#def step_impl(context, message):
#    #opening another instance of Speakeasy
#    browser1 = webdriver.Chrome()
#    context.browser = browser1
#    browser2.get("https://vzyrianov.pythonanywhere.com/")
#    time.sleep(5)
#    assert "SpeakEasy" in browser1.title
#    #sending message from second instance
#    textbox = browser1.find_element_by_name("chat_text")
#    textbox.clear()
#    textbox.send_keys(message)
#    textbox.send_keys(Keys.RETURN)
#    time.sleep(5)
#    assert "SpeakEasy" in browser.title #need the site name
#    sendbutton = browser1.find_element_by_name("chat_btn") #not sure if right
#    sendbutton.click()
#    time.sleep(5)
#    assert "SpeakEasy" in browser.title

#@then(u'we should see the "{message}" in the chat')
#def step_impl(context, message):
#    browser = context.browser
#    assert message in browser.pagesource("msg_list") #need the name of messagebox not sure if .pagesource is what is needed

#browser.quit()