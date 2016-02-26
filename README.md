# Badge.Kloud51.com

Badge/Pins/Shields/Medal or what so ever for projects.

Services Supported:

* Python [PyPi](https://pypi.python.org/)
* ArchLinux [AUR](https://aur.archlinux.org/)


## Badges

### PyPi

PyPi badges are the first of course, this project has been written in Python.
Currently below actions are supported.


* Downloads: ![d, download](http://badge.kloud51.com/pypi/d/html2text.svg)
  * URL:  http://badge.kloud51.com/pypi/d/html2text.svg
  * Actions: `d`, `download`
* Version: ![v, version](http://badge.kloud51.com/pypi/v/html2text.svg)
  * URL: http://badge.kloud51.com/pypi/v/html2text.svg
  * Actions: `v`, `version`
* Python Versions: ![py_versions](http://badge.kloud51.com/pypi/py_versions/html2text.svg)
  * URL: http://badge.kloud51.com/pypi/py_versions/html2text.svg
  * Action `py_versions`
* Wheel: ![wheel, w](http://badge.kloud51.com/pypi/w/html2text.svg)
  * URL: http://badge.kloud51.com/pypi/w/html2text.svg
  * Action: `w`, `wheel`
* Egg: ![e, egg](http://badge.kloud51.com/pypi/e/html2text.svg)
  * URL: http://badge.kloud51.com/pypi/e/html2text.svg
  * Actions: `e`, `egg`
* Implementation: ![i, implementation](http://badge.kloud51.com/pypi/i/html2text.svg)
  * URL: http://badge.kloud51.com/pypi/i/html2text.svg
  * Actions: `i`, `implementation`
* Status: ![s, status](http://badge.kloud51.com/pypi/s/html2text.svg)
  * URL: http://badge.kloud51.com/pypi/s/html2text.svg
  * Actions: `s`, `status`
* License: ![l, license](http://badge.kloud51.com/pypi/l/html2text.svg) 
  * URL: http://badge.kloud51.com/pypi/l/html2text.svg
  * Actions: `l`, `license`
* Format: ![f, format](http://badge.kloud51.com/pypi/f/html2text.svg)
  * URL: http://badge.kloud51.com/pypi/f/html2text.svg
  * Actions: `f`, `format`


#### ArchLinux AUR

ArchLinux and its AUR is lovely, no need to mention the server powering [badge.kloud51.com](http://badge.kloud51.com)
is Kloud51 customized ArchLinux 64 bit backed by `OpenVZ`.

* Version: ![v, version](http://badge.kloud51.com/aur/v/git-cola.svg)
  * URL: http://badge.kloud51.com/aur/v/git-cola.svg
  * Actions: `v`, `version`
* Number of Votes:![num_votes](http://badge.kloud51.com/aur/num_votes/git-cola.svg)
  * URL: http://badge.kloud51.com/aur/num_votes/git-cola.svg
  * Actions: `num_votes`
* Popularity: ![p, popularity](http://badge.kloud51.com/aur/p/git-cola.svg)
  * URL: http://badge.kloud51.com/aur/p/git-cola.svg
  * Actions: `p`, `popularity`
* Status: ![s, status](http://badge.kloud51.com/aur/s/git-cola.svg)
  * URL: http://badge.kloud51.com/aur/s/git-cola.svg
  * Actions: `s`, `status`
* Maintainer: ![v=m, maintainer](http://badge.kloud51.com/aur/m/git-cola.svg)
  * URL: http://badge.kloud51.com/aur/m/git-cola.svg
  * Actions: `m`, `maintainer`
* License: ![l, license](http://badge.kloud51.com/aur/l/git-cola.svg)
  * URL: http://badge.kloud51.com/aur/l/git-cola.svg
  * Actions: `l`, `license`



## Tests

We're writing tests with `unittest` library provided by Python Standard Library.
Running the test suit has been implemented via a simple Fabric task.

To run the `badge` tests:

```
fab run_tests
```

## License

Badge is licensed and distributed under MIT License.
