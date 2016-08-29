#!/usr/bin/env bash

# Configuration
SERVER='thiago@192.241.145.192'
DEPLOY_TO='~/coffee-advisor-api/'
EXCLUDE='*.swp .git/ db/sphinx/ tmp/ log/'
DRY_RUN=false

# Map the excluded files to rsync's options
function excludes {
  EXCLUDES=''
  for i in $(echo $EXCLUDE | tr " " "\n")
  do
    EXCLUDES="$EXCLUDES --exclude $i"
  done
}


# Run rsync
function upload_files {
  excludes

  CMD="rsync -avz $EXCLUDES"
  if $DRY_RUN ; then
    CMD="$CMD --dry-run"
  fi

  CMD="$CMD ./ $SERVER:$DEPLOY_TO"
  echo $CMD
  $CMD
}

# Stop containers
function down {
  ssh $SERVER "cd $DEPLOY_TO && docker-compose down"
}

# Start containers
function up {
  ssh $SERVER "cd $DEPLOY_TO && docker-compose build"
  ssh $SERVER "cd $DEPLOY_TO && docker-compose up -d"
}


# Run deployment
upload_files

if ! $DRY_RUN ; then
  down
fi

up
