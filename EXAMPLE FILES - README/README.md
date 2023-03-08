# Example Files
Hello professor! We added an example database with some pre-filled data in case you want to check
it out. Just delete the existing db.sqlite3 file in the project directory (if it exists)
and put the one from this folder into the project root directory.

The goal of including this is to show our project at its best with pre-populated data while keeping things easier on
you.

> **NOTE:** You may need to run `python manage.py migrate` if using this database file. It might be slightly outdated.

## Credentials  
### Eventgoer (Client Site)  
**Email:** `demo@example.com`  
**Password:** `password123!`  
### Venue Manager  
> This is the venue manager that has registered the example concerts.  

**Email:** `eden.burton@senecacollege.ca`  
**Password:** `password123!`  
### Admin Site (Django Internal)  
_Use this if you want to check out how our models function in more depth._  
> **Note:** _This is not meant to be accessed by normal users._  

**Username:** `Burton`  
**Password:** `password123!`  