random-fuzzer
=============

A very simple fuzzer designed to send random bytes and, if instructed to, capture the first reply and write it to a file.

This is simply a quick hack I wrote to debug an issue. I am willing to support this if bugs are filed and maybe even some enhancement requests, but left alone I will likely not touch it.

There is a lot of room for improvement, if you are interested in furthering the development of this project. This includes addition of concurrency (and at the same time gain the ability to wait longer for a response), keeping track of the number of connections attempted, optional banning of characters or provide a mask system, and so on. If I ever have a use for these things I'll add them, but don't hold your breath. Pull requests will be gladly merged after reviewed for style changes.
