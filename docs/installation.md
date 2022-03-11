# Spacetag app installation
> A general guide for example, on a Fedora server

```bash
uname -or
5.11.20-300.fc34.x86_64 GNU/Linux
```


## Pre-requisites

* Procure a MongoDB service with
  * login
  * password
  * path to the database
  * SSL certificate

* NodeJS
* Git
* Python 

## Download the application 

* From the default **develop** branch

  This branch may contain the latest breaking changes
  and hopefully fixes to the previous breaking changes.

  ```bash
  git clone https://github.com/NorthDecoder/nasaMining.git
  ```

* From the **stable** branch

  This branch will most often be several commits behind
  the develop branch.  Tagged commits will be made to
  this branch.

  ```bash
  git clone --branch stable https://github.com/NorthDecoder/nasaMining.git
  ```

* From a specifically tagged commit

  Replace the version x.y.z below with the version you
  are interested in cloning.

  ```bash
  git clone --depth 1 --branch x.y.z https://github.com/NorthDecoder/nasaMining.git
  ```

## Update project python modules

```bash
cd /nasaMining
pip install -r requirements.txt
```


## Update the project node modules

```bash
cd nasaMining/frontEnd
npm update
```

## Add environment variables file

A `.env` file is expected to be created (by you) in
the directory `nasaMining/frontEnd/` containing
something like the following, with your MongoDB
credentials, not the placeholders shown.


```bash
# filename: .env
ADMIN_NAME="your-mongo-administrator-name"

ADMIN_PASSWORD="your-super-long-secret-MongoDB-password"

SERVER_MONGO="dbaas889.hyperp-dbaas.cloud.ibm.com:29083,dbaas890.hyperp-dbaas.cloud.ibm.com:29502,dbaas891.hyperp-dbaas.cloud.ibm.com:29338"

# the name of the MongoDB SSL certificate file to be
# placed in the nasaMining/frontEnd/secrets/ directory
FILENAME_SSLCA="rootCA.pem"

# port number and address for the web page server
PORT="3000"
SERVER_ADDRESS="0.0.0.0"
```

## Add certificate file
```bash
cd nasaMining/frontEnd/secrets
vim rootCA.pem
# paste the MongoDB certificate authority
# credential into this file
# save and close
:wq
```

## Open a port in the firewall for http access
```bash
sudo firewall-cmd --add-port=3000/tcp --permanent
sudo firewall-cmd --add-service=http --permanent
sudo systemctl restart firewalld
sudo firewall-cmd --list-services
```

## Run the Express web page server 

```bash
cd nasaMining/frontEnd/
node server.js
```

## View the web page in your browser at

```
put.your.servername.here:3000
# or
put.your.serverIP.here:3000
```

## Close the firewall 

> When done with development tests and
> server is no longer needed

```bash
sudo firewall-cmd --remove-port=3000/tcp --permanent
sudo firewall-cmd --remove-service=http --permanent
systemctl restart firewalld
```

## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
## Mongo Work

> Get data from NASA then load the data into a Mongo database

### Initialization

```bash
# only once
pip install pymongo[tls]  # secure connector for MongoDB
pip install python-dotenv # access the .env file

# if you want to update to the latest NASA data then,
cd ~/nasaMining/data
wget -O nasa.json "https://data.nasa.gov/data.json"
```
## Add environment variables file

A `.env` file is expected to be created (by you) in
the directory `nasaMining/mongoWork/` containing
something like the following, with your MongoDB
credentials, not the placeholders shown.
> This is the same information that is in the .env
> file placed in the frontEnd directory. For now
> they are duplicated. It would be nice for me to
> to figure out how to get the front end code
> to access a .env file that is up one directory
> level.  That way there could be just one .env
> file.


```bash
# filename: .env
ADMIN_NAME="your-mongo-administrator-name"

ADMIN_PASSWORD="your-super-long-secret-MongoDB-password"

SERVER_MONGO="dbaas889.hyperp-dbaas.cloud.ibm.com:29083,dbaas890.hyperp-dbaas.cloud.ibm.com:29502,dbaas891.hyperp-dbaas.cloud.ibm.com:29338"

# the name of the MongoDB SSL certificate file to be
# placed in the nasaMining/mongoWork/secrets/ directory
FILENAME_SSLCA="rootCA.pem"
```

## FILENAME_SSLCA needs to be updated with the current SSL certificate

> the filename just defined in the .env file needs to have the
> actual cert uploaded into the secrets directory

* Download the certificate from your MongoDB admin panel, or wherever the cert
  is stored on your MongoDB server to a temporary local location.

* With [sftp](https://www.ssh.com/academy/ssh/sftp) upload the recently downloaded
  cert to the application server.  Something like the commands shown below.


```bash
cd /my_temp_local_directory
# just to make sure cert has been downloaded to the above directory
ls
cert.pem

sftp myusername@ip-of-app-server
cd nasaMining/mongoWork/secrets/

#put localfilenme remotefilename
put cert.pem rootCA.pem

exit

```



```bash
# build the database
#
cd ~/nasaMining/mongoWork
python3 buildDB.py
```


## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
## Notes

* It is not clear why there is Flask folder in the frontEnd/
  directory.  Combining a Python app and 
  a NodeJS app in the same project is confusing.
  TODO: Consider what is to become of that.

## Reference

* [enable-and-disable-firewalld](https://firewalld.org/documentation/howto/enable-and-disable-firewalld.html)
