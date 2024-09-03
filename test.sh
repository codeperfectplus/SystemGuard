#!/bin/bash

# Array of old and new filenames
declare -A files_to_rename=(
    ["src/models/card_settings.py"]="src/models/user_card_settings.py"
    ["src/models/dashboard_network.py"]="src/models/dashboard_network_settings.py"
    ["src/models/dashboard_settings.py"]="src/models/user_dashboard_settings.py"
    ["src/models/feature_toggles_settings.py"]="src/models/feature_toggle_settings.py"
    ["src/models/general_settings.py"]="src/models/application_general_settings.py"
    ["src/models/smtp_settings.py"]="src/models/smtp_configuration.py"
    ["src/models/speedtest.py"]="src/models/network_speed_test_result.py"
    ["src/models/system_info.py"]="src/models/system_information.py"
    ["src/models/user.py"]="src/models/user_profile.py"
)

# Loop through each key-value pair in the array
for old_name in "${!files_to_rename[@]}"; do
    new_name=${files_to_rename[$old_name]}
    # Check if the old file exists
    if [ -f "$old_name" ]; then
        echo "Renaming $old_name to $new_name"
        mv "$old_name" "$new_name"
    else
        echo "File $old_name not found, skipping."
    fi
done
