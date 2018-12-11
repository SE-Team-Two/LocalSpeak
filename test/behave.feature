Feature: User can send and recieve messages
    Scenario: Sending message
        Given we are on https://vzyrianov.pythonanywhere.com/
        And we type "Hello" in the message box
        When we click send
        Then we should see the message in the chat

    Scenario: Recieving messages
        Given we are on https://vzyrianov.pythonanywhere.com/
        And a message "Hello" has been sent by another instance 
        Then we should see "Hello" in the chat
