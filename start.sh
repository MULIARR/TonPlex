#!/bin/bash
export PYTHONPATH=$(pwd)/backend
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
