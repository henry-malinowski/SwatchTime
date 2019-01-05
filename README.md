# SwatchTime

[![Maintainability](https://api.codeclimate.com/v1/badges/dd0f9388c802c7c8cea2/maintainability)](https://codeclimate.com/github/henry-malinowski/SwatchTime/maintainability)

SwatchTime is a Python program for displaying the current date and time using [Swatch Internet Time](https://en.wikipedia.org/wiki/Swatch_Internet_Time). It provides a set of flags that are useful for a caller from the CLI or as part of a module for another program; like a [Polybar](https://github.com/jaagr/polybar) [module](https://github.com/jaagr/polybar/wiki/User-contributed-modules).  Currently the flags are mostly stable, but may be changed in the future to be more like [`date`](https://linux.die.net/man/1/date).

## Installation

Copy the python script to a location that is in your path. On way might be...

```sh
sudo install -m 0755 swatchtime.py /usr/bin/swatchtime
```

### Arch Linux

A `PKGBUILD` file will be included or (submitted to the AUR) in the future to streamline installation and updating.

## Usage

`-h, --help` Print help message and exit

`-v, --verbose` Shows the PID a few seconds before starting. (default: False)

`-t, --tail` Enables tail output mode. (default: False)

`-d, --delay` The delay between refreshes in tail mode; only applies if tail mode is set. (default: 1 second)

`-f, --format` A mostly [strftime](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) compliant string to format the Swatch Time. A notable addition is a way to denote how and where to format the current .beat. (default: `d%d.%m.%y@{Beat}`)

* `{Beat}` will format the number of beats with left-padding zeros.
  * Example `swatchtime --format d%d.%m.%y@{beat}` will output `d19.5.19@1`
* `{beat}` will format the number of beats without padding zeros.
  * Example `%G-%m-%d@{Beat}` will output `2019-05-19@001`

`--alt-format` Format to switch to after receiving a USR1 signal; only applies if tail output is set. (default: None). Unlike the format argument, this must be a strictly [strftime](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior) compliant string. Examples:

* `swatchtime -t --alt-format %c` produces `Thu Jan  4 05:45:16 2019` (similar to `date`)

* `swatchtime -t --alt-format %Y-%m-%dT%H:%M:%S` produces `2019-01-04T04:45:19` (an ISO-8601 string for local time)

`-u, --utc, --universal` Displays standard time as UTC (Coordinated Universal Time). (default: False)

* `swatchtime -t -u --alt-format %Y-%m-%dT%H:%M:%SZ` produces `2019-01-04T04:45:19Z` (an ISO-8601 string for Zulu time).

*Note: Both format options may be called using 'single-quotes', "double-quotes", or no quotes. Quotation marks are only needed if the formatting string contains a space.*