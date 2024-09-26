# LibraryManagementSystem
--------------------------
* In this project main we have to deal with three sections
  ## frontend_image
  ## backend
    * ### books
    * ### users
## What has to do?
* In this we have to do following things
  * build docker image
  * run trivy scan for docker image
  * publish trivy scan reports  
  * push the image to docker hub
* We have two approaches for doing this 
  * Manual 
  * Write azure pipeline
## Manual
* Clone git repository into the instance

### Install docker
```sh
curl -fsSL https://get.docker.com -o install-docker.sh
docker --version
```
* Add the user to docker group through following command
```  
sudo usermod -aG docker ubuntu
exit 
```
* ![frontend_image](images/library1.png)
* Clone the repository into your machine.

### Install Trivy
* Install trivy to scan docker images
* Execute the following commands 
```sh
sudo apt-get install -y wget
wget https://github.com/aquasecurity/trivy/releases/download/v0.34.0/trivy_0.34.0_Linux-64bit.deb
sudo dpkg -i trivy_0.34.0_Linux-64bit.deb
```
* ![frontend_image](images/library2.png)

## frontend_image
* Run trivy scan for the image of frontend_image
* build image and run the trivy scan 
```sh
docker image build -t frontend_image:1.0 .
trivy image frontend_image:1.0
```
* After running trivy scan we get reports like that
* ![frontend_image](images/library3.png)
* Fix the issues by modifying Dockerfile 
  * Create the user `library` and run the application through that user
  * Run the working directory through `/library`
  * Run the Multi stage Dockerfile
* Make the necessary changes in Dockerfile as below
* ![frontend_image](images/library4.png)
* After that see the results of trivy, issues got resolved after making those changes
* ![frontend_image](images/library5.png)
* Make sure that application is running inside the container and it is accessable
![frontend_image](images/library20.png)
![frontend_image](images/library21.png)

* Do trivy scan and see there is no issues in trivy reports
![frontend_image](images/library12.jpg)
## Backend
* As mentioned earlier in backend we have two service
  * books 
  * users
### books
* First build the image for the backend books service
![frontend_image](images/library7.png)
* Run trivy scan for image 
![frontend_image](images/library8.png)
* Here two problems are there 
  * In the requirements section we have to change the version of `PyJWT` from `2.3.0 `  to `2.4.0 ` as done below
  ![frontend_image](images/library10.png)
* Now run trivy scan issue got solved
![frontend_image](images/library11.png)
* To resolve the second trivy issue make change in Dockerfile as follows
![frontend_image](images/library13.png)
* Build image for modified Dockerfile and run trivy scan 
* you get that issues get resolved through it
![frontend_image](images/library14.png)
### users
* First build the docker image and run trivy scan for image
![frontend_image](images/library15.png)
* Afer trivy scan you get errors like below
* ![frontend_image](images/library16.png)
* To solve setuptools error we have to install 70.0.0 
* Add one instruction in the Dockerfile as below
![frontend_image](images/library17.png)
* Again build the image and run trivy scan
![frontend_image](images/library18.png)
* As you see the issue with setuptool got resolved
* For the second issue possibly we don't have any fixed version to resolve the problem.
![frontend_image](images/library19.png)