# global-exam-bot
A bot that does your english exercies for you.

### installation
put your credentials in `credentials.json` as described in `credentialsExample.json`. 
``pip install -U ./requirements.txt``

This bot uses chromium : make sure to have it installed, and get its version number with 
`version=$(echo $(chromium --version | grep -Eo "[0-9\.]" |tr -d '\012\015'))`. 
Next, clone this branch.
You will also need a selenium driver : while being in your cloned repository, execute :
`wget https://chromedriver.storage.googleapis.com/$version/chromedriver_linux64.zip`, then unzip with : 
`unzip chromedriver_linux64.zip`

You're all set now ! 


### run 
`python main.py`
be lazy :)
