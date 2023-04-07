#!/bin/bash

# AWS Multi-Session Assume Role
# -----------------------------
# The script creates an MFA session with the access keys of a user
# It uses that session to refresh all role sessions across all accounts
# Also saves all the profile names to `profile_names` in the cwd


# Change these values:
# Set the user's access keys
echo "[default]
aws_access_key_id="<AKIA...>"
aws_secret_access_key="<sak....>"
" > ~/.aws/credentials
# Account number of the user that is assuming the role
praetoacc="<ACC_ID>"
# Name of MFA device for the user that is assuming
mfadev="<MFA_Name>"
# Name of the role in other accounts that will be assumed
rolename="<ROLE_Name>"


# Read MFA token and create STS session with MFA set as true
read -p "MFA Code: " token
values=$(aws sts get-session-token --serial-number arn:aws:iam::$praetoacc:mfa/$mfadev --token-code $token)
ak=$(echo $values | jq '.Credentials.AccessKeyId' | tr -d "\"")
sak=$(echo $values | jq '.Credentials.SecretAccessKey' | tr -d "\"")
st=$(echo $values | jq '.Credentials.SessionToken' | tr -d "\"")
echo "[mfaprofile]
aws_access_key_id=$ak
aws_secret_access_key=$sak
aws_session_token=$st
" >> ~/.aws/credentials
echo -n "" > profile_names
echo -n "" > account_names


# Populate the array below in the format shown for all accounts
# that you need to assume a role in; part after : will be the profile name

accounts=(
    "acc_num:alias"
    "acc_num2:alias2"
)

for account in "${accounts[@]}"
do
    IFS=":" read -ra acct <<< "$account"
    acct_num="${acct[0]}"
    alias="${acct[1]}"
    echo $alias >> profile_names
    echo "$acct_num:$alias" >> account_names
    values=$(aws sts assume-role --role-arn arn:aws:iam::$acct_num:role/$rolename --role-session-name $alias --profile mfaprofile)
    ak=$(echo $values | jq '.Credentials.AccessKeyId' | tr -d "\"")
    sak=$(echo $values | jq '.Credentials.SecretAccessKey' | tr -d "\"")
    st=$(echo $values | jq '.Credentials.SessionToken' | tr -d "\"")
    echo "[$alias]
aws_access_key_id=$ak
aws_secret_access_key=$sak
aws_session_token=$st
" >> ~/.aws/credentials
    echo "Role in $alias assumed!"
done