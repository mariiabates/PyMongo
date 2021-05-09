A command line implementation of an application to query a MongoDB database. 

## Architecture
I deployed a Free Tier Cluster, populated a database with The UK election data (add description) and installed PyMongo to communicate with the database from Python.  
The application is developed in a functional programming style with each query representing a function. 
Queries are written as MongoDB aggregation pipelines.

### Interesting features
- I do not print the queries as a long string, but use f-strings with function docstrings.
- I manage the user input using the EAFP principle (_Easier to ask for forgiveness than permission_) with `try except` blocks instead of `if else`.
- Notice how I pass the user input to functions in a uniform way and how I deal with functions requiring additional parameters.
- Notice how I deal with functions' return values in a uniform way: either iterating the cursor or printing a single row.

## Instructions
`PyMongo` should be installed.   

When you start the application, you will see a list of 6 possible queries to run and a prompt to choose a query:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_Enter a query number (see above): ._

Enter a single number and hit Enter.   
N.B. You will see the same question again if the input is not valid (not a number or beyond the range of available queries).  

For some queries you might be asked to enter additional parameters. 
For example:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_This query requires you to enter a party: ._   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_This query requires you to enter a constituency area: ._   
Enter a single word and hit Enter.  
N.B. For such queries, it is assumed you know short names for constituencies or parties ('con', 'lab', 'eco' etc) as they are presented in a db. 
If the input does not match records, you will see a message _No records found..._ 

If everything is correct, you will see the result of your query on the command line.
