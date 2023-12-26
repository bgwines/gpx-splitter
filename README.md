## Example usage:

The GPX file must be placed in the same directory as this script.

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
