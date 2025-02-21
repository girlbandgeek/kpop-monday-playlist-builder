# foo
from mastodon import Mastodon

# Register your app! This only needs to be done once (per server, or when
# distributing rather than hosting an application, most likely per device and server).
# Uncomment the code and substitute in your information:

Mastodon.create_app(
    'pytooterapp',
     api_base_url = 'https://mstdn.social',
     to_file = 'pytooter_clientcred.secret'
)


# Then, log in. This can be done every time your application starts, or you can use the persisted information:
mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
print(mastodon.auth_request_url())

# open the URL in the browser and paste the code you get
mastodon.log_in(
    code=input("Enter the OAuth authorization code: "),
    to_file="pytooter_usercred.secret"
)

# To post, create an actual API instance:
mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
mastodon.toot('Tooting from Python using #mastodonpy !')
