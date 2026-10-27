[1] Scanpi Program Interface — irsa.ipac.caltech.edu
https://irsa.ipac.caltech.edu/applications/Scanpi/docs/ScanpiProgramInterface.html

Scanpi Program Interface

Some ZTF services (including ZTF Lightcurve Queries) are currently unavailable. 

## IRAS Scan Processing and Integration tool (Scanpi): Program Interface 

 Introduction Examples XML Output Description of XML Tags 

Scanpi is an interactive tool for viewing, plotting, and averaging the calibrated survey scans from the Infrared Astronomical Satellite (IRAS); these scans are the fundamental data from the IRAS survey. These data can be accessed via an interactive front end (filling in a web form for searching data), as well as via an HTTP GET/POST program interface where the request is a set of "

parameter=value

" pairs and the return is an XML document containing URL links to the resulting data and metadata. 

 This document describes these input parameters, the HTTP GET request which can be created to get results in an non-web form interactive fashion, and the structure of the returned XML. 

 Note: Some of the more interactive features found on the HTML form interface (such as iterative fitting, including/exclusing scans in the coaddion scan) are not available in the program interface. Program-mode programmer/users will presumably want to control this sort of functionality themselves. 

 Similarly, the table upload option on the form interface (which loops over a list of coordinates to produce all the results in one submit) is not necessary in program mode since programmers can perform this looping themselves. 

 Several of the input parameters have default values, so queries are quite straightforward, as shown in the following example: https://irsa.ipac.caltech.edu/cgi-bin/Scanpi/nph-scanpi?locstr=M31&band1=12um&band2=25um&band3=60um&band4=100um&mode=PI 

 where the 

- The Base URL for the service is

 https://irsa.ipac.caltech.edu/cgi-bin/Scanpi/nph-scanpi 
- Input parameters are specified by standard parameter/value pairs. For instance, "

locstr=M31

" searches for data covering location "

M31

" (Messier object 31). Note that additional parameters are needed, such as those to specify the IRAS band wavelength requested. These additional parameters are explained in detail below. 
- Output is an XML document containing a set of URL links to: summaries of retrieved counts; the metadata tables; the download scripts for the retrieved data; and, for completeness, the HTML result page generated for the default interactive (non-program) mode. See the output from Example 3 in the XML Output section below for details. 

 Input Parameters Introduction Examples XML Output Description of XML Tags 

 The input parameters are entered as standard HTTP "

parameter=value

" pairs in HTTP/GET syntax. In this syntax, the parameter name is followed by an equal sign which is then followed by a value. No extra spaces are allowed and if the value contains any spaces or special characters that might cause ambiguities they have to be encoded as shown in any HTTP or URL reference (e.g. here). As shown above, these pairs are separated from each other by ampersand (&) characters. 

 The parameters are grouped here for presentation clarity into two subsets: manadatory search parameters and optional search parameters (which can be used to change the data fitting input limits or boundaries). 

 Manadatory Search Parameters for all queries 

