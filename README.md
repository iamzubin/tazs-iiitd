
Face recognition and blockchain wallet for Public Transport
===


## Table of Contents

[TOC]

## Project Descreption

The idea is to use face recognition and blockchain (especially matic) to have an automated payment systems for public transports. Imagine Tag based tollways for humans without the need for any hardware / physical cards. You can simply walk in, we'll scan the face and deduct the costs from your eth blockchain wallet.


## Libraries Used

### facial recognition
1. Dlib face recognition module
2. openCV
3. Flask server

### Blockchain
1. Web3.js
2. maticJS
3. NodeJS server


User story
---
```gherkin=
Feature: Facial Recognition

  # The first example has two steps
  Scenario: User enters into X metro station
    Then the facial recognition platform looks for the user in database.
    Then An api is called for the transection of blockchain contract to init
    

  # The second example has three steps
  Scenario: User Exits from Y metro station
    Then The facial recognition looks for the user in database
    Then it calculates the fare for the distance travelled 
    Then An api is called for the deduction of fare from the smart contract
```

######  `hackiiitD`

