# Bridge

Pyrlang demo for bridging between python and elixir

## Installation

* install erlang OTP 21 and elixir 1.9 or 1.10
* install python 3.7
* install pyrlang :
  - pip install https://github.com/rizki96/bridge_demo/releases/download/0.1.0/pyrlang-term-1.2.tar.gz
  - pip install https://github.com/rizki96/bridge_demo/releases/download/0.1.0/pyrlang-0.9.tar.gz

## Running the demo

* open two terminal
* terminal1 run: > iex --name test@127.0.0.1 --cookie COOKIE -S mix run --no-halt
* terminal2 run: > python lib/pyrlang/test.py
* from iex console (terminal1) try run :
  - iex> alias Bridge.PyProxy
  - iex> PyProxy.hello()
