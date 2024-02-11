# RAG_Hacktogether

reference: https://towardsdatascience.com/beginner-guide-to-streamlit-deployment-on-azure-f6618eee1ba9

# login commands  
az login
Resource group: hackapp-rg
az acr login -n hackappregistry

# Push to the registry 
docker build -t hackapp_demo:v1 .
docker tag hackapp_demo:v1 hackappregistry.azurecr.io/hackapp_demo:v1
docker push hackappregistry.azurecr.io/hackapp_demo:v1

# deploy application
az container create --resource-group hackapp-rg --name hackapp -f deployment.yml
az container restart --resource-group hackapp-rg --name hackapp


hackapp.eastus.azurecontainer.io