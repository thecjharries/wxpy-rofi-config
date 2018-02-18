# `wxpy-rofi-config`

[![Build Status](https://travis-ci.org/thecjharries/wxpy-rofi-config.svg?branch=master)](https://travis-ci.org/thecjharries/wxpy-rofi-config) [![Coverage Status](https://coveralls.io/repos/github/thecjharries/wxpy-rofi-config/badge.svg)](https://coveralls.io/github/thecjharries/wxpy-rofi-config)

**NOTE**: The builds are failing miserably on Travis because `wxPython` takes forever to build. I'll investigate a Docker later. In the mean time, if you're interested, all the tests are in the repo. `master` should always be (fairly) stable and near 100% coverage (for now).

## Refactor

I'm currently refactoring the source. I slammed out the first couple of versions just to figure out wxPython, and it shows. I'm starting from scratch and rebuilding each component, taking the time now to research best practices, grok code I didn't quite understand the first time around, and implement proper messaging. Aside from some cosmetic stuff, the refactor shouldn't add any new features and might actually remove a few things until I can build them properly.

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
