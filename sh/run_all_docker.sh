# start the poem server:

bash run_client.sh &

echo "Poem Client loaded"

if ! echo "TEST" | nc localhost 10010; then
    cd ./;
    bash run_server.sh &
    while ! echo "TEST" | nc localhost 10010; 
    do
	sleep 10;
    done
    echo "Poem Server loaded and listen on localhost:10010";
fi;

if ! echo "HAFEZ:CONNECT" | nc localhost 50001; then
    cd ../sonnet-project-for-server/;
    bash initial_server_1.sh &
    while ! echo "HAFEZ:CONNECT" | nc localhost 50001; 
    do
	sleep 3;
    done
    echo "Rhyme Server 1 loaded and listen on localhost:50001";
fi;

if ! echo "HAFEZ:CONNECT" | nc localhost 50002; then
    cd ../sonnet-project-for-server/;
    bash initial_server_2.sh &
    while ! echo "HAFEZ:CONNECT" | nc localhost 50002; 
    do
	sleep 3;
    done
    echo "Rhyme Server 2 loaded and listen on localhost:50002";
fi;

if ! echo "HAFEZ:CONNECT" | nc localhost 50003; then
    cd ../sonnet-project-for-server/;
    bash initial_server_3.sh &
    while ! echo "HAFEZ:CONNECT" | nc localhost 50003; 
    do
	sleep 3;
    done
    echo "Rhyme Server 3 loaded and listen on localhost:50003";
fi;

export GEM_HOME="$HOME/gems"
export PATH="$HOME/gems/bin:$PATH"
cd ../jekyll/poem;
jekyll serve --host 0.0.0.0
