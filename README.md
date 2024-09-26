# LibraryManagementSystem
--------------------------
* In this project main we have to deal with three sections
  ## frontend
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
* ![alt text](images/library1.png)
* Clone the repository into your machine.

### Install Trivy
* Install trivy to scan docker images
* Execute the following commands 
```sh
sudo apt-get install -y wget
wget https://github.com/aquasecurity/trivy/releases/download/v0.34.0/trivy_0.34.0_Linux-64bit.deb
sudo dpkg -i trivy_0.34.0_Linux-64bit.deb
```
* ![alt text](images/library2.png)

## Frontend
* Run trivy scan for the image of frontend
* build image and run the trivy scan 
```sh
docker image build -t frontend:1.0 .
trivy image frontend:1.0
```
* After running trivy scan we get reports like that
* ![alt text](images/library3.png)
* Fix the issues by modifying Dockerfile 
  * Create the user `library` and run the application through that user
  * Run the working directory through `/library`
  * Run the Multi stage Dockerfile
* Make the necessary changes in Dockerfile as below
* ![alt text](images/library4.png)
* After that see the results of trivy, issues got resolved after making those changes
* ![alt text](images/library5.png)
* Files are get copied into the container checkit with interactive mode
![alt text](images/library6.png)
* Do trivy scan and see there is no issues in trivy reports
![alt text](images/library12.jpg)
## Backend
* As mentioned earlier in backend we have two service
  * books 
  * users
### books
* First build the image for the backend books service
![alt text](images/library7.png)
* Run trivy scan for image 
![alt text](images/library8.png)
* Here two problems are there 
  * In the requirements section we have to change the version of `PyJWT` from `2.3.0 `  to `2.4.0 ` as done below
  ![alt text](images/library10.png)
* Now run trivy scan issue got solved
![alt text](images/library11.png)
* To resolve the second trivy issue make change in Dockerfile as follows
![alt text](images/library13.png)
* Build image for modified Dockerfile and run trivy scan 
* you get that issues get resolved through it
![alt text](images/library14.png)
### users
* First build the docker image and run trivy scan for image
![alt text](images/library15.png)
* Afer trivy scan you get errors like below
* ![alt text](images/library16.png)
* To solve setuptools error we have to install 70.0.0 
* Add one instruction in the Dockerfile as below
![alt text](images/library17.png)
* Again build the image and run trivy scan
![alt text](images/library18.png)
* As you see the issue with setuptool got resolved
* For the second issue possibly we don't have any fixed version to resolve the problem.
![alt text](images/library19.png)