###########################################
# Fetching the 2000 surname data
echo "Downloading 2000 data"
echo "====================="

FETCHED_DIR=./wrangle/corral/fetched/census-2000
FETCHED_ZIP=$FETCHED_DIR/surnames.zip
mkdir -p $FETCHED_DIR

curl http://www2.census.gov/topics/genealogy/2000surnames/names.zip \
      -o $FETCHED_ZIP
echo "Unzipping $FETCHED_ZIP"
unzip -oL $FETCHED_ZIP \
   -d $FETCHED_DIR



###########################################
# Fetching the 1990 surname data, which includes some first name data
echo "Downloading 1990 data"
echo "====================="

FETCHED_DIR=./wrangle/corral/fetched/census-1990
mkdir -p $FETCHED_DIR

# last names distributions
destpath=$FETCHED_DIR/surnames.txt
echo "Downloading to $destpath"
curl -o  $destpath \
    http://www2.census.gov/topics/genealogy/1990surnames/dist.all.last

# first name distributions
for gender in male female; do
    destpath=$FETCHED_DIR/firstnames-$gender.txt
    echo "Downloading to $destpath"
    curl -o $destpath \
        http://www2.census.gov/topics/genealogy/1990surnames/dist.$gender.first
done
