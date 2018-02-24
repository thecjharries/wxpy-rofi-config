# `wxpy-rofi-config`

[![Build Status](https://travis-ci.org/thecjharries/wxpy-rofi-config.svg?branch=master)](https://travis-ci.org/thecjharries/wxpy-rofi-config) [![Coverage Status](https://coveralls.io/repos/github/thecjharries/wxpy-rofi-config/badge.svg)](https://coveralls.io/github/thecjharries/wxpy-rofi-config)

**NOTE**: The builds use the latest GTK3 wheel and might not test everything.

## Refactor

I'm currently refactoring the source. I slammed out the first couple of versions just to figure out wxPython, and it shows. I'm starting from scratch and rebuilding each component, taking the time now to research best practices, grok code I didn't quite understand the first time around, and implement proper messaging. Aside from some cosmetic stuff, the refactor shouldn't add any new features and might actually remove a few things until I can build them properly.

## Sample

I'm using [vanilla Equilux](https://github.com/ddnexus/equilux-theme). It uses native bindings so it should theme like your OS.

![Sample Screenshot](assets/sample.png)


## Overview

I've got a few goals with this project:

1. Test out `wxPython >=4.0`
2. Learn wxWidgets basics
3. Provide a GUI for `rofi` config

At the moment, I'm able to

* load `rofi`'s default and current configs
* provide a tabbed interface with settings
* include inline documentation
* save a rudimentary config file in an easy location

## Links

* [`rofi`](https://github.com/DaveDavenport/rofi)
* [`wxPython`](https://www.wxpython.org/)
