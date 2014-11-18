#!/usr/bin/env python3

import argparse
import errno
import random
import select
import socket
import sys

def main():
  arg_parser = argparse.ArgumentParser(
    description="Repeatedly connect to server and fuzz with random bytes"
  )

  arg_parser.add_argument(
    "host",
    help="target server"
  )
  arg_parser.add_argument(
    "port",
    help="the port to fuzz",
    type=int,
  )
  arg_parser.add_argument(
    "--max-length",
    help="the maximum length of the noise",
    type=int,
    default=100
  )
  arg_parser.add_argument(
    "--min-length",
    help="the minimum length of the noise",
    type=int,
    default=1
  )
  arg_parser.add_argument(
    "--find-response",
    help="stop when we reach a response from the server",
    action="store_true",
    default=False
  )
  arg_parser.add_argument(
    "--response-file",
    help="the file to write a truncated response to when using --find-response",
    type=argparse.FileType('w')
  )
  arg_parser.add_argument(
    "--max-response-length",
    help="amount to truncate server response to, you may only get a packet's worth",
    type=int,
    default=1000000
  )
  arg_parser.add_argument(
    "--recv-timeout",
    help="how long in seconds to wait for the first byte of response",
    type=float,
    default=1
  )
  args = arg_parser.parse_args()

  find_response = args.find_response
  if args.response_file is not None and not args.find_response:
    sys.exit("--respone-file requires --find-response")

  host = args.host
  port = args.port
  recv_timeout = args.recv_timeout
  max_response = args.max_response_length
  response_file = args.response_file

  while True:
    response = ""
    soc = connect_nonblocking(host, port)

    if find_response and socket_ready(soc, recv_timeout):
      response = read_socket(soc, max_response)
      print("Response given on connect")

    # Don't bother sending if we found the response we were searching for it.
    if (find_response and len(response) == 0) or not find_response:
      fuzz = generate_fuzz(args.min_length, args.max_length)
      soc.send(fuzz)

      if find_response and socket_ready(soc, recv_timeout):
        response = read_socket(soc, max_response)
        print("Response found after sending (as python string): " + repr(fuzz))

    soc.close()

    if len(response) > 0 and find_response:
      if response_file is not None:
        args.response_file.write(response)

      break

def connect_nonblocking(host, port):
  soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  soc.connect((host, port))
  soc.setblocking(False)

  return soc

def generate_fuzz(min_length, max_length):
  fuzz = ""

  for _ in range(random.randint(min_length, max_length)):
    fuzz += chr(random.randint(0, 255))

  return fuzz

def socket_ready(soc, timeout):
  sockets_ready, _, _ = select.select([soc], [], [], timeout)

  return len(sockets_ready) > 0

def read_socket(soc, max_length):
  data = ""

  while len(data) < max_length:
    buf = ""

    try:
      buf = soc.recv(4096)
    except socket.error as e:
      err_code = e.args[0]

      # There was no data.
      if err_code in (errno.EAGAIN, errno.EWOULDBLOCK):
        break

      # The connection closed.
      if err_code in (errno.ECONNRESET,):
        break

      raise e

    data += buf

  return data[0:max_length + 1]

if __name__ == "__main__":
  main()
