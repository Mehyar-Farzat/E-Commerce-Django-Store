
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User




class EmailOrUsernameLogin(ModelBackend):                         # create class for email or username login

    def authenticate(self, request, username=None, password=None, **kwargs):       # create authenticate function 
        try:                                                                      # try to get user by email or username
            user = User.objects.get(email=username)                              # get user by email 
        except User.DoesNotExist:                                               # if user does not exist
            try:                                                              # try to get user by username 
                user = User.objects.get(username=username)                     # get user by username 
            except User.DoesNotExist:                                        # if user does not exist 
                return None                                                  # return none 
        
        
        if user.check_password(password):                                   # check if password is correct        
            return user                                                    # return user if password is correct

        return None                                                        # return none if password is incorrect
                                               