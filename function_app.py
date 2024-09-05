import azure.functions as func
import logging
import msal
import os

# The user account to authenticate on behalf of
username = 'coch.pbi@nhs.net'
password = 'hvo6-b9zd-jk75-pcvdc241'

# Scopes needed for Power BI API
scope = ["https://analysis.windows.net/powerbi/api/.default"]

# Azure AD application information
client_id = 'e1cfb4ec-2c21-400c-a001-76f1ba480189'
client_secret = os.getenv('CLIENT_SECRET')
authority_url = 'https://login.microsoftonline.com/37c354b2-85b0-47f5-b222-07b48d774ee3'

# Function definition
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="GetAccessToken")
def GetAccessToken(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing Power BI access token request.')

    # Create a confidential client app (with client secret)
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_credential=client_secret
    )

    # Acquire token using the username and password (Resource Owner Password Credentials flow)
    result = app.acquire_token_by_username_password(
        username=username,
        password=password,
        scopes=scope
    )

    if "access_token" in result:
        access_token = result['access_token']
        logging.info("Access token acquired successfully")
        return func.HttpResponse(f"Access token: {access_token}", status_code=200)
    else:
        logging.error("Failed to acquire access token")
        return func.HttpResponse(f"Error: {result}", status_code=500)
