#!/bin/sh

IMG_NAME="twitch_queue_bot"

docker run -d -v ./:/bot $IMG_NAME