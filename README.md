## About this project
This is a simple User Interface based Project to manage Client feature list and their priorities.
All features of a client are assigned some priorities and these priorities cannot go out of order.

> Types of operations covered:
* Create/delete/update Domains of features. For example domain of Cost accountancy is Accountancy.
* Create/delete/update individual clients.
* Create/delete/update multiple features for each client.
* Assign priority to each feature.
* Auto adjust priorities whenever priority of a feature is changed or a feature is deleted.

##### Demo:
http://159.65.154.104/

#### Project Requirements:
* Python 3
* MySql
* MySQL-python3
* Flask Web Framework
* flask_login
* sqlalchemy
* Knockout JS
* Jquery
> Please refer requirements.txt for more details.


#### Site Navigation:
* To create feature domain click "ProductArea" in top menu bar
* To create Clients click "home" in top menu bar
* To add Features for a client click "feature" link in home page


#### Project Layout and setup:
* A default config file "config.cfg.txt" is added with this project. rename it to config.cfg  . Flask will load configuration from this file.
* create a file filename.py (or wsgi.py) outside project directory
```
from project_dir import app
app.run(debug=True) # for production donot use debug=True
```
* To populate database
first create a database in mysql say "mydb"
then go to project directory (cd path to project directory)

  run
  ```
  python3 models.py
  ```
  After database has been populated run
  ```
  cd ../
  python3 filename.py
  ```

#### Production Setup:

##### I found below links very useful for my Setup  
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04  

 https://realpython.com/kickstarting-flask-on-ubuntu-setup-and-deployment/

 ### How to setup Flask Application In Production:
 Tested On Ubuntu 18
 * gunicorn3
 * supervisor
 * nginx

 dirname is the project(fl_feature) container  
 A sudo user is required

**install nginx server**  
```
sudo apt install nginx
sudo service nginx start
```

**Allow nginx to default port in firewall**  
```
sudo ufw enable
sudo ufw allow 'Nginx HTTP'
```

**install virtualenv**  
```
	sudo apt install virtualenv
```


**install gunicorn3**  
```
sudo apt install gunicorn3
```
**create a virtual environment**  
In home directory
```
virtualenv -p python3 <dirname>
cd <dirname>
git clone https://github.com/himdyoti/fl_feature.git
```

**install python3 packages**  

```
	pip3 install Flask
	pip3 install flask-login
	pip3 install sqlalchemy
```
I installed them Globally.  
To install them in virtualenv, first virtualenv needs to be activated.  
Then in supervisor conf file
environment=PATH=dirname_path/bin
```
  cd dirname
  source bin\activate
  pip install Flask
  pip install flask-login
  pip install sqlalchemy
```



**create a wsgi.py file in "dirname" above**  
	nano wsgi.py
```
	from fl_feature import APP

	if __name__=="__main__":
		APP.run()
```

**create a supervisor server configuration file**  

sudo nano /etc/supervisor/conf.d/flask_project.conf
```
	[program:dirname]
	command=gunicorn3 wsgi:APP -b localhost:8000
	directory=/userHomeDir/dirname
	user=your sudo user
	stderr_logfile=/var/log/supervisor/error.log
```  
**delete default nginx sites-enabled file "default"**  
```
	sudo rm /etc/nginx/sites-enabled/default
```
**create a new file flask_project. On start Nginx will read   this file when it has a symbolic link in /etc/nginx/sites-enabled/flask_project**  
	sudo nano etc/nginx/sites-available/flask_project
```
	server {
	    location / {
	        proxy_pass http://localhost:8000;
	        proxy_set_header Host $host;
	        proxy_set_header X-Real-IP $remote_addr;
	    }
	    location /static {
	        alias  /userHomeDir/dirname/fl_feature/static/;
	    }
	}
```

**create a symbolic link for this file**
```
sudo ln -s /etc/nginx/sites-available/flask_project /etc/nginx/sites-enabled/flask_project
```
```
sudo /etc/init.d/nginx restart

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start flask_project
```
