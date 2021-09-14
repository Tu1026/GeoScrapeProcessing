SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd $SCRIPT_DIR
echo What is the name of the file that contains the filtering terms
read filter
echo what is the name of your geo file;
read geo;
pipenv run python filtering.py $filter $geo;