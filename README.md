
## Example usage:

Download this script (as a Zip file):
<img width="647" alt="Screenshot 2023-12-26 at 1 55 02 PM" src="https://github.com/bgwines/gpx-splitter/assets/2442246/2d935179-ae94-453e-b93f-1243c486bb50">

The GPX file must be placed in the same directory as this script.

Open the "Terminal" application, `cd` to the directory containing the file and the script (e.g. `cd ~/Downloads`), and run it as follows:

```
$ ./gpx_splitter.py scarface.gpx
scarface.gpx is a GPX file by **GaiaGPS**. It spans **15:13:14** hours.

The start of the GPX file is **2023-10-29 08:27:17-04:00 (EST)** / 2023-10-29 12:27:17+00:00 (UTC)
The   end of the GPX file is **2023-10-29 23:40:31-04:00 (EST)** / 2023-10-30 03:40:31+00:00 (UTC)
Please enter timestamps in your local timezone (EST), one by one. Each one may be in any of the following formats:
	1. 2023-10-29T14:25:33
	2. 14:25:33 (date inferred as 2023-10-29)
	3. 14:25 (seconds inferred as :00 and date inferred as 2023-10-29
Hit Enter when you're done.
... 09:00
... 11:00
... 23:00
... 
UTC timestamps that will be used:
	2023-10-29 13:00:00+00:00
	2023-10-29 15:00:00+00:00
	2023-10-30 03:00:00+00:00

scarface-split-1.gpx already exists; removing
scarface-split-2.gpx already exists; removing
scarface-split-3.gpx already exists; removing
scarface-split-4.gpx already exists; removing
Wrote scarface-split-1.gpx
Wrote scarface-split-2.gpx
Wrote scarface-split-3.gpx
Wrote scarface-split-4.gpx
```

Here's the output, uploaded to GaiaGPS:
* Split 1: https://www.gaiagps.com/datasummary/folder/128e10d9-3082-4efe-8bb8-e07d940bd72b/?layer=GaiaTopoRasterFeet
* Split 2 (contains some issue; not sure what; the file looks fine): https://www.gaiagps.com/datasummary/folder/d6b9650e-78a2-46eb-9a7a-52c1fcb03506/?layer=GaiaTopoRasterFeet
* Split 3: https://www.gaiagps.com/datasummary/folder/fb5fb20d-f638-4703-ad0a-622df9972973/?layer=GaiaTopoRasterFeet
* Split 4: https://www.gaiagps.com/datasummary/folder/07ad2495-f213-4ab5-8e0e-a5e0743dc5b1/?layer=GaiaTopoRasterFeet

A second test (which had no issues), which came from a file from Strava:
* Stinson Beach <-> Mt. Tam, Split 1: https://www.gaiagps.com/datasummary/folder/94247d82-0efb-48b0-90f2-6db5cb9f12d6/?layer=GaiaTopoRasterFeet
* Stinson Beach <-> Mt. Tam, Split 2: https://www.gaiagps.com/datasummary/folder/8814fe58-0583-4177-b4c2-93172ae1ce2c/?layer=GaiaTopoRasterFeet
* Stinson Beach <-> Mt. Tam, Split 3: https://www.gaiagps.com/datasummary/folder/f5fda520-e7fe-4e64-9d73-1ee9bd3131ed/?layer=GaiaTopoRasterFeet
