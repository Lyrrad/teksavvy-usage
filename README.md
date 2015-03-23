TekSavvy Usage Checker
==========================


This is a simple checker to check your usage from TekSavvy from the past three calendar months.  It lists the On and Off Peak upload and download information from TekSavvy's API.  This requires an API key from your account.  See [here](http://www.dslreports.com/forum/r29122264-Portal-MYACCOUNT-API-KEY-MANAGEMENT) for details on how to generate the key.

Options: 

-a, --apikey: Pass in API key from TekSavvy.  If one is not given, it will try to load it from the configuration file.
-s, --save: Save given API key in file.  

Notes:

* Requires requests module.