from fastapi import HTTPException

invalidJson = HTTPException(status_code=400, detail="Invalid JSON - No valid json provided.")

noSubmissions = HTTPException(status_code=400,detail="No Submissions and no feedback found -"
                                                     "Provide an array \"submissions\" or  \"feedback\" with {id.., text: ..}")
typeError = HTTPException(status_code=400,detail="TypeError: Could not deserialize to_segment -"
                                                 " Provide array to_segment with {\"id\": ..., \"text\": ...}")
keyError = HTTPException(status_code=400,detail="KeyError: Could not deserialize to_segment -"
                                                "Provide array to_segment with {\"id\": ..., \"text\": ...}")
invalidAuthorization = HTTPException(status_code=401, detail="Invalid Authorization Header")

missingCallbackUrl = HTTPException(status_code=400, detail="callbackUrl missing")

missingSubmission = HTTPException(status_code=400, detail="Submissions missing")

missingSampleSolution = HTTPException(status_code=400, detail="Sample Solution missing")
