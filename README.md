Data Scraping on Sports Website
==============================

This is a submission of **assignment 2** for the **CIS711** course.

It contains the code necessary to scrape data from a well-known sports website.

This repository is merely a demonstration of how web scraping performs.


Getting Started
------------
Clone the project from GitHub

`$ git clone https://github.com/tariqshaban/sports-data-scraper.git`

Install numpy
`pip install numpy`

Install pandas
`pip install pandas`

install matplotlib
`pip install matplotlib.pyplot`

Install scipy
`pip install scipy`

Install requests
`pip install requests`

Install beautiful soup
`pip install bs4`

No further configuration is required.


Project Structure
------------

    ├── README.md                 <- The top-level README for developers using this project.
    │
    ├── helpers
    │   ├── date_time_handler     <- Set of static methods that aid some time manipulations
    │   └── progress_handler      <- Set of static methods that aid some progress manipulations
    │
    ├── models
    │   ├── league                <- A container for storing league url as well as league name.
    │   └── club                  <- A container for storing club id as well as club name
    │
    ├── providers
    │   ├── plots_provider        <- Static methods which perform the plotting functionality
    │   └── sports_scraper        <- Static methods which perform the scraping functionality
    │
    └── main                      <- Acts as a sandbox for methods invocation


Report / Findings
------------

### What tools have been used to scrape data off the web?

Beautiful Soup has been used for scraping; it contains abstract out-of-the-box methods that help extract information
from the HTML file

> Beautiful Soup is a Python library for pulling
> data out of HTML and XML files. It works with your
> favorite parser to provide idiomatic ways of navigating,
> searching, and modifying the parse tree.
> It commonly saves programmers hours or days of work.

There were no modifications committed for this scraping tool since it already satisfies the required objectives.

### What were the target websites?

Primarily [ESPN](https://www.espn.in/)

### Why haven't you used the provided website (CNN Sports)?!

While [CNN Sports](https://edition.cnn.com/sport) is considered an excellent candidate for scraping, it only contains
data about the news itself (Title, images, date of release, content) rather than showing a list of players, etc.

### What information did you extract?

We successfully collected partial information of the following:

* Players
    * Name
    * Number
    * Position
    * Physical Status
    * Matches Stats (total goals, fouls, etc.)
* Leagues
    * League Name
    * League URL (for future scraping purposes)
* Clubs
    * League Name
    * Club Name
* Matches
    * Elapsed Matches
        * Opponents
        * Result
        * Location
        * Attendance
    * Fixtures
        * Opponents
        * Time
        * TV Channel

### What manipulations have you made for the data?

* Players
  * Column datatype conversion
  * Replaced blank spaces/empty values with nulls
  * Replaced double dashes with nulls
  * Converted weight from lbs to kg
  * Converted height from ft to meters
* Leagues
    * None
* Clubs
    * None
* Matches
    * Column datatype conversion
    * Replaced blank spaces/empty values with nulls
    * Replaced double dashes with nulls
    * Dropped rows that contained less than three non-null values

### What illustrations have you made?

***TBA***

### What experiments have you conducted?

***TBA***

### What hypothesis have you formulated?

***TBA***

--------