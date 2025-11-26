#!/bin/bash

repo=$REPO
access_token=$ACCESS_TOKEN
student_id=$STUDENT_ID
registration_token=$(curl -X POST -H "Authorization: Bearer ${access_token}" -H "Accept: application/vnd.github+json" https://api.github.com/repos/${repo}/actions/runners/registration-token | jq .token --raw-output)

cd /home/docker/actions-runner

./config.sh --unattended --replace --url https://github.com/${repo} --name ${student_id} --labels ${student_id} --token ${registration_token}

cleanup() {
    echo "Removing runner..."
    remove_token=$(curl -X POST -H "Authorization: Bearer ${access_token}" -H "Accept: application/vnd.github+json" https://api.github.com/repos/${repo}/actions/runners/remove-token | jq .token --raw-output)
    ./config.sh remove --token ${remove_token}
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

./run.sh & wait $!