| Parameter | Values | Default | Description |
| --- | --- | --- | --- |
| locstr | (locstr examples) | NA | This is the search location parameter; is required for all searches. The input can be a coordinate or astronomical object name; if it is an object name, it is resolved into coordinates using NED and, if that fails, SIMBAD is used for name resolution. |
| band1 | 12um | NA | This sets the state of iterative processing for IRAS band 1 (12µm) for Scanpi. This parameter must be set for the first iteration of fitting in order for the program to recognize the initial state (1st fitting of a user source) for processing of 12µm IRAS band. If this parameter is missing from the CGI argument list, then no fitting is performed for IRAS band 1 (12µm). |
| band2 | 25um | NA | This sets the state of iterative processing for IRAS band 2 (25 µm) for Scanpi. This parameter must be set for the first iteration of fitting in order for the program to recognize the initial state (1st fitting of a user source) for processing of 25µm IRAS band. If this parameter is missing from the CGI argument list, then no fitting is performed for IRAS band 2 (25 µm). |
| band3 | 60um | NA | This sets the state of iterative processing for IRAS band 3 (60µm) for Scanpi. This parameter must be set for the first iteration of fitting in order for the program to recognize the initial state (1st fitting of a user source) for processing of 60µm IRAS band. If this parameter is missing from the CGI argument list, then no fitting is performed for IRAS band 3 (60µm). |
| band4 | 100um | NA | This sets the state of iterative processing for IRAS band 4 (100µm) for Scanpi. This parameter must be set for the first iteration of fitting in order for the program to recognize the initial state (1st fitting of a user source) for processing of 100µm IRAS band. If this parameter is missing from the CGI argument list, then no fitting is performed for IRAS band 4 (100µm). |
| mode | PI | NA | Scanpi can be run in several different modes; this document is specific to Program Interface (PI) mode only. The mode must be set to "PI" to return results in XML. If the mode is not set, the program's default results set is in HTML, not XML. |

 Optional Search Parameters for Fitting/Plotting limits 

 The following optional parameters are used to change the fitting limits as well as the plotting display ranges. These parameters are set optimally for most search results, but can be manipulated by the user to better match their fitting needs. The fitting range parameters for 4 bands are described in the below. All parameters are +/- of the source center. A visualization of all the fitting ranges is available. 

