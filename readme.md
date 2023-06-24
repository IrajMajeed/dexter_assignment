## To run this project, 
Clone the repo : git clone https://github.com/IrajMajeed/dexter_assignment.git

# Open terminal 
activate virtual environment using commnad source env/bin/activate

# navigate to dexter_project using these commands
cd dexter/dexter_project

run this command
bash build.sh 

This will add stubs in all the required directories

After that run this command to run the microservices
docker-compose up --build

# You can test the api  by this curl. Simply copy and paste this in postman and send request. Output will be shown on Terminal.

curl --location --request GET 'localhost:9000/audio-wave/' \
--header 'Cookie: csrftoken=Lt89xtLc6uOshKXCsKv7ZpylA8m4RTaXuZ4rOQLvjWqobBnAgwfaDnSCLUFGuA38'