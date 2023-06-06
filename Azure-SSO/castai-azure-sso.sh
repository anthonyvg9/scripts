# Variables
appName="castai-azuresso"
redirectUri="https://login.cast.ai/login/callback"

# Create enterprise app registration
app=$(az ad app create --display-name $appName --web-redirect-uris $redirectUri --sign-in-audience AzureADMyOrg --query "{appId: appId}" -o tsv)

# Create a password (client secret) for the app
password=$(az ad app credential reset --id $app --query password -o tsv)

# Output the client ID and client secret
echo "Client ID: $app" | base64 > credentials.txt
echo "Client Secret: $password" | base64 >> credentials.txt

# Display success message
echo "Enterprise app registration created successfully. Client ID and Client Secret saved to credentials.txt file."
