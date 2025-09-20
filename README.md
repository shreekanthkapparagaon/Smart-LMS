# Smart-LMS
## steps to run the project
> clone the repo or download zip an unzip it

> move to project directory

> open terminal in the project directory 

>follow the commands
> ```command
>  add the following to the core/.env file 
> ```
> * ```env 
>   SECRET_KEY=your secreate key
>   DEBUG=True
>   DATABASE_NAME=database_name
>   DATABASE_USER=database_user
>   DATABASE_PASSWORD=database_password
>   DATABASE_HOST=database_host
>   DATABASE_PORT=database_port // normally 5432
> ```
> 
> * `python -m venv env`
> 
> 
> * for linux terminal `source env/bin/activate`
> 
> 
> * for windows terminal `env\Scripts\activate`
> 
> 
> * `pip install -r requirements.txt`
> 
> 
> * `python manage.py migrate`
> 
> 
> * to create a super user ``python manage.py createsuperuser``

> ## Now run ther server
>  ### To run the project
> ```commandline
> python manage.py runserver

### Go to ther url normally it will be run on 8000 port

go to ```http://127.0.0.1:8000```

# Thank you