#!/bin/bash

gunicorn server:app -c python:config.gunicorn_config