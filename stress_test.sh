#!/bin/bash

locust -f test_data_populate.py --headless --users 10000 --spawn-rate 50 --run-time 40s --host http://localhost:3000
