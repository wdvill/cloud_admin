echo "Deploy cloudwork"
git checkout master
git pull origin master
cd migrations
../../env/bin/python upgrade.py
cd ..
sudo supervisorctl restart cloudwork
