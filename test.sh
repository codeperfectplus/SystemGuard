get_user_home() {
    if [ -n "$SUDO_USER" ]; then
        # When using sudo, SUDO_USER gives the original user who invoked sudo
        TARGET_USER="$SUDO_USER"
    else
        # If not using sudo, use LOGNAME to find the current user
        TARGET_USER="$LOGNAME"
    fi
    
    # Get the home directory of the target user
    USER_HOME=$(eval echo ~$TARGET_USER)
    echo "$USER_HOME"
}

USER_HOME=$(get_user_home)
echo "USER_HOME: $USER_HOME"
# get only user name
USER_NAME=$(echo $USER_HOME | awk -F'/' '{print $3}')
echo "USER_NAME: $USER_NAME"