# Deploy script for connectical.com
# (c) 2011 Andres J. Diaz <ajdiaz@connectical.com>

if ! type -P python 2>&1 >/dev/null; then
	echo "* python >= 2.6 is a requirement. Install python in your system."
	echo "  Debian users: apt-get install python"
	exit 1
fi

if ! type -P virtualenv 2>&1 >/dev/null; then
	echo "* virtualenv is a requirement. Install python-virtualenv in your system."
	echo "  Debian users: apt-get install python-virtualenv"
	exit 1
fi

if ! type -P pip 2>&1 >/dev/null; then
	echo "* pip is a requirement. Install python-pip in your system."
	echo "  Debian users: apt-get install python-pip"
	exit 1
fi

if ! type -P git 2>&1 >/dev/null; then
	echo "* git is a requirement. Install git in your system."
	echo "  Debian users: apt-get install git"
	exit 1
fi

echo "Clonning website..."
git clone git://github.com/Connectical/connectical-web.git

echo "Conning growl..."
git clone git://furi-ku.org/code/growl

echo "Creating virtualenv..."
virtualenv /tmp/connectical.com

echo "Installing dependencies..."
/tmp/connectical.com/bin/pip install -r connectical-web/requirements.txt

echo "Entering website..."
cd connectical-web

echo "Building website..."
/tmp/connectical.com/bin/python ../growl/growl

echo "Removing growl..."
rm -rf ../growl

echo "Generating targz with site..."
mv _deploy connectical.com
tar cvzf ../connectical-web.tar.gz connectical.com

echo "Removing website..."
cd .. && rm -rf connectical-web