| Parameter | Values | Default | Description |
| --- | --- | --- | --- |
| det_distance | Valid range: 0.1 to 3.0 arcmin | 2.2 | Maximum Allowable Distance From Detector Center, in units of arcminutes. This parameter is used in a coarse approximation of all detectors which pass within the allowable distance of the source, using orbit-based parameters and calculation. The next parameter, "Cross Scan Distance", is used as the precise distance a scan can be from the source. Unlike the "Cross Scan Distance" parameter, the precision of this Maximum Allowable Distance From Detector Center can be off by as much as ~0.5 arcmin, and so is a padded value of the next parameter. |
| cross_scan | Valid range: 0.0 to 3.0 arcmin | 1.7 | The cross-scan distance around the position of interest which will be searched for IRAS scan data. After the coarse approximation in finding all the detectors within an allowable distance from the source, this cross-scan distance is used as a definitive, precise calculation as to whether a scan is within the user-defined limiting distance from the source. The units are arcminutes. |
| src_fit1 | Valid range: 1.0 to 30.0 arcmin | 1.7 | The distance from center (in arcmin) to be included in the source fit, for IRAS Band 1 (12µm). Note that the Source Fitting Range must be smaller than the "Source Exclusion Range" (srcex_fit1 parameter value), per band. |
| src_fit2 | Valid range: 1.0 to 30.0 arcmin | 1.7 | The distance from center (in arcmin) to be included in the source fit, for IRAS Band 2 (25 um). Note that the Source Fitting Range must be smaller than the "Source Exclusion Range" (srcex_fit2 parameter value), per band. |
| src_fit3 | Valid range: 1.0 to 30.0 arcmin | 3.2 | The distance from center (in arcmin) to be included in the source fit, for IRAS Band 3 (60µm). Note that the Source Fitting Range must be smaller than the "Source Exclusion Range" (srcex_fit3 parameter value), per band. |
| src_fit4 | Valid range: 1.0 to 30.0 arcmin | 6.4 | The distance from center (in arcmin) to be included in the source fit, for IRAS Band 4 (100µm). Note that the Source Fitting Range must be smaller than the "Source Exclusion Range" (srcex_fit4 parameter value), per band. |
| bg_fit1 | Valid range: 1.0 to 60.0 arcmin | 30.0 | The outer distance from center (in arcmin) to be used in background fits for coadd scans, for IRAS Band 1 (12µm). For individual scans, +/-60.0 arcmin is used for the local background range, for all bands. |
| bg_fit2 | Valid range: 1.0 to 60.0 arcmin | 30.0 | The outer distance from center (in arcmin) to be used in background fits for coadd scans, for IRAS Band 2 (25µm). For individual scans, +/-60.0 arcmin is used for the local background range, for all bands. |
| bg_fit3 | Valid range: 1.0 to 60.0 arcmin | 30.0 | The outer distance from center (in arcmin) to be used in background fits for coadd scans, for IRAS Band 3 (60µm). For individual scans, +/-60.0 arcmin is used for the local background range, for all bands. |
| bg_fit4 | Valid range: 1.0 to 60.0 arcmin | 30.0 | The outer distance from center (in arcmin) to be used in background fits for coadd scans, for IRAS Band 4 (100µm). For individual scans, +/-60.0 arcmin is used for the local background range, for all bands. |
| srcex_fit1 | Valid range: 1.0 to 30.0 arcmin | 2.0 | The inner distance from center (in arcmin) to be used in defining the region to be excluded from the background fit, for IRAS Band 1 (12µm). This parameter must be at least as large as the "Source Fitting Range" (src_fit1 parameter), per band. |
| srcex_fit2 | Valid range: 1.0 to 30.0 arcmin | 2.0 | The inner distance from center (in arcmin) to be used in defining the region to be excluded from the background fit, for IRAS Band 2 (25µm). This parameter must be at least as large as the "Source Fitting Range" (src_fit2 parameter), per band. |
| srcex_fit3 | Valid range: 1.0 to 30.0 arcmin | 4.0 | The inner distance from center (in arcmin) to be used in defining the region to be excluded from the background fit, for IRAS Band 3 (60µm). This parameter must be at least as large as the "Source Fitting Range" (src_fit3 parameter), per band. |
| srcex_fit4 | Valid range: 1.0 to 30.0 arcmin | 6.0 | The inner distance from center (in arcmin) to be used in defining the region to be excluded from the background fit, for IRAS Band 4 (100µm). This parameter must be at least as large as the "Source Fitting Range" (src_fit4 parameter), per band. |
| disp1 | Valid range: 1 to 60 arcmin | 12.0 | This parameter allows the user to change the x-axis range of display (in arcmin), for IRAS Band 1 (12µm) plotting. This parameter setting must be ≤ "Local Background Fitting Range" (bg_fit1 parameter), per band. |
| disp2 | Valid range: 1 to 60 arcmin | 12.0 | This parameter allows the user to change the x-axis range of display (in arcmin), for IRAS Band 2 (25µm) plotting. This parameter setting must be ≤ "Local Background Fitting Range" (bg_fit2 parameter), per band. |
| disp3 | Valid range: 1 to 60 arcmin | 20.0 | This parameter allows the user to change the x-axis range of display (in arcmin), for IRAS Band 3 (60µm) plotting. This parameter setting must be ≤ "Local Background Fitting Range" (bg_fit3 parameter), per band. |
| disp4 | Valid range: 1 to 60 arcmin | 26.0 | This parameter allows the user to change the x-axis range of display (in arcmin), for IRAS Band 4 (100µm) plotting. This parameter setting must be ≤ "Local Background Fitting Range" (bg_fit4 parameter), per band. |
| extra | 0 or 1 (0 = off; 1 = on) | 0 | Turn on/off the access to all the intermediate steps plotted on one summary page. Note that setting this parameter to "on" (value of 1) triples the processing time to approximately 30 seconds per source. |

 Examples Introduction Input Parameters XML Output Description of XML Tags 

 Examples are given below using a combination of parameters. The rest of the parameters are varied to show as examples. The same example is given twice, once for HTTP results and once for XML results(mode=PI). Valid input locations are used for each dataset. Listed at the very bottom of the examples are a few which show error conditions (bad input) and warnings of no data found at a specified location. 

 Note: The following examples can be run by clicking their links. 

