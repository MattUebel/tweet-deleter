## Twitter Cleanup

This is a simple script that deletes all of your tweets or unlikes all your likes.

### Prerequisites

#### Request an Archive of your Data

Go to [Twitter Settings](https://twitter.com/settings/account) and find "Download an archive of your data". Click the button and wait for the email. It may take some days.

Once you have your archive, unzip it into the `archive` folder at the root of this project.

You should end up with a file `archive/data/tweets.js` that contains all of your tweets.

#### Authentication setup

You need to have a Twitter developer account and create an app. You can do this [here](https://developer.twitter.com/en/apps).

You'll need the API key and secret, otherwise known as the `CONSUMER_KEY` and `CONSUMER_SECRET`. This is found in the "Keys and tokens" tab of your app.

Since this script deletes tweets, you'll need the app to have user-level write permissions. This enabled in the settings for the app.

When setting up the user-level authentication, you'll have a form where you define some more app properties. The questions may change, but as of writing they are:

- App Permissions - Change to "Read and write"
- Type of App - Select "Web App, Automated App or Bot"
- App Info:
    - Anything is ok for the Callback URI (e.g. "https://127.0.0.1"). 
    - The Website is any valid URL.

Once the app is updated to have Read and Write, you'll need to generate the `ACCESS_TOKEN` and `ACCESS_TOKEN_SECRET`. This is found in the "Keys and tokens" tab of your app.

You'll now have all the things setup to authenticate.

#### Prepare the .env file

Create a file called `.env` in the root of the project. This file will contain the authentication information for your Twitter app. 

an example of the file is:

```
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
```

#### Python and pipenv

This has been tested with Python 3.10

It has dependencies that are installed with pipenv:
    
```bash
pipenv install
```

### Running the script

This script takes a `--likes` or `--tweets` flag, and is intended to be run in one mode or the other.

```bash
pipenv run python3 twitter_cleanup.py --help

usage: TwitterCleanup [-h] [-t] [-l]

Delete all tweets or likes from a Twitter account given that accounts archive

options:
  -h, --help    show this help message and exit
  -t, --tweets  Delete all tweets
  -l, --likes   Delete all likes
```

This will delete one tweet or like every 20 seconds. Looping on the response from the endpoint would be an improvement, but I just took the [50 tweet limit per 15 minutes](https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/introduction) and set the loop to slightly exceed that.

Due to this low rate, the script will take a long time to run. It's advised running it in screen or tmux.

This is using the v2 API, and works differently and protentially much faster if you have access to the v1 version of the API.

