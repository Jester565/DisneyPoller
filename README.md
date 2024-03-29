# Disney Polling Script

## Summary

This script provide a method to:
1. stay authenticated with Disney's APIs
2. continually poll Disney's endpoints
3. send a text when a certain condition is met

The script will hit Disney's login APIs at least every 30 minutes (which is how long we have to renew our refreshToken before it expires).

## Code

The [template.py](./template.py) file will provide you with a starting point for your script and [poll_park_availability.py](./poll_park_availability.py) will provide an example of a working script. You’ll want to update the template for-loop with the call you’d like to make against Disney’s API.  You can add that call to the [disney_api.py](./utils/disney_api.py) file. The call you add will likely have a very similar spec to the get_park_reservation_availability function. Calls on the Disney World website should all work with the authToken provided in the for-loop. However, Disneyland and other Disney offerings have not been tested.

Using the information from your API call, you can invoke the twilio api to send a message to the `NOTIFY_NUMBERS` in the [config](./config.py).  If your script runs into an error, the `ERROR_NOTIFY_NUMBER` will be informed so you can action it.


## Pre Requisites

There are a few things you'll need for the script to work:
* A linux server with at least python3.8 for the script
  * running 24/7
  * recommend a EC2 t2.nano ($4.75 / month)
* A twilio account's API credentials for sending texts
  1. [Setup Account](https://www.twilio.com/login)
  2. OPTIONAL: To send to any phone number (other than ones you've manually verified in the twilio console, eg. your own phone), [request your number to be verified](https://www.twilio.com/docs/messaging/compliance/toll-free/console-onboarding#start-the-verification-flow-for-existing-us-or-ca-toll-free-numbers). I just made stuff up.
  3. [Create a API Key](https://www.twilio.com/docs/iam/api-keys#create-an-api-key)
* A disney account

## Setup
1. Goto the parent directory of the repo
2. Install dependencies with
    ```pip install -r requirements.txt```
3. Update the [config.py](./config.py) with secrets and account info
    1. Set your Twilio credentials / phone number
    2. Get your Disney ID & Refresh Token (Note: After you get your refresh token, you have 30 minutes to run the script. We have to use the refresh token to kick off the script since the login API is captcha protected but the renew refresh token endpoint is not)
        1. Goto [Disney](https://disneyworld.disney.go.com/) w/ Firefox
(Chrome has trouble keeping response data)
        2. Open the network tab (F12 -> Network) and login to your account
        3. View the `POST /v8/client/TPR-WDW-LBJS.WEB-PROD/guest/login` 
response
        4. The response will have the following format. Set the refresh_token as the INIT_REFRESH_TOKEN and the swid to DIS_ID.
            ```
            {
                “token”: {
                    “refresh_token”: “ABC”,
                    “swid”: “{3B-AB-12}”
                    ...
                }
                ...
            }
            ```
        5. Run your script, if you want to keep the script running use
        ```screen -L -Logfile logs.txt -d -m python {yourscript}```
        6. View logs w/
        ```tail -n 100 -f logs.txt```
    