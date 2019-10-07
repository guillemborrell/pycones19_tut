# Flappystream

![Screenshot](https://github.com/guillemborrell/pycones19_tut/raw/master/doc/shot.png)

An instrumented flappybird game to experiment with real time streaming with Python.

The application is broken up in three independent Python applications

* flappystream-source: A ASGI application that serves the game's javascript + html and manages the logs

* flappystream-analysis: Some handy tools to analyze the game's log stream

* flappystream-worker: Worker where the actual analysis is run

This project is a showcase for some interesting Python technologies useful for building an AA streaming platform.
