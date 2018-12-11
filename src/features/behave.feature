Feature: User can use SpeakEasy application
  Scenario: Create a New Account
    Given we are at the SpeakEasy website
	When we click "Create Account"
	Then we can create a new account
	
  Scenario: Successful Login
    Given we are at the SpeakEasy website
	When we enter our username and password
	Then we can log in
	
  Scenario: Sending message
    Given we are at the SpeakEasy website
	  And we successfully logged in
    When we type Testing_Bot1 in the message box
      And we press Return
    Then we should see Testin_Bot1 in the chat
	
  Scenario: Receiving messages
    Given we are at the SpeakEasy website
	  And we successfully logged in
    When a message Testing_Bot2 from another user is sent
    Then we should see Testing_Bot2 in the chat from other user
  
  Scenario: Successful Logout
    Given we are at the SpeakEasy website
	  And we successfully logged in
	When we click logout
	Then we are logged out
	
  Scenario: Hide Chat Rooms
    Given we are at the SpeakEasy website
	  And we successfully logged in
	When we click the Hide Rooms button
	Then the Rooms In Your Area tab disappears
	
Scenario: User can create a new room
  Given we are at the SpeakEasy website
	And we successfully logged in
  When we try to create a room
  Then a room is created
