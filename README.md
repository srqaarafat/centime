# centime
centime api testing framework

api_base.py : All the basic building api methods, invoke api and get response methods are maintained here.
alpha_views.py : All utilitiy methods that supports the frame work like the methods to build different APIs aith differeent params, methods to validate schemas, methods to validate erros, response ..etc maintained here.
alpha_vantage_constants.py = All the supporting constants related to project are maintained here.
test_Intraday.py : All different test cases maintained here
conftest.py : ALl the supporting fixtures maintained here.
config.properties : All the environment level test data maintained here.

Step to run the test cases:

please run requirements.txt to install all required libraries using the below command :

pip install -r ./requirements.txt

please run the following command to run the testcases and to generate a report .html file:

pytest .\test\test_Intraday.py --env=test --html=abc.html