1. Source: M31, default parameters (HTTP results) nph-scanpi?locstr=M31&band1=12um&band2=25um&band3=60um&band4=100um Searched at location of source name "M31" [locstr]; perform fitting for all IRAS bands [band1=12um, band2=25um, band3=60um, band4=100um); mode is not set (HTTP output). Source: M31, default parameters (XML results) nph-scanpi?locstr=M31&band1=12um&band2=25um&band3=60um&band4=100um&mode=PI The same parameters apply as above but the mode is set to Program Interface (PI). 
2. Source: arp220, bands 1 & 4, default parameters (HTTP results) nph-scanpi?locstr=arp220&band1=12um&band4=100um Searched at location of source name "arp220" [locstr]; perform fitting for IRAS bands 1 & 4 (band1=12um, band4=100um); mode is not set (HTTP output). Source: arp220, bands 1 & 4, default parameters (XML results) nph-scanpi?locstr=arp220&band1=12um&band4=100um&mode=PI The same parameters apply as above but the mode is set to Program Interface (PI). 
3. Source: arp160, bands 1 & 2, changing optional parameters (HTTP results) nph-scanpi?locstr=arp160&band1=12um&band2=25um&det_distance=2.0&src_fit1=1.5&src_fit2=1.6&bg_fit1=20&bg_fit2=24&disp2=14 Searched at location of source name "arp160" [locstr]; perform fitting for IRAS bands 1 & 2 [band1=12um, band2=25um]; Maximum Allowable Distance From Detector Center is 2.0 [det_distance]; Source Fitting Range for Band 1 is 1.5 arcmin [src_fit1=1.5] and for Band 2 is 1.6 arcmin [src_fit2=1.6]; Local Background Fitting Range for Band 1 is 20 arcmin [bg_fit1=20] and for Band 2 is 24 arcmin [bg_fit2=24]; display plotting of Band 2 fits out to 14 arcmin [disp2=14]; mode is not set (HTTP output). Source: arp160, bands 1 & 2, changing optional parameters (XML results) nph-scanpi?locstr=arp160&band1=12um&band2=25um&det_distance=2.0&src_fit1=1.5&src_fit2=1.6&bg_fit1=20&bg_fit2=24&disp2=14&mode=PI The same parameters apply as above but the mode is set to Program Interface (PI). 
4. Source Location: 229.64063 +2.08269 Eq., band 1 only, changing optional parameters (HTTP results) nph-scanpi?locstr=229.64063+%2B2.08269+Eq.&det_distance=1.9&band1=12um&src_fit1=1.7&bg_fit1=18&srcex_fit1=1.8&disp1=12.0&extra=1 Searched at location "229.64063 +2.08269 Eq." [locstr]; perform fitting for only IRAS band 1 [band1=12um]; Maximum Allowable Distance From Detector Center is 1.9 [det_distance=1.9]; Source Fitting Range for Band 1 is 1.7 arcmin [src_fit1=1.5]; Local Background Fitting Range for Band 1 is 18 arcmin [bg_fit1=18]; display plotting of Band 1 fits out to 12 arcmin [disp1=12]; show plots of Intermediate Steps on the results pages [extra=1]; mode is not set (HTTP output). Source Location: 229.64063 +2.08269 Eq., band 1 only, changing optional parameters (XML results) nph-scanpi?locstr=229.64063+%2B2.08269+Eq.&det_distance=1.9&band1=12um&src_fit1=1.7&bg_fit1=18&srcex_fit1=1.8&disp1=12.0&extra=1&mode=PI The same parameters apply as above but the mode is set to Program Interface (PI). 
5. Source: "none" (to cause an error condition), default parameters (HTTP results) nph-scanpi?locstr=none&band1=12um&band2=25um&band3=60um&band4=100um Searched for bigu source name "none" [locstr]; perform fitting for all IRAS bands [band1=12um, band2=25um, band3=60um, band4=100um); mode is not set (HTTP output). This example is to show an error condition for HTTP results. Source: "none" (to cause an error condition), default parameters (XML results) nph-scanpi?locstr=none&band1=12um&band2=25um&band3=60um&band4=100um&mode=PI The same parameters apply as above but the mode is set to Program Interface (PI). This example is to show an error condition for XML results. Additional example XML results of errors are given below. 

 XML Output Introduction Input Parameters Examples Description of XML Tags 

 Normally, when you run a web application, the return is HTML text which is rendered in a browser and contains links to download additional data files. However, HTML is notoriously difficult to parse, so in program mode we instead return a simple XML document. This document can be rendered in a browser but the normal use pattern is as follows: have your program make an HTTP request using the above parameters; retrieve the XML result into a file (or memory); parse it; extract links to the desired final data files; and use these links (again from your program) to retrieve the data. 

 The interaction above can be done in a variety of ways, ranging from simple scripting (using programs like 'wget') to integrated URL-access and XML-parsing in JAVA, PERL, Python, etc. Our XML is simple enough that if you do not have XML-parsing tools, simple pattern checking (using manually built shell code or tools like PERL) should suffice. 

 The returned XML "inventory" contains links - URLs you can use to download data files from a temporary workspace. Also available is a 'wget' script which is provided as a convenience for people who want to use that mechanism for bulk data downloads. 

 Below, we give example XML output for three of the use cases above. The first block is from Example 3 above (a normal return), the second is an example error return (using a bogus coordinate locstr value of "bla") and the third is an example of a notication that no sources were found for a valid position. After these examples, we will enumerate all the tags that might be returned by a successful query. These examples vary only in the input constraints; their XML outputs are similar in layout with varying number of bands requested for fitting. 

 Note: In the real XML files, all this is just text. Here we have turned some of this text into links so you can see examples of the result files. Also note that results files are for example visualization purposes; since these are not actual search results for iterative fitting, some links within the results file examples will not work. 

 Output from Example 3: 

