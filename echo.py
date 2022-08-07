import os
import asyncio
import httpx
import traceback
from datetime import datetime
from random import randint
from email.message import EmailMessage

from worker import WorkerError

MOCKBIN = os.getenv('MOCKBIN',"")
IPIFY = os.getenv('IPIFY',"")
INTMAIL = os.getenv('INTMAIL',"")

async def echo(vars):
    if 'TIMESTAMP' in vars:
        return {'timestamp':datetime.now().__str__()}

    if 'USERID' in vars:
        return {'loggedinuser':vars['userid'] if 'userid' in vars else ""}

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
