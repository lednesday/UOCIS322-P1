# UOCIS322 - Project 1 #

A "getting started" project for CIS 322, introduction to software engineering,
at the University of Oregon.

## Author: Lindsay Marean, linzanna@cs.uoregon.edu ##


## Description

* This is a very small server or API

* Designed to work in "user mode" (unprivileged),
therefore using a port number above 1000.


* Includes the following functionality:
(a) If URL ends with `name.html` or `name.css`
(i.e., if `path/to/name.html` is in document path (from `DOCROOT`)),
sends content of `name.html` or `name.css` with proper http response.
(b) If `name.html` is not in current directory responds with 404 (not found).
(c) If a page starts with or includes one of the symbols(`~` `//` `..`), and that includes the initial forward slash that all requests have, responds with 403 forbidden error. For example, `url=hostname:5000/..name.html`
or `/~name.html` gives 403 forbidden error.