```
 
    <?xml version="1.0"?>
    <result status="ok">
      <description> 
        <ra>  233.194920 </ra> 
        <dec> 23.668890 </dec> 
        <userInput> arp160</userInput> 
      </description>
      <summary>
        <resultHtml>
            https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/index_results.html 
        </resultHtml>
        <workspace>
            https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/ 
        </workspace>
        <README>
            https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/README 
        </README>
        <logfileTXT>
            https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/logfile.txt 
        </logfileTXT>
        <summaryHTML>
            https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/summary.html 
        </summaryHTML>
        <band1_summary>
           <summaryHTML>
               https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/b1_summary.html 
           </summaryHTML>
           <summaryTBL>
               https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/b1_summary.tbl 
           </summaryTBL>
           <workspace>
               https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/b1/ 
           </workspace>
           <srcfit_coadd_plot>
               https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/b1_srcfit_coadd_sm.jpg 
           </srcfit_coadd_plot>
        </band1_summary>
        <band2_summary>
           <summaryHTML>
               https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/b2_summary.html 
           </summaryHTML>
           <summaryTBL>
               https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/b2_summary.tbl 
           </summaryTBL>
           <workspace>
               https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/b2/ 
           </workspace>
           <srcfit_coadd_plot>
               https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/b2_srcfit_coadd_sm.jpg 
           </srcfit_coadd_plot>
        </band2_summary>
        <downloadScript>
            https://irsa.ipac.caltech.edu/workspace/TMP_AAAylaqUG/Scanpi/arp160.v0001/wget_data.bat 
        </downloadScript>
      </summary>
    </result> 
  
```

 Output with an error condition: 

```
 
    <?xml version="1.0"?>
    <result status="error">
      <message>
      Coordinate lookup error: Invalid object name.
      </message>
    </result>
  
```

 Output with a error that no sources were found for requested position: 

```
 
    <?xml version="1.0"?>
    <result status="error">
      <message>
      ERROR: No IRAS scans available at that location (most likely on an IRAS Gap).
      </message>
    </result>
  
```

 Description of XML Tags Introduction Input Parameters Examples XML Output 

 The structure of the XML file is straightforward and is fully illustrated by the above examples; we do not feel it necessary to provide formal schema information. We may add information to the XML as needed, though we will make every effort not to change the existing tag structure in the process. 

