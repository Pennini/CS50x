# InspireVerse - Daily Motivation Phrases Website

<i>InspireVerse</i> is a web application that provides users with daily motivational phrases to inspire and uplift them. This README will guide you through setting up, using, and understanding the project.

## Getting Started

### Tools

![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-0D1117?style=for-the-badge&logo=visual-studio-code&logoColor=007ACC&labelColor=0D1117)&nbsp;
![Python](https://img.shields.io/badge/-python-0D1117?style=for-the-badge&logo=python&logoColor=1572B6&labelColor=0D1117)&nbsp;

### Installation

1. Clone the project folder to your local machine:

   <img width="83" alt="project folder" src="https://github.com/Pennini/CS50x/assets/135245057/71ae125b-d1ec-4aa3-85d3-3f020cc2e232">


3. Start a virtual environment

   ```
   > mkdir project
   > cd project
   > py -3 -m venv .venv
   >.venv\Scripts\activate
   ```

4. Install flask and flask_session

   ```
   pip install Flask
   ```

   ```
   pip install Flask_Session
   ```

5. Install pyttsx3

   ```
   pip install pyttsx3
   ```

6. Install pillow

   ```
   pip install Pillow
   ```

### Running the program

To start the application, run the following command within your virtual environment:

    ```
    python3 -m flask run
    ```

## Usage

#### Login Page

<br>

<img width="960" alt="Login Page" src="https://github.com/Pennini/Pennini/assets/135245057/37e548b5-69da-413b-86e9-366b265b02dd">

<hr>

#### Register Page

<img width="960" alt="Register Page" src="https://github.com/Pennini/Pennini/assets/135245057/88206983-d362-44cd-b56f-027e7dca19cc">

<hr>

#### Homepage

<br>

<img width="960" alt="Homepage" src="https://github.com/Pennini/Pennini/assets/135245057/4ad14191-0bc2-4fc8-8376-0ff0115bec06">

<br>
<br>

- Open the envelope to reveal a new daily motivational phrase.

<img width="960" alt="Open Envelope" src="https://github.com/Pennini/Pennini/assets/135245057/a8d55802-551c-454d-a83d-5eca05c40bbe">
    
<br>
<br>

- Click the button to listen to the phrase.

https://github.com/Pennini/Pennini/assets/135245057/43a08c8f-9f6b-44ae-b1ac-ef9ce7a47c3e

<hr>

#### Add a phrase

<br>

<img width="960" alt="Add a phrase Page" src="https://github.com/Pennini/Pennini/assets/135245057/e5b70607-5896-4bc7-bb47-78d5d3b0783d">

<br>
<br>

- Add personalized phrases for your eyes only.
- Remove phrases if you no longer want to see them.
- Search for specific phrases.

https://github.com/Pennini/Pennini/assets/135245057/b96f6af2-a92b-40ea-ae03-768df7195d5c

<hr>

#### History

<br>

- View a history of all the phrases that have appeared in your envelope.

<img width="960" alt="Captura de tela 2023-09-18 104812" src="https://github.com/Pennini/Pennini/assets/135245057/9c4e15d3-9f47-4d3b-a720-03741bdbb855">

<br>
<br>

- Search for phrases by date, text, or author.

<img width="960" alt="Captura de tela 2023-09-18 104851" src="https://github.com/Pennini/Pennini/assets/135245057/57028f54-9b53-4165-aa04-3299819baf5a">

## Database Structure

The database is divided into four tables:

<img width="434" alt="Captura de tela 2023-09-18 105305" src="https://github.com/Pennini/Pennini/assets/135245057/8c11c3a7-3801-45db-a0d4-9c7ec6290b42">

<br>
<br>

- <strong>users:</strong> Stores user information including username, email, hashed password, full name, and date of birth.

<img width="120" alt="users" src="https://github.com/Pennini/Pennini/assets/135245057/74ba2427-53a0-4d25-907a-af0784495ac4">

<br>
<br>

- <strong>phrases:</strong> Stores motivational sentences along with their respective authors.

<img width="124" alt="phrases" src="https://github.com/Pennini/Pennini/assets/135245057/ea9fcfe7-5d64-4d88-982d-3c0de649da38">

<br>
<br>

- <strong>user_phrases:</strong>Keeps track of user-added phrases. The status of a phrase changes when removed.

<img width="118" alt="user_phrases" src="https://github.com/Pennini/Pennini/assets/135245057/0db99e71-8f69-4721-bcd1-6f1eda263314">

<br>
<br>

- <strong>history:</strong>Records all phrases that appeared in the user's envelope and associates them with the respective phrase ID from either the "phrases" or "user_phrases" table.

<img width="123" alt="history" src="https://github.com/Pennini/Pennini/assets/135245057/767f7d5c-6b11-443a-a598-5170fe099957">
