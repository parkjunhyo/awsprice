#! /usr/bin/env bash

offercodeapitarget="https://pricing.us-east-1.amazonaws.com"

offercodedir="offercodes"
if [[ -d $offercodedir ]]
then
  rm -rf $offercodedir
fi
 
mkdir $offercodedir
cd $offercodedir/
echo $(pwd)
wget $offercodeapitarget/offers/v1.0/aws/index.json
