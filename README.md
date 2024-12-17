# P!nwheel Coding Challenge:

### Table of Contents

| [Set up](#set-up)                                                     |                                                  |
|-----------------------------------------------------------------------|---------------------------------------------------|
| [Utility1.py](#utility1py)                                            | [Input](#input-for-u1) / [Output](#output-for-u1) |
|                                                                       | [Troubleshooting](#troubleshooting)               |
|                                                                       | [Feedback](#feedback-on-u2)                       |
| [Utility2.py](#utility2py)                                            | [Input](#input-for-u2) / [Output](#output-for-u2) |
|                                                                       | [Feedback](#feedback-on-u1)                       |
| [Final Coding Challenge Takeaways](#final-coding-challenge-takeaways) |                                                   |
| [Possible Tax Feature Add-ons](#possible-tax-feature-add-ons)         |                                                   |
--------------------

### Set up:

- [x] *Have Python 3.10.0 installed* 

- [x] Set up a virtual environment: `virtualenv env`

- [x] Activate the env: `source env/bin/activate`

- [x] Install libraries for each respective utility: `pip3 install -r utility1/reqs.txt` or `pip3 install -r utility2/reqs.txt`

- [x] Before running the scripts, create environmental variables: Follow the steps in `setting_up_env_vars.md` to set these up yourself and familiarize yourself with the Network tab in your browser

------------------------

# `utility1.py`
*aka U1*

### Running `utility1.py` from root dir
`python utility1/utility1.py utility1/search_terms.txt`

![script 1](md_img/utility2-recording.gif)

### Input for U1
A file entitled `search_terms.txt` can be updated within the codebase. Each search query is preferrably on seperate lines. 

For example: `Form 1095-C` is one query and can be written on one line. Writing `Form` on one line and `1095-C` on another will give you same results. Putting `house` on the line after that line will give you far less results given IRS prior docs search algorithim. 

###  Test cases to input -> `search_terms.txt` (one example at a time!):
```
Ex:
Abatement
instructions

Ex:
Abatement instructions

Ex:
1099-NEC

Ex:
Form W-2

Ex:
1099-K

Ex:
-left blank-

Ex:
house
tax

Ex:
1099-MISC

```

### Output for U1
Script outputs JSON into the `utility1_results.html` file 

### Troubleshooting
- [x] Verify the IRS search HTML page structure hasn't changed! One issue with integration/reverse engineering API's (for sites that don't have an API) is changing tree structures.

- [x] Ensure your search terms file is correctly formatted with one query per line. The shorter the query, the better according to the IRS.g*v's search algorithim.

### Feedback on U1:
It was difficult to me, but not in an "I'm sweating way". I was more so interested in refamiliarizing myself with the Network tab in the Inspector. I spent many months in this tab during my contract at KBR, Inc. and things that took me a while to learn all came together for this assignment.

I learned new tricks in Selenium because I thought I'd have to use it to implement this task at the outset (I did not, but I still included a file that uses Selenium to navigate to an endpoint and reverse the order of a search query's results). Reading about the list user's tax-forms feature [P!nwheels application of it](https://docs.pinwheelapi.com/public/reference/list_tax_forms_v1_accounts__account_id__tax_forms_get) made the use case come alive.

I also became familiar with Beautiful Soup and got to implement handling [pagination](https://docs.pinwheelapi.com/public/docs/api-pagination) for the second time since I started developing. I have experience using FastAPI and JS for maintaining API's, so using only Python, and without a framework shows the power of the requests library on its own.

----------

# `utility2.py`:
*aka U2*
###  Command line arguments from root dir:
`python utility2/utility2.py`

![script 1](md_img/utility1-recording.gif)

### Input for U2
Input comes from a script called 'queries.txt` that you should edit. The first line should be your tax form publication number and the second line a range of years in this format: xxxx - xxxx (e.g. 2000 - 2024)

###  Test cases to put in `queries.txt` (one example at a time!):
```
Ex:
Form 1095-C
2021 - 2024

Ex:
Form W-2
2018 - 2022

Ex:
Form 8835
1800-2024

Ex:
Form 8609-A
1800-2024
```

One thing to note about the above examples for `utility2.py`:
This method of search is spotty. It's the IRS not you! Searching for the form 'Form 8609-A", "Form 8609" and even the keywords "house income" all return varyin results depending on the query, but not necessarily the ones you are looking for or need. See image:

Looking for Form 8609 via Title:
![results](md_img/inconsistent_results.png)

Looking for Form 8609 via query, but only Form 8609-A is queried:
![results](md_img/inconsistent_results2.png)

Looking for Form 8609 via exact Product Number match:
![results](md_img/inconsistent_results3.png)

*Should I email them?* ;)

### Output for U2
The script outputs folders with each folder name being representative of the exact IRS.g*v's "publication number"/"form number" for each tax doc. The names of the files should be an exact match as well of the form numer and the year of that form revision.

### Feedback on U2:
Nothing daunting. I just really wanted to finish. I was able to use a lot of the logic from `utility1.py`. I like that I broke this script up and made it modular. There's something satisfying knowing the data I wrangled is now accessbile, easy to capture and *pretty* all because of this script (minus the irs.gov search feature inconsistencies). 

I didn't necessarily learn anything new in task #2. Reading about [P!nwheels application of a GET request for tax-forms]([https://docs.pinwheelapi.com/public/reference/list_tax_forms_v1_accounts__account_id__tax_forms_get](https://docs.pinwheelapi.com/public/reference/get_tax_form_v1_accounts__account_id__tax_forms__tax_form_id__get) made the use case more realistic.

-----------

### Final coding challenge takeaways:

* One known flaw that I have in utility1.py is that when aggregating 'samemess' across form numbers and titles, the min/max currently calculates min/max by page number and not across all pages. I would implement that in version 2.

* Finally used a dictionary to keep track of items outside of it and having the dict itself be independant of pending JSON transformation, but instead used for a different type of tracking (the 'occurrences' variable in utility1.py)

* Although I used Ch*tGPT for certain helper functions, I found that there's no way (still) that it can take the place of background knowledge and the power of understanding certain logic. For example, I'd use it to pattern-match a much simpler concept in order to implement a complex one for utility2.py, but even on the small tasks it'd hallucinate. I also know that the free version is less up to date, so being aware of out of date libraries etc is key.

* Great podcast from [Syntax: Tasty Web Development Treats](https://syntax.fm/show/60/the-undocumented-web-scraping-private-apis-proxies-and-alternative-solutions) on web scraping I used to prep (although they frequently use JS...which is what I've mainly used to get client data in the past): 
    * [Web Scraping + Reverse Engineering APIs - 2024](https://open.spotify.com/episode/6QuwVPSE0iSORqDnx4VSVN?si=0935ad346c2541f2)
    * [The Undocumented Web - scraping, private APIs, proxies and “alternative solutions" -2018](https://open.spotify.com/episode/0YfWhIdgACU1fRSY9chGWq?si=ebfdab9a01bd4f39)

------------------------------

# Possible Tax Feature Add-ons
### Other possible tax form formats to offer to help better the financial lives of end consumers:
![funny_meme](md_img/bring_me_data_meme.jpg)

Adding a user flow that includes customers (businesses or their consumers) being able to select a processed data format based on their use case (outside of JSON and PDF). This could enhance flexibility and improve adoption across diverse user bases. These can account for the varying tech-saviness of customers.

Other possible format #1
Image Formats (.png, .jpg)
```
    Why:
        Essential for users needing visual representations of tax forms for manual reviews. Great for non-tech saavy users who in turn use a more antiquated tax filing system (if not a real life tax preparer).
    Use cases:
        Uploading tax form snapshots (like PDF but a picture version) to platforms requiring a visual proof of income or tax filing. Older systems most likely. Also whose to say in the future people won't use their own GPTs to gather their own data across a series of photographs of their own tax documents.
```

### Other possible format #2
(.csv or .xlsx)
```
    Why:
        Lightweight, human-readable, and easy to handle.
        Compatible with most spreadsheet tools (e.g., Excel, Google Sheets) and data analysis platforms.
    Use cases:
        Smaller CUs or niche banks might use real-life tax professionals to import income and expense data into tax preparation software.
        Financial planners could utilize these as well when analyzing tax data trends. 
  ```      

### Other possible format #3
(.pgp)
```
    Why:
        Encrypted and secure JSON
    Use cases:
        When I think of encryption-centered products, I think of blockchain, crypto etc and there are like underserved users in this arena who need viable            tax doc generation services for their tricky tax needs (they're often decentralized, high-volume, and cross-border transactions). I'm still learning          about decentralized finance (DeFi), NFT trading, and crypto staking income, but I know the tools for reporting are few and far between. Also, "High-          Net-Worth Individuals" with special privacy needs. Cross-border workers, digital nomads, and expatriates often need encrypted solutions for sharing           income verification forms or dual-country tax reports
  ```      
### Questions:
I noticed more tax forms are being added and currently the W-2 form is the only form that can have your data from last year parsed for P!nwheel clients. If not implemented already, will parsed user data for other tax form docs be availible soon?
