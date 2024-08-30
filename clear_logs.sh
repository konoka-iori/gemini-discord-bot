#!/bin/bash

read -p "Are you sure you want to clear the log directory? (y/n): " answer

if [[ $answer == "y" || $answer == "Y" ]]; then
    rm -rf log/*
    echo "Log directory cleared."
else
    echo "Cancelled."
fi
