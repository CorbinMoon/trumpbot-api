# trumpbot-api

[![Build Status](https://travis-ci.org/CorbinMoon/trumpbot-api.svg?branch=master)](https://travis-ci.org/CorbinMoon/trumpbot-api)

A simple Trump chatbot Api built using TensorFlow, Keras, textgenrnn, Flask-RESTX, SQLAlchemy and Authlib.
This Api includes the following:
- Multi-class text classification model
- Text generation models (with direct correspondence to labels from classification model)
- OAuth2 implementation with password and authorization code grant types

The flow diagram below visually illustrates the basic architecture of this Api:
![alt text](api-flow-diagram.png)

##### TODOs:
- fix custom error handler
- add unit/integration tests
- add automated deployment of docker container to hosting site

### Installation

```shell script
$ docker pull corbinmoon/trumpbot-api
$ docker run -p 5000:5000 corbinmoon/trumpbot-api
```

### Examples

The application making requests to this Api first must be registered and given a `client_id` and `client_secret`.
This can be done be doing the following:
```shell script
$ curl -X POST --data '{"client_name":"app name","grant_types":["password"],"response_types":["code"],"scope":"profile","token_endpoint_auth_method":"client_secret_basic"}' \
    http://localhost:5000/clients -i -v
```
The response will be the `client_id`, `client_secret` and the date issued:
```json
{
    "client_id": "2EGSheZ0LJ8Sc4mUYwYvpkwU",
    "client_secret": "R1sOF5zvwhhEpFRPMdJGGerMM7y14hKZ8EXKlcHL7wJ0eqga",
    "issued_at": 1590964258
}
```
End users can then create an account:
```shell script
$ curl -X POST -F username=some-username -F email=some@email.com -F password=some=password http://localhost:5000/register -i -v
```
Once the end user has created an account, they will need an access token. `client_id` and `client_secret` should be provided by the application as a base64 encoded header:
```shell script
$ curl -X POST -F username=some-username -F password=some-password -F grant_type=password -F scope=profile \
    -H "Authorization: Basic MkVHU2hlWjBMSjhTYzRtVVl3WXZwa3dVOlIxc09GNXp2d2hoRXBGUlBNZEpHR2VyTU03eTE0aEtaOEVYS2xjSEw3d0owZXFnYQ==" \
    http://localhost:5000/oauth2/token -i -v
```
An access token of type `Bearer` will then be issued to the end user:
```json
{
    "access_token": "hq0tBc8I9cGXFZD1fz1FxxaDFZwCqI0WTiOMuVqnEw",
    "expires_in": 864000,
    "scope": "profile",
    "token_type": "Bearer"
}
```
The user now can use this token to access protected resources by putting the token in the authorization header. To send a message to the trump chatbot, do the following:
```shell script
$ curl -X POST -H "Authorization: Bearer hq0tBc8I9cGXFZD1fz1FxxaDFZwCqI0WTiOMuVqnEw" \
    --data '{"sender": "some-username", "text": "hey trump!"}' \
    http://localhost:5000/chat -i -v
```
The Trumpbot Api will then send a response message:
```json
{
    "sender": "Trump Bot",
    "text": "It’s amazing that people can say such bad things about me but if I say bad things about them, it becomes a national incident.",
    "timestamp": "Sun, 31 May 2020 22:50:31 GMT"
}
```
