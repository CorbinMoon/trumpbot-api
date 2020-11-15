# trumpbot-api

[![Build Status](https://travis-ci.org/CorbinMoon/trumpbot-api.svg?branch=master)](https://travis-ci.org/CorbinMoon/trumpbot-api)

A simple Trump chatbot Api built using TensorFlow, Keras, textgenrnn, Flask-RESTX, SQLAlchemy and Authlib.
This Api includes the following:
- Multi-class text classification model
- Text generation models (with direct correspondence to labels from classification model)
- OAuth2 implementation with password and authorization code grant types

The flow diagram below visually illustrates the basic architecture of this Api:
![alt text](api-flow-diagram.png)

### Installation

```shell script
$ docker pull corbinmoon/trumpbot-api
$ docker run -p 80:80 corbinmoon/trumpbot-api
```
