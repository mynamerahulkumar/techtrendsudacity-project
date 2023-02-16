Project Overview
TechTrends is an online website used as a news sharing platform, that enables consumers to access the latest news within the cloud-native ecosystem. In addition to accessing the available articles, readers are able to create new media articles and share them with the wider community. In this project, I have packaged and deploy the application to a Kubernetes platform. Throughout this project, I  have used Docker to package the application, and automated the Continuous Integration process with GitHub Actions. For the release process, you have used Kubernetes declarative manifests, which were templated using Helm. To automated the Continuous Delivery process, I  have used ArgoCD.


<br/>
argocd - the folder that will contain the ArgoCD manifests
<br/>
helm - the folder that will contain the Helm chart files
<br/>
kubernetes - the folder that will contain Kubernetes declarative manifests
<br/>
screenshots - the folder that will contain all the screenshots that you take throughout the course
<br/>
docker_commands - the file will be used to record any used Docker commands and outputs
<br/>
Dockerfile - the file that contains the instructions to package the application
<br/>
.github - folder containing the configuration for GitHub Actions workflows