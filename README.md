# django-hipersimple-faceauth
A super direct facebook authentication code. Not integration with default Django's auth systems, it's just a straitforward way to provide authentication.

You should inherit this base class and provide 2 methods:

* process_error, a view wich handles any error in authentication process
* process_success, the view receiving all user data fetched and should continue the proccess, now eith user authenticated
