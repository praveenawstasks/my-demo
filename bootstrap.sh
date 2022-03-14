#!/bin/bash
echo "Provided bootstrap execution started..."

sudo yum update -y
echo "yum update completed..."

echo "Git installation started..."
sudo yum install git -y
echo "Git installation completed..."

echo "base packages installed..."

pip install pandas

echo "All bootstrap actions completed!"

cd /home/hadoop

pwd

git clone https://github.com/praveenawstasks/my-demo.git

echo "Cloning my-demo completed!"

cd my-demo