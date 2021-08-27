import json
import logging
import os
import sys

import requests
from fastapi import FastAPI, Request, Response, status

from ProcessingResource import ProcessingResource
from errors import invalidAuthorization, invalidJson, missingCallbackUrl, missingSampleSolution, missingSubmission

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()



def checkAuthorization(request: Request):
    auth_secret = str(os.environ['AUTHORIZATION_SECRET']) if "AUTHORIZATION_SECRET" in os.environ else ""
    if auth_secret == "":
        logger.warning("No Authorization secret set")
        return

    if request.headers.get("Authorization") != auth_secret:
        logger.error("Host {} placed a request with an invalid secret: {}".format(request.client.host,
                                                                                  request.headers.get("Authorization")))
        raise invalidAuthorization


async def parseJson(request: Request):
    try:
        return await request.json()
    except Exception as e:
        logger.error("Exception while parsing json: {}".format(str(e)))
        raise invalidJson



# Endpoint for Artemis to submit a job
@app.post("/submit")
async def submit_job(request: Request, response: Response):
    checkAuthorization(request)

    job_request = await parseJson(request)

    # Error handling
    if "exerciseId" in job_request:
        exercise_id = job_request["exerciseId"]
    else:
        exercise_id = -1

    if "callbackUrl" not in job_request:
        raise missingCallbackUrl

    if "submission" not in job_request:
        raise missingSubmission

    if "sampleSolutionModel" not in job_request:
        raise missingSampleSolution

    processor = ProcessingResource()
    result = processor.processTask(await request.json())

    final_result = json.dumps(result)

    try:
        auth_secret = str(os.environ['AUTHORIZATION_SECRET']) if "AUTHORIZATION_SECRET" in os.environ else ""
        headers = {
            "Authorization": auth_secret,
            "Content-type": "application/json"
        }
        response = requests.post(job_request["callbackUrl"], data=final_result, headers=headers, timeout=600)
        if response.status_code == status.HTTP_200_OK:
            logger.info("Callback successful")
        else:
            logger.error("Callback failed. Status Code {}: {}".format(str(response.status_code), str(response.content)))
    except Exception as e:
        logger.error("Exception while sending back results: {}".format(str(e)))



@app.get("/test")
async def test():
    print("Tst")