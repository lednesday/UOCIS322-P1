# README #

A "getting started" project for CIS 322, introduction to software engineering,
at the University of Oregon.

### What is this repository for? ###

The objectives of this mini-project are:

  * Experience with GIT workflow with separate configuration:
  Fork the project, make and test changes locally, commit;
  turn in configuration file with reference to repo.
  (Project 0 is practice for this part.)
  * Extend a tiny web server in Python, to check understanding of
  basic web architecture
  * Use automated tests to check progress (plus manual tests for good measure)

### What do I need?  Where will it work? ###

* Use the server to test, edit wherever you'd like.

* The server currently has all the requirements (if you don't know the
credentials, contact me.)

* Designed to work in "user mode" (unprivileged),
therefore using a port number above 1000.

### Assignment ###

* Fork this repository to create your own repository on GitHub,
and make sure it is PRIVATE. Be sure to add me as collaborator so I have access.
(Read the documentation as needed, and create an account on GitHub
  if you don't have one.
  You should've already done finished this as part of Project 0.)
* Clone your repository onto the machine you want to work on.
* Add the following functionality in pageserver.py.
(a) If URL ends with `name.html` or `name.css`
(i.e., if `path/to/name.html` is in document path (from DOCROOT)),
send content of `name.html` or `name.css` with proper http response.
(b) If `name.html` is not in current directory Respond with 404 (not found).
(c) If a page starts with or includes one of the symbols(~ // ..), and that includes the initial forward slash that all requests have, respond with 403 forbidden error. For example, `url=hostname:5000/..name.html`
or `/~name.html` would give 403 forbidden error.
* Make and test your changes. Use both automated tests
(the script in the 'tests' directory) and some manual tests.
* Revise this README.md file: Erase what is no longer relevant and add
identifying information.
If you have concerns about adding your email ID, let me know.

  ```
  ## Author: John Doe, jdoe@uoregon.edu ##
  ```

* Copy the credentials-skel.ini file to credentials.ini,
then edit it to contain correct information including your
GitHub repository URL. `credentials.ini` should NOT be under version control
(exclude it using your .gitignore file)
* Commit and push ALL your changes to GitHub
(except those not under revision control)
* Test deployment in other environments.
Deployment should work "out of the box" with this command sequence:

  ```
  git clone <yourGitRepository> <targetDirectory>
  ```

  ```
  cd <targetDirectory>
  ```

  ```
  make run or make start
  ```

  *test it with a browser now; send a request*

  ```
  make stop
  ```

* Alternatively, use the script under "tests" folder to test the
expected outcomes in an automated fashion.
It is accompanied by README file and comments (inside tests.sh)
explaining how to test your code.
* Check and revise your `credentials/credentials.ini` file.
The autograder will read this. Be precise.
The autograder IS NOT very good at guessing what you meant to write.
* Turn in the `credentials.ini` file in Canvas.
Autograder will use this file to access your GitHub repository.   

### Grading Rubric ###

* Your code works as expected: 100 points

* For every wrong functionality (i.e., (a), (b), and (c) above),
20 points will be docked off.

* If none of the functionalities work, 40 points will be given.
Assuming the credentials.ini is submitted with the correct URL of your repo.

* If credentials.ini is missing, 0 will be assigned.

### Credits ###

Ram Durairajan, Steven Walton, Joe Istas, Michal Yong
