# trumpbot-api

A simple Trump chatbot Api built using TensorFlow, Keras, textgenrnn, Flask-RESTX, SQLAlchemy and Authlib.
This Api includes the following:
- Multi-class text classification model
- Text generation models (with direct correspondence to labels from classification model)
- OAuth2 implementation with password and authorization code grant types

The flow diagram below visually illustrates the basic architecture of this Api:
![alt text](api-flow-diagram.png)

##### TODOs:
- fix image upload endpoint for user profiles
- fix custom error handler
- add unit/integration tests
- add automated deployment of docker container to hosting site
