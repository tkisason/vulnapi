#!/bin/bash

uvicorn main:app --http h11 --reload --host 0.0.0.0