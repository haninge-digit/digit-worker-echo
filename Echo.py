import os
import asyncio
import httpx
import traceback
from datetime import datetime
from random import randint
from email.message import EmailMessage

from zeebe_worker import WorkerError


"""
Environment
"""
MOCKBIN = os.getenv('MOCKBIN',"")
IPIFY = os.getenv('IPIFY',"")
INTMAIL = os.getenv('INTMAIL',"")
USERINFOCASH = os.getenv('USERINFOCASH',"userinfocash.worker-services:8080")


class Echo(object):

    queue_name = "echo"

    def __init__(self):
        pass

    async def worker(self, vars):
        if 'TIMESTAMP' in vars:
            return {'timestamp':datetime.now().__str__()}

        if 'USERID' in vars:
            return {'loggedinuser':vars['userid'] if 'userid' in vars else ""}

        if 'USERINFO' in vars:
            userID = vars.get("userid","")
            if userID == "":
                userID = "196512123339"     # Nisse Johan Pärlemo
            async with httpx.AsyncClient(timeout=10, verify=False) as client:
                r = await client.get(f"http://{USERINFOCASH}/userinfo/{userID}")        # Get userinfo from cash system
                if r.status_code != 200:
                    return {'_DIGIT_ERROR': r.text, '_DIGIT_ERROR_STATUS_CODE': r.status_code}       # Error from userinfocash service

            userinfo = r.json()
            user = {}   # user values to return
            user['personId'] = userinfo['PersonId'].strip()
            if ',' in userinfo['GivenName']:
                user['firstName'] = userinfo['GivenName'].split(',')[1].strip()    # Get first (given) name from last part of 'GivenName'
            else:
                user['firstName'] = userinfo['GivenName'].strip()      # Just grab what is there
            user['lastName'] = userinfo['LastName'].strip()
            user['fullName'] = userinfo['FirstName'].strip()+" "+userinfo['LastName'].strip()
            user['address'] = userinfo['Address'].strip()
            user['zipcode'] = userinfo['ZipCode'].strip()
            user['city'] = userinfo['City'].strip()
            # user['country'] = userinfo['Country'].strip()       # Skip this for now
            user['municipalityCode'] = userinfo['MunicipalityCode'].strip()
            for k,v in userinfo.items():
                if k not in ['PersonId','Address','BirthPlace','City','CivilStatus','Country','FirstName','GivenName','LastName','ZipCode','MunicipalityCode','Parish','Relation']: # List of KIR data
                    user[k] = v     # Added extra data that are not from KIR

            return {'user': user}     # Return what we found

        if 'DELAY' in vars:
            delay = vars['DELAY'] if vars['DELAY'] != "" else "1"
            await asyncio.sleep(int(delay))
            return {}

        if 'RANDELAY' in vars:
            delay = vars['RANDELAY'] if vars['RANDELAY'] != "" else "10"
            await asyncio.sleep(randint(0,int(delay)))
            return {}

        if 'MOCKBIN' in vars:
            try:
                async with httpx.AsyncClient(timeout=10, verify=False) as client:
                    r = await client.get(MOCKBIN, params=vars)
                    res = r.json()
                    return res
            except Exception as e:
                raise WorkerError(f"echo worker fatal error: {traceback.format_exc()}")       # Okänt fel

        if 'IPIFY' in vars:
            try:
                async with httpx.AsyncClient(timeout=10, verify=False) as client:
                    r = await client.get(IPIFY, params={'format':'json'})
                    res = r.json()
                    return res
            except Exception as e:
                raise WorkerError(f"echo worker fatal error: {traceback.format_exc()}")       # Okänt fel

        if 'EMAIL' in vars:
            try:
                recepients = vars['EMAIL']
                msg = "Hej hopp i lingonskogen!"
                message = EmailMessage()
                message["From"] = "NoReply@haninge.se"
                message["To"] = recepients
                message["Subject"] = f"Message from Camunda process {vars['PROCESS_NAME']}"
                message.set_content(msg)
                async with httpx.AsyncClient(timeout=10, verify=False) as client:
                    r = await client.post(INTMAIL, json={'EmailMessage':message.as_string()}) 
                    return {}
            except Exception as e:
                raise WorkerError(f"echo worker fatal error: {traceback.format_exc()}")       # Okänt fel

        if 'ERROR' in vars:
            raise WorkerError(f"Simulating non fatal error ERROR", retry_in=10)       # Okänt fel


        return vars|{"PING":True}
