#!/bin/bash

echo "-------------------------------------------"
echo "______ _       _____       _     _ _      "
echo "|  ___(_)     /  ___|     (_)   | (_)     "
echo "| |_   _  ___ \ \`--. _ __  _  __| |_  ___ "
echo "|  _| | |/ _ \ \`--. \ '_ \| |/ _\` | |/ _ \\"
echo "| |   | | (_) /\__/ / |_) | | (_| | |  __/"
echo "\_|   | |\___/\____/| .__/|_|\__,_|_|\___|"
echo "     _/ |           | |                   "
echo "    |__/            |_|                   "
echo "-------------------------------------------"

set_config() {
    key="$1"
    value="${*:2}"
    evalue="$(echo "$value" | sed 's/[\/&]/\\&/g')"

    sed -ri "s/($key=).*/\1$evalue/" fjospidie.conf

}

if [ ! -z "$MONGO_HOST" ] && [ ! -z "$MONGO_PORT_27017_TCP_ADDR" ]; then
    echo "This FjoSpidie container is linked to a MongoDB Docker container, and given MONGO_HOST environment variable. Using linked MongoDB at $MONGO_PORT_27017_TCP_ADDR:$MONGO_PORT_27017_TCP_PORT"
fi
if [ -z "$MONGO_PORT" ] && [ -z "$MONGO_PORT_27017_TCP_PORT" ]; then
    MONGO_PORT=27017
fi

if [ ! -z "$MONGO_PORT_27017_TCP_ADDR" ]; then
    MONGO_HOST=$MONGO_PORT_27017_TCP_ADDR
fi
if [ ! -z "$MONGO_PORT_27017_TCP_PORT" ]; then
    MONGO_PORT=$MONGO_PORT_27017_TCP_PORT
fi


NET=$(ip a show dev eth0 |grep -w inet| awk '{print $2}' | sed "s/[0-9]*\/16/0\/16/") # Hack to replace IP with .0 :(
bpf="not ip6 and not net $NET"

set_config database_host "$MONGO_HOST"
set_config database_port "$MONGO_PORT"
set_config mynet "$NET"
set_config bpf $bpf

python fjospidie.py $@


