echo "starting posting matches process"
python main.py --user albert --post_matches AAPL &
echo "starting posting prices process"
python main.py --user albert --post_prices AAPL & 
echo "starting backend api server"
cd api 
flask --app server run & 
echo "done"