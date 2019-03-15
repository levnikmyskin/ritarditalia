# Ritarditalia
A telegram bot written in Python to keep track of Trenitalia delays.  
The bot is available at http://t.me/ritarditalia_bot  

## Running
The recommended way of running this bot is by using the [docker-compose.yml](https://docs.docker.com/compose/overview/)
file in the root of the repository: you'll need to first build the image provided in the Dockerfile. You can set your
database name, user and password in the `environment` section of the docker-compose file 
The bot requires several files which are not versioned because they contain passwords or the like. To run your own
instance you'll need to have the following files:
  * `bot_token.json` in the root of the repository with format `{"token": "yourtoken"}`  
  * `config.py` in the root of the repository, you can read an example in the example_config.py  

Once you have all of this, you can run the `bootstraping.py` script which will import the train stations from the
`stazioni.tsv` file to the database. You're now ready to run the bot, even though probably you missed your train
in the meanwhile.  
  
## Running tests
As you may have noticed, some tests are provided, however they're pretty much empty for the moment :(

## Known issues
At the moment, the biggest issue is that the bot works with Trenitalia assigned train codes:  
these train codes are, surprisingly enough, not unique; if this happens the bot will not manage it 
correctly and will probably either send an error to the user or do nothing

## Connecting to Gmail
The Python program can also connect to Gmail and start listening for mails coming from Trenitalia:
it will then parse the email (it's a really dummy parse at the moment :D) and store the information 
in the database, same as if you added that train from the bot.  
For this to work, you need a `credentials.json` file in the root of the repository, used to connect 
with the [Gmail API](https://developers.google.com/gmail/api/). Check the link if you don't know how to obtain
the API keys, authorization and so on.  
You can then set a cronjob or similar to run the `gmail/gmail.py` file at desired intervals.  
This was not added as a bot feature due to privacy concerns mostly: even though the code does not do anything similar,
giving the bot complete access to your Gmail inbox will allow it to read all of your emails.

## Desiderata
One cool feature which could really be added now is a way of searching for trains. 
The main issue is managing to offer the user a reasonably simple interface
to search for trains, but I couldn't come up with any idea :/

## Contributing
This project was basically born because I needed a simple way to keep track of trains delays several hours before my 
departure, but I would gladly appreciate any contribution. Just fork the repo and make a pull request on a new branch 
when you're ready.  

## Credits
This bot was possible thanks to the amazing work done on the Trenitalia API documentation by https://github.com/SimoDax/Trenitalia-API/wiki/API-Trenitalia---lefrecce.it and https://github.com/sabas/trenitalia
