# removes all dead screens
screen -wipe

# greps all detached screens and kills them by sending the 'quit' command to each of them
screen -ls | grep '(Detached)' | awk '{print $1}' | xargs -I % -t screen -X -S % quit
