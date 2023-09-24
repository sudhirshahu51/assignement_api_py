from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# Replace 'your_username' with the superuser's username
user = User.objects.get(username='sudhir51')
token, created = Token.objects.get_or_create(user=user)
print(f'Token for {user.username}: {token.key}')
