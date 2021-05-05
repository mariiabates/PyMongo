## Instructions
Run the application as a normal python file (`PyMongo` should be already installed).   

You will see a list of 6 possible queries to run and a prompt to enter a query number from 1 to 6:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_Enter a query number (see above): ._

Enter a single number and hit Enter.   
N.B. There is an additional check to validate user input. You might see the same question again if the input is not a number or beyond the range of available queries.  

For some queries you might be asked to enter additional parameters. 
For example:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_This query requires you to enter a party: ._   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_This query requires you to enter a constituency area: ._   
Enter a single word and hit Enter.  
N.B. For such queries, it is assumed you know short names for the parties ('con', 'lab', 'eco' etc) and areas as they are presented in a db. 
If the input does not match records, you will see a message _No records found..._ 

If everything is correct, you will see the result of your query on the command line.

## Architecture
I deployed a Free Tier Cluster, populated a database with The UK election data (add description) and installed PyMongo to communicate with the database from Python.  
The application is developed in a functional programming style with each query representing a function. 
Queries are written as MongoDB aggregation pipelines.

### Interesting features
- Notice how I do not print the queries to a user as a text, but return them as docstrings from functions.
- Notice how I manage user input in an EAFP style (_Easier to ask for forgiveness than permission_) using `try except` block instead of `if`.
- Notice how I deal with some functions requiring additional parameters directly mapping query numbers to appropriate function calls.
- Notice how I deal with printing results of the queries in a uniform style: if a cursor was returned, I iterate the cursor printing line by line; if a single row was returned, I print a line.
