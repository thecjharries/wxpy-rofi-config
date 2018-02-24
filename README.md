# `wxpy-rofi-config`

[![Build Status](https://travis-ci.org/thecjharries/wxpy-rofi-config.svg?branch=master)](https://travis-ci.org/thecjharries/wxpy-rofi-config) [![Coverage Status](https://coveralls.io/repos/github/thecjharries/wxpy-rofi-config/badge.svg)](https://coveralls.io/github/thecjharries/wxpy-rofi-config)

**NOTE**: The builds use the latest GTK3 wheel and might not test everything.

<!-- MarkdownTOC -->

- [Overview](#overview)
- [Sample](#sample)
- [Links](#links)

<!-- /MarkdownTOC -->

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

## Sample

I'm using [vanilla Equilux](https://github.com/ddnexus/equilux-theme). It uses native bindings so it should theme like your OS.

![Sample Screenshot](assets/sample.png)

## Links

* [`rofi`](https://github.com/DaveDavenport/rofi)
* [`wxPython`](https://www.wxpython.org/)
