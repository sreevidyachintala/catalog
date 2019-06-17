# ItemCatalog Project - Electronic Devices
## By Chintala Sreevidya
This Electronic Devices is a project for the Udacity  [FSND Course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

## About Project:
This Project display the different Electronic categories with respective electronic items, Any user can view the items but only authenticated people can add an item, edit an item, delete an item. Currently OAuth2 is implemented for Google Accounts.

## In This Project
This project has one main Python module `electronic.py` which runs the Flask application. A SQL database is created using the `db_setup.py` module and you can populate the database with test data using `db_init.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application.

## Skills Required:
   1. Python
   2. Html5
   3. CSS3
   4. Flask FrameWork
   5. OAuth
   6. SQLAlchemy
  
## Resourses :
   - Vagrant 
   - Udacity Vagrantfile 
   - VirtualBox 

## How to Install :

    Step1 --> Install [Python](https://www.python.org/downloads)
    
    Step2 --> Install [Vagrant](https://www.vagrantup.com/downloads.html)
    
    Step3 --> Install [VirtualBox](https://www.virtualbox.org/wiki/downloads)
    
    Step4 --> Install [Git](https://git-scm.com/download/win) --> For Windows
    
    Step5 --> Launch the vagrant virtual machine inside vagrant sub-directory then open Git Bash: `$vagrant up`
    
    Step6 --> Login to vagrant virtual machine --> `$vagrant ssh`
    
    Step7 --> Change directory to /vagrant --> `$cd /vagrant/`
    
    Step8 -->  Change directory to project folder inside vagrant folder--> `$cd ItemCatalog`
    
    Step9 --> Install the requirement project modules are:
    
        * `sudo pip install flask`
        * `sudo pip install oauth2client`
        * `sudo pip install sqlalchemy`
        * `sudo pip install requests`
    
     Step10 --> Create application database:`$python db_setup.py`
    
     Step11 --> Inserting application data in database -->`$python db_init.py`

     Step12 --> Run the main project file -->`python electronic.py`
    
     Step13 --> Access the application any local browser[http://localhost:5000](http://localhost:5000)

 ### JSON EndPoints: 
 In this project we create json endpoints using REST architecture

 1. Display the all Categories with Items : ``http://localhost:5000/category/JSON``

 2. Display the categories: `http://localhost:5000/category/category/JSON`

 3. Display the item of given category: `http://localhost:5000/category/1/items/JSON`

 4. Display the all Items : `http://localhost:5000/category/items/JSON`


