while true
do
    ./get_data.py &
    PID=$!
    sleep 10
    kill $PID
done