| Tag name | description |
| --- | --- |
| result | This is the top tag of the XML file, it contains a variable "status" indicating whether the query is successful: "ok" for successul query, "error" indicating that something went wrong during the query or if the requested position had no results. |
| message | This tag contains the error message when the query status = "error". |
| description | This series of tags contain input parameter information regarding the user input query and location of the search. |
| ra | The Right Ascension of the requested search, in decimal degrees [J2000] |
| dec | The Declination of the requested search, in decimal degrees [J2000] |
| summary | Overall summary of coadd scans (initial Scanpi output web page). |
| resultHtml | An HTML page that contains the entire set of search results in a summary for coadd scans, with plotting and tabular summary information, as well as links for more detailed results. |
| workspace | The directory location of the workspace which was used to store all result files, intermediate files and any associated material for that query. |
| README | A simple ASCII text file which describes each results file in the "workspace" of a Scanpi run. |
| logfileTXT | A simple ASCII text file which lists all the fitting parameters for all Scanpi individual scans as well as coadd scans. |
| summaryHTML | An HTML page that contains the entire set of search results per band, listing individual scans as well as coadd scans. |
| band1_summary | Subset summary section for individual and coadd scans for IRAS Band 1 (12µm), when requested. |
| summaryHTML | An HTML page that contains the Band 1 set of fitting results, listing individual scans as well as coadd scans. |
| summaryTBL | An IPAC Table version of summaryHTML that contains the Band 1 set of fitting results, listing individual scans as well as coadd scans. |
| workspace | The directory location of the workspace which was used to store all result files, intermediate files and any associated material for that query, specifically for IRAS Band 1. |
| srcfit_coadd_plot | Plot of all coadd scans, fits and background fits, for IRAS Band 1. |
| band2_summary | Subset summary section for individual and coadd scans for IRAS Band 2 (25µm), when requested. |
| summaryHTML | An HTML page that contains the Band 2 set of fitting results, listing individual scans as well as coadd scans. |
| summaryTBL | An IPAC Table version of summaryHTML that contains the Band 2 set of fitting results, listing individual scans as well as coadd scans. |
| workspace | The directory location of the workspace which was used to store all result files, intermediate files and any associated material for that query, specifically for IRAS Band 2. |
| srcfit_coadd_plot | Plot of all coadd scans, fits and background fits, for IRAS Band 2. |
| band3_summary | Subset summary section for individual and coadd scans for IRAS Band 3 (60µm), when requested. |
| summaryHTML | An HTML page that contains the Band 3 set of fitting results, listing individual scans as well as coadd scans. |
| summaryTBL | An IPAC Table version of summaryHTML that contains the Band 3 set of fitting results, listing individual scans as well as coadd scans. |
| workspace | The directory location of the workspace which was used to store all result files, intermediate files and any associated material for that query, specifically for IRAS Band 3. |
| srcfit_coadd_plot | Plot of all coadd scans, fits and background fits, for IRAS Band 3. |
| band4_summary | Subset summary section for individual and coadd scans for IRAS Band 4 (100µm), when requested. |
| summaryHTML | An HTML page that contains the Band 4 set of fitting results, listing individual scans as well as coadd scans. |
| summaryTBL | An IPAC Table version of summaryHTML that contains the Band 4 set of fitting results, listing individual scans as well as coadd scans. |
| workspace | The directory location of the workspace which was used to store all result files, intermediate files and any associated material for that query, specifically for IRAS Band 4. |
| srcfit_coadd_plot | Plot of all coadd scans, fits and background fits, for IRAS Band 4. |
| downloadScript | A link to a script (file) which contains bulk download instructions using the unix tool "wget" to download all the search results for all requested bands. |
