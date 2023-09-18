# Final project - InspireVerse

Website that gives motivation phrases everyday for the user

## Starting

### Tools

![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-0D1117?style=for-the-badge&logo=visual-studio-code&logoColor=007ACC&labelColor=0D1117)&nbsp;

- Start a virtual environment

```
> mkdir myproject
> cd myproject
> py -3 -m venv .venv
>.venv\Scripts\activate
```


- Install flask and flask_session

```
pip install Flask
```
```
pip install Flask_Session
```

- Install pyttsx3

```
pip install pyttsx3
```

- Install pillow

```
pip install Pillow
```

- Run the program - after started a venv

```
python3 -m flask run
```

## Operation

- Login page

<img width="960" alt="Login Page" src="https://github.com/Pennini/Pennini/assets/135245057/37e548b5-69da-413b-86e9-366b265b02dd">

<hr>

- Register page

<img width="960" alt="Register Page" src="https://github.com/Pennini/Pennini/assets/135245057/88206983-d362-44cd-b56f-027e7dca19cc">

<hr>

- Homepage

<img width="960" alt="Homepage" src="https://github.com/Pennini/Pennini/assets/135245057/4ad14191-0bc2-4fc8-8376-0ff0115bec06">

    1. You can open the envelope to see a new phrase everyday

<img width="960" alt="Open Envelope" src="https://github.com/Pennini/Pennini/assets/135245057/a8d55802-551c-454d-a83d-5eca05c40bbe">
    
    2. You can click the button to listen to the phrase

https://github.com/Pennini/Pennini/assets/135245057/43a08c8f-9f6b-44ae-b1ac-ef9ce7a47c3e

<hr>

- Add a phrase

<img width="960" alt="Add a phrase Page" src="https://github.com/Pennini/Pennini/assets/135245057/e5b70607-5896-4bc7-bb47-78d5d3b0783d">

    1. You can add phrases for only you to see

    2. You can remove the phrase if you don't want anymore
    
    3. You can search for a specific phrase

https://github.com/Pennini/Pennini/assets/135245057/b96f6af2-a92b-40ea-ae03-768df7195d5c

<hr>

- History

    1. You can see all the phrases that appeared in the envelope for you

<img width="960" alt="Captura de tela 2023-09-18 104812" src="https://github.com/Pennini/Pennini/assets/135245057/9c4e15d3-9f47-4d3b-a720-03741bdbb855">


    2. You can search by date, phrase or author

<img width="960" alt="Captura de tela 2023-09-18 104851" src="https://github.com/Pennini/Pennini/assets/135245057/57028f54-9b53-4165-aa04-3299819baf5a">

## The database

I divided the database in 4 tables

<img width="434" alt="Captura de tela 2023-09-18 105305" src="https://github.com/Pennini/Pennini/assets/135245057/8c11c3a7-3801-45db-a0d4-9c7ec6290b42">

- users
    
Store all users with username, email, hashed password, full name and date of birth.

<img width="120" alt="users" src="https://github.com/Pennini/Pennini/assets/135245057/74ba2427-53a0-4d25-907a-af0784495ac4">

- phrases

Store all sentences that may appear on the envelope with the author's name.

<img width="124" alt="phrases" src="https://github.com/Pennini/Pennini/assets/135245057/ea9fcfe7-5d64-4d88-982d-3c0de649da38">

- user phrases

Store all sentences the user wants to save. If the user removes a phrase, the status of the phrase will change and it will no longer be used

<img width="118" alt="user_phrases" src="https://github.com/Pennini/Pennini/assets/135245057/0db99e71-8f69-4721-bcd1-6f1eda263314">

- history

Store all phrases that appeared in the envelope for the user and associate with the phrase id in the right table (phrases or user_phrases)

<img width="123" alt="history" src="https://github.com/Pennini/Pennini/assets/135245057/767f7d5c-6b11-443a-a598-5170fe099957">
