# mcu-actor-appearances

Python script to scrape comic convention websites to find appearances of actors from Marvel Cinematic Universe movies. To run the script, checkout the repo like:
```
git clone https://github.com/rrrxr6/mcu-actor-appearances.git
```
Then run:
```
python main.py
```
This will produce output like:
```
[#####################################]
Danai Gurira
        Walker Stalker Atlanta (10-26-2018)

Dave Bautista
        Awesome Con (03-30-2018)
        C2E2 (04-06-2018)
        Wizard World Portland (04-13-2018)
        Wizard World Philly (05-17-2018)
        Florida Supercon (07-12-2018)
        Raleigh Supercon (07-27-2018)
        Wizard World Chicago (08-23-2018)

Evangeline Lilly
        Salt Lake Comic Con (09-06-2018)

---------------------------
Added: {'Danai Gurira'}
Removed: set()
Modified: {}
Same: {'Dave Bautista', 'Evangeline Lilly'}
---------------------------
Errors:
The server at http://someconvention.com/guests/ couldn't fulfill the request.
Reason: Service Unavailable
Error code: 404
---------------------------
```
