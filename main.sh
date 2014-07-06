

sudo apt-get update && sudo apt-get upgrade;

# install essentials
sudo apt-get install build-essential;
sudo apt-get update && sudo apt-get upgrade;
sudo apt-get install apache2 apache2.2-common apache2-utils;
sudo apt-get update && sudo apt-get upgrade;

# install python3 and libs
sudo apt-get install python3 python3-bs4;
sudo apt-get update && sudo apt-get upgrade;

# install APACHE
sudo apt-get install apache2 libapache2-mod-python;
sudo apt-get update && sudo apt-get upgrade;

# install lib APACHE2 para PYTHON-WEB
sudo apt-get install libapache2-mod-wsgi;
sudo apt-get update && sudo apt-get upgrade;

# install PIP
sudo apt-get install python3-setuptools
sudo easy_install3 pip


# in HOME
tar xzvf Django-1.6.5.tar.gz;
cd Django-1.6.5;
sudo python3 setup.py install;

sudo service apache2 restart;

# install mongodb
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10;
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list;
sudo apt-get update;
sudo apt-get install mongodb-org;

iptables -A INPUT -s 172.20.22.64 -p tcp --destination-port 27019 -m state --state NEW,ESTABLISHED -j ACCEPT;
iptables -A OUTPUT -d 172.20.22.64 -p tcp --source-port 27019 -m state --state ESTABLISHED -j ACCEPT;