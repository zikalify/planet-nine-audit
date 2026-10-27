[1] SCANPI Input Parameters — irsa.ipac.caltech.edu
https://irsa.ipac.caltech.edu/IRASdocs/scanpi_inputs.html

SCANPI Input Parameters

## IRAS

The following list of input parameters may all optionally be modified.

### SPIMED
: Path and name for the SCANPI median scans output file

 Example: ~ipac123/a01data

 Default: blank
### SPISUM
: Path name for the output file containing the ASCII summary tables for all bands (same as the printed summary tables).

 Example: ~ipac123/a01table

 Default: blank
### TITLE
: A label to be shown on each plot. 30 characters maximum. 
### NOPT
: Controls processing of individual scans. 

- NOPT=0 All individual data strings are processed and shown 
- NOPT=1 Only strings specified by user will be processed and shown 
- NOPT=2 Only the four coadded strings are processed and shown 
- NOPT=21 Only median coadded string is processed and shown 

Default: 2
### NOPLOT
: Controls plot output. 

- NOPLOT=0 Plots are generated 
- NOPLOT=1 No plot output 

Default: 0 
### SUMPLT
: Controls output of summary plots. 

- SUMPLT=0 No summary or scan track plot output 
- SUMPLT=1 Summary and scan track plots are generated 

Default: 0 
### NOPRNT
: Controls detailed printout. 

- NOPRNT=0 Detailed printout is generated 
- NOPRNT=1 Only the tables are output 

Default: 1 
### NBAND(4)
: Controls which bands are processed.

 i=1, 2, 3, 4 for 12, 25, 60, 100 µm, respectively. 

- NBAND(i)=0 No processing for ith band 
- NBAND(i)=1 Band is processed 

Default: 1, 1, 1, 1 (all 4 bands processed) 
### TOTLS(4)
: Portion (in arcminutes) of string to be used in baseline fitting for each band, centered on target position.

 Default: 15., 15., 20., 30. 
### SIGLS(2, 4)
: Signal range (in arcminutes) used for the integrated flux (fnu(t)) for each band, centered on target position.

 Default: (-2., 2.), (-2., 2.), (-2.5, 2.5), (-4., 4.) 
### MISS
: Allowed deviation (in arcminutes) of signal position from the target position. If not specified, MISS is determined to be the location where the best template fit occurs. If MISS is specified, the point source template will be centered at that point.

 Default: 999.99 (same as no input)

 NOTE: If MISS is not specified, the template fit will be restricted to within 0.5' of the nominal position at 12 and 25, within 1.0' at 60, and within 2.0' at 100 µm. 
### YBOTTMS
: Starting flux values (in watts/m^2) for Y-axis on each scan plot. If input values are zero, the program will compute the range.

 Default: 0., 0., 0., 0. 
### YTOPS
: Ending flux values (in watts/m^2) for Y-axis. Zeros give auto-scaling.

 Default: 0., 0., 0., 0. 
### NDEG(4)
: Degree of polynomial used in baseline fit. Max value is 9.

 Default: 2, 2, 2, 2 
### OTOMSK(4)
: The threshold for masking out large deviations from the baseline in the iterative fit. OTOMSK multiplied by RMS determines the maximum deviation (larger deviations are discarded). Set to 0 for no masking.

 Default: 2.5, 2.5, 2.5, 2.5 
### ITMPL
: Controls template fitting. 

- ITMPL=0 Fitting is performed with the template baseline as a free parameter 
- ITMPL=1 Baseline of template tied to large-scale baseline 

Default: 0 
### TMPRNG(4)
: Range in arcminutes over which template fitting is to be performed. Acceptable values for each band are: 

- 2.7 to 7.5 for 12 µm 
- 2.7 to 7.5 for 25 µm 
- 5.5 to 15.1 for 60 µm 
- 10.9 to 30.1 for 100 µm 

Default: 3.5, 3.5, 6.5, 13.1 
### NCOADD(4)
: Number of scans to be coadded in each band. A value of -1 means all scans in the window.

 Default:-1, -1, -1, -1 
### EWXLIM(2)
: Limits distance in arcminutes from center of the detector, in the East-West direction, for which scans are included in the coaddition. Zero means no limit.

 Default: 0.0, 0.0 
### NS12(50), NS25(50), NS60(50), NS100(50)
: List, by scan number, of the scans to be coadded for the 12, 25, 60 and 100 µm band. The number of scans must match NOCADD(i), where i=1,2,3,4 for the 12,25,60 and 100 µm bands respectively. If NCOADD(i)=-1, this parameter is ignored.

 No default.

| <-- Previous Section | Next Section --> |
| --- | --- |
| (SCANPI & SUPERSCANPI Processing) | (SCANPI Output) |
