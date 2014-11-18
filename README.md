About
=====

A very simple fuzzer designed to send random bytes and, if instructed to, capture the first reply and write it to a file.

This is simply a quick hack I wrote to debug an issue. I am willing to support this if bugs are filed and maybe even some enhancement requests, but left alone I will likely not touch it.

There is a lot of room for improvement, if you are interested in furthering the development of this project. This includes addition of concurrency (and at the same time gain the ability to wait longer for a response), keeping track of the number of connections attempted, optional banning of characters or provide a mask system, and so on. If I ever have a use for these things I'll add them, but don't hold your breath. Pull requests will be gladly merged after reviewed for style changes.

Usage
=====
```
usage: noise-fuzz.py [-h] [--max-length MAX_LENGTH] [--min-length MIN_LENGTH]
                     [--find-response] [--response-file RESPONSE_FILE]
                     [--max-response-length MAX_RESPONSE_LENGTH]
                     [--recv-timeout RECV_TIMEOUT]
                     host port

Repeatedly connect to server and fuzz with random bytes

positional arguments:
  host                  target server
  port                  the port to fuzz

optional arguments:
  -h, --help            show this help message and exit
  --max-length MAX_LENGTH
                        the maximum length of the noise
  --min-length MIN_LENGTH
                        the minimum length of the noise
  --find-response       stop when we reach a response from the server
  --response-file RESPONSE_FILE
                        the file to write a truncated response to when using
                        --find-response
  --max-response-length MAX_RESPONSE_LENGTH
                        amount to truncate server response to, you may only
                        get a packet
  --recv-timeout RECV_TIMEOUT
                        how long in seconds to wait for the response
```
