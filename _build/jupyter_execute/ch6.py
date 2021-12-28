#!/usr/bin/env python
# coding: utf-8

# # Creating and Connecting to Databases

# ```{contents} Table of Contents
# :depth: 4
# ```

# ## Introduction: What is a Database?
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/tidy.jpg" width="500" >
# 
# A database is an organized collection of many data records, whether those records are tables, JSON, or another format. If a single data record is a book, then a database is a library: the library contains many books, which are organized according to some system such as alphabetical order or the Dewey Decimal System. Databases, if they are carefully organized and well-maintained, allow big organizations to keep track of huge amounts data and access specific data quickly. Databases also make security easier: by storing all the data together inside a database, it is also easier to use encryption, credentials, and other security measures to control who has access to what data inside the database. Databases can exist locally, on your own computer's hard drive for example, or on remote servers that anyone with an internet connection and the right credentials can access.

# ### Querying a Database vs. Using an API
# As a data scientist, you will frequently have to issue requests to remote databases to get the data you need. These requests are called **queries**. We've already discussed sending queries to a database in Module 4 through APIs, but here we will focus on situations in which no API is available. Remember that an API is code that takes a request as input, translates that request to language the database can understand, and returns the requested data subject to the API's restrictions and security measures. A REST API requires client-server separation, and that allows database managers to make changes to a database without requiring front end users to change their code for issuing a query because the API does that translation on behalf of the user. So if a remote database has an API, the database managers intend for users to make queries through that API, and not to query the database directly.
# 
# If there is no API, users will have to pay close attention to how the database is organized to query the database correctly. The specific way in which a database is organized is called the **schema**. If the database managers change the schema for any reason, users will need to change their queries to work with the new schema. 
# 
# Both APIs and direct queries can include security measures, but APIs allow more nuanced security. For example, an API can be used to keep track of how much data is being requested and how many calls have been issued and block users that exceed pre-set limits. A database without an API can require a username and password to grant or deny access to the data, but cannot in general place restrictions on the extent of use the way APIs can.

# ### Atomicity, Consistency, Isolation, Durability (ACID)
# The purpose of a database is to store data and make sure that data can always be transferred to approved applications. A transfer of data is called a **transaction**, and a transaction is considered valid if it meets four criteria - atomicity, consistency, isolation, and durability - that were first described by [Theo Haerder and Andreas Reuter in 1983](https://dl.acm.org/doi/10.1145/289.291):
# 
# * Atomicity: one transaction might require many actions to be run in sequence. For example, making a credit card purchase involves five steps:
#     1. The customer swipes the card and approves the purchase
#     2. The vendor's card reader communicates the payment information to the vendor's bank 
#     3. The vendor's bank communicates with the credit card issuer 
#     4. The issuer either declines or approves and pays the request and sends this information to the bank
#     5. The bank communicates the result to the vendor 
#   
#   Atomicity says that all of these steps should be considered part of a single transaction. The transaction is successful if and only if all five steps are successful, and the transaction fails if any of these steps fail. In the case of a credit card purchase, that means that if the credit card issuer pays the bank, but the bank fails to transfer that payment to the vendor, then the entire transaction fails and the issuer's payment to the bank is cancelled: that prevents situations where people disagree about who did or did not pay.
# 
# * Consistency: the result of a transaction is not allowed to invalidate the data that already exists in the database. If there is an error that causes an invalid datapoint to be transmitted to the database, the entire transaction is cancelled. Consistency also means that no data should contradict other data. For example, if a customer's account is debited by some amount, it might take some time for the transaction to be communicated to both the bank and the credit card company. A transaction is not considered complete until the record of the customer's account balance is updated in every system. It might take longer to complete a transaction this way, but this step ensures that there's no possibility of problems due to different systems having different balances for the same account.
# 
# * Isolation: if there are many transactions issued to the same database in a short period of time, one transaction must be fully completed before the next transaction is processed. That ensures that the information available in the database for each transaction is the most up-to-date.
# 
# * Durability: once a transaction has been made, the record of that transaction cannot be erased, even if the system experiences a hardware failure such as a power outage.
# 
# The ACID criteria are standards that well-maintained databases need to achieve, regardless of how the data are organized, stored, and used.

# ### A Brief History of Databases
# According to [Kristi L. Berg, Tom Seymour, and Richa Goel (2013, p. 29)](https://doi.org/10.19030/ijmis.v17i1.7587):
# 
# > The origins of the database go back to libraries, governmental, business and medical records before the computers were invented. . . . Once people realized they needed to have the means to store data and maintain the data files for later retrieval, they were trying to find ways to store, index, and retrieve data. With the emergence of computers, the world of the database changed rapidly, making it an easy, cost effective, and less space-consuming task to collect and maintain the database.
# 
# While physical database systems date back to ancient times, electronic databases were invented in the 1960s to work with the first computers capable of using disk storage. The first databases emphasized storage over the content of the data. The focus was to find sufficient physicial storage for a large number of records with the same fields and different values for those fields. As the early concerns revolved around physical storage, the icon for a database resembles physical disk storage. You've probably seen some representation of this icon to represent a database:
# 
# <img src="https://blog.learningtree.com/wp-content/uploads/2016/02/database-152091_640.png" width="200">
# 
# To be specific, this standard database icon is a picture of a [drum memory](https://stackoverflow.com/questions/2822650/why-is-a-database-always-represented-with-a-cylinder) data storage device, which was [invented in 1932](https://en.wikipedia.org/wiki/Drum_memory) and predates disk drives. Here's a picture of a drum memory that would have been used in the 1950s:
# 
# <img src="https://upload.wikimedia.org/wikipedia/commons/d/d2/Pamiec_bebnowa_1.jpg" width="200">
# 
# From the 1960s onward, new database types were developed to match the needs of businesses as data and databases gained increased use in industry and government. In the 1970s the invention of the relational database structure allowed users to query a database for records with specific content. Relational databases also enabled more stringent data validation standards - certain fields could only be populated by values with specific data types - and allowed database managers to add new features without having to go back and revise every record in the database. In the 1980s and 1990s, the relational framework was extended to work with object-oriented programming languages and with web-based applications such as APIs. More recent innovations in database structures respond to the greater need for databases to store massive amounts of data, the need to use distributed storage and cloud computing, and the proliferation of data in which records exist in an interconnected network or come from real-time streaming. The following table summarizes these innovations:
# 
# | Timeframe   | Database Need                                       | New Type of Database   | 
# |:-------------|:-----------------------------------------------------|:--------------|
# | 1960s       | Store data and page through records                 | Navigational | 
# | 1970s-1980s | Search/filter based on the content of records; add new features without having to revise all records in the database | Relational   |
# | 1980s | Work with object oriented programming languages | Object Oriented |
# | 1990s | Use internet connectivity to create client-server systems and APIs | Web-Enabled Relational | 
# | 2000s | Huge data storage memory requirements; need for flexible schema | NoSQL Databases| 
# | 2010s | Host databases on distributed systems using cloud computing | Databases with cloud functionality| 
# | 2010s-2020s | Store data in which records link to each other in a network | Graph databases | 
# | 2010s-2020s | Store data in which records come from a streaming time series | Time series databases | 
# 
# A **database management system** (DBMS) is software that allows users create, revise, or delete records in a database, generate security protocols, or issue queries to obtain a selection of the data. Every innovation in database structure and functionality brought about the creation of new DMBSs. People sometimes muddle the terminology and refer to a database, its schema, and a DBMS interchangably: it's not uncommon to hear people speak about a "MySQL database" when it would be more accurate to describe "a database with a relational schema managed using the MySQL DBMS". In addition, there has been a huge proliferation in DBMSs, and people can spend a lot of time debating competiting DBMSs that are only marginally different from each other. That can be frustrating to new coders who are trying to find the "right" or "best" DBMS, and many people have had the experience of finally mastering one DBMS only to be told that its been replaced by a new one. It is important to understand your options when it comes to choosing a database type and a DBMS,  but it is also important to understand which distinctions are major and which are minor.

# ## Types of Databases
# As described in the previous section, electronic databases have evolved a great deal since the 1960s to increase the functionality of working with data, to handle new kinds of data, and manage bigger and bigger amounts of data. If you intend to create a database, the first decision you need to make is what type of database are you going to create. If you are going to work with an existing database, knowing what type of database you are working with will guide you to the correct methods for issuing queries to this database.
# 
# To illustrate the differences between types of database, consider the following (fake) data, based on data on books checked out from the Jefferson-Madison Regional Library (https://www.jmrl.org/), a network of public libraries that serves Charlottesville and the surrounding region. In this data table, rows represent individual books checked out by particular patrons, every library patron has a unique library card number, every book has a title and at least one author, the checkout dates are recorded but the return dates are `NULL` if the book is still checked out, and the librarian who conducted the transaction is included along with library branch where they work:
# 
# | CardNum | Patron            | Book                                                                                                       | Checkout | Return   | Librarian          | Branch          |
# |:---------|:-------------------|:------------------------------------------------------------------------------------------------------------|:----------|:----------|:--------------------|:-----------------|
# | 18473   | Ernesto Hanna     | [A Brief History of Time, Stephen Hawking]                                                                 | 8/20/19  | 9/3/19   | José María Chantal | Charlottesville |
# | 29001   | Lakshmi Euripides | [Love in the Time of Cholera, Gabriel Garcia Marquez]                                                      | 11/23/19 | 12/14/19 | José María Chantal | Charlottesville |
# | 29001   | Lakshmi Euripides | [Anne of Green Gables, L.M. Montgomery]                                                                    | 1/7/20   | 2/3/20   | Antony Yusif       | Charlottesville |
# | 29001   | Lakshmi Euripides | [The Master and Margarita, Mikhail Bulgakov]                                                               | 4/2/20   | NULL     | Antony Yusif       | Charlottesville |
# | 73498   | Pia Galchobhar    | [Freakonomics: A Rogue Economist Explores the Hidden Side of Everything, Steven Levitt, Stephen J. Dubner] | 3/2/20   | 3/20/20  | Dominicus Mansoor  | Crozet          |
# | 73498   | Pia Galchobhar    | [Moneyball: The Art of Winning an Unfair Game, Michael Lewis]                                              | 3/24/20  | NULL     | Antony Yusif       | Charlottesville |
# 
# This table contains all of the data. However, this representation of the data is not the way any of the commonly used database schemas organize the data.

# ### Navigational Databases
# Early databases treated records as equivalent units, stored in sequential order, like pages in a book. Patient records at a hospital, for example, could all be stored in a database, and an individual patient's data could be extracted by flipping through the records until the patient's data appears. Navigational databases also allow records to link to other records based on common features, such as patients who see the same doctor. 
# 
# If the library data is stored in a navigational database, one record might appear on a librarian's computer screen like this:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/navigational.png" width="600">
# 
# Notice that only one record appears on the screen, but there are links to the previous and next records in the database, along with the previous or next records for this patron or that occurred at this branch.
# 
# The major drawback of navigational database systems is that there is no way to perform a search other than moving through the links, which is time consumming and computationally inefficient. Navigational databases cannot filter data based on the content of a record, so there's no way to see all the times a book by Gabriel Garcia Marquez was checked out, for example. While the early history of databases was dominated by navigational types, and while this type of database still gets used in some applications, most databases no longer use this structure.

# ### Relational Databases
# The relational database structure was first proposed by [E. F. Codd in 1970](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf). He describes the motivation for a relational database model as follows (p. 377):
# 
# > The relational view (or model) of data . . . appears to be superior in several respects to the [navigational] model presently in vogue for non-inferential systems. It provides a means of describing data with its natural structure only - that is, without superimposing any additional structure for machine representation purposes. Accordingly, it provides a basis for a high level data language which will yield maximal independence between programs on the one hand and machine representation and organization of data on the other.
# 
# In other words, relational databases do not have to rely on a pre-set ordering or indexing of the records. There should be no intrinsic meaning to the order of the rows or the order of the columns. That way, to find specific data, a user only needs to search for that data and does not need to lookup the location of the data in an index. 
# 
# Codd also describes a further advantage of the relational schema: "it forms a sound basis for treating derivability, redundancy, and consistency of relations" (p. 377):
# 
# * Derivability refers to an ability to use a set of operations to pinpoint a desired selection of the data; that is, we can use queries that operate on the quantities in the data to extract exactly the data we need. If we wanted data on all books checked out from the Crozet branch in February that had more than one author, we can specify a query to return that dataset. 
# 
# * Redundancy refers to the fact that some of the information in a data table is implied by other features, and therefore takes up more space than it needs to. For example, in the library data shown above, it's redundant to list "Charlottesville" over and over for every row in which the librarian is Antony Yusif because each librarian works at only one branch. If we know the librarian, we can lookup the branch where that librarian works in a separate table, and separating the data into two tables will reduce the overall amount of memory needed to store the data. 
# 
# * Consistency refers to the possibility of contradictions within the data. If someone updates the data one record at a time, then it is possible for the person entering the data to make a mistake. For example, I could create another row in the library data that lists Antony Yusif with the Crozet branch, which is a mistake because Antony Yusif works at the Charlottesville branch. Either someone needs to catch and fix this mistake, or else the data now contain contradictory information. The relational database, however, lists librarians with their branches in another table, so there's no opportunity for me to mistakenly input the wrong branch: instead the correct branch is automatically drawn from this second table. 

# #### Relational Database Normalization
# In order for a relational database to provide derivability, redundancy, and consistency, it must be in **normal form**. Database normalization is a series of rules that a collection of data tables within a relational database must follow in order to solve the problems that Codd identified. There are many, progressive versions of normal forms: each version adds more stringent rules, but solves more problems. Here we will discuss three different organization standards called first, second, and third normal form.
# 
# ##### First Normal Form
# To be in first normal form (1NF), data must meet three criteria:
# 
# 1. Every table must have a **primary key**.
# 
# A primary key is one column or a combination of several columns that contain unique identifying values for each row. (A combination of columns that comprise the primary key is sometimes called a [superkey](https://en.wikipedia.org/wiki/Superkey).) This column or combination of columns is called a **foreign key** when used in other tables.
# 
# <ol start="2">
#     <li> The values inside every cell in every table must be <b>atomic</b>.</li>
# </ol>
# 
# That means these values cannot be lists or tuples. Put another way: every individual piece of data must get its own cell. But what constitutes an "individual piece of data"? The answer depends on the context of the data and the purpose of the database. Take for example the `Patron` column in the library data, which contains the patrons' first and last names. Is this column non-atomic? It depends on whether we have a purpose in considering the patrons' first and last names separately. Suppose we run an automated email client that extracts the first names from the database and sends emails to each patron beginning "Dear *firstname*,", then we should break the `Patron` field into first and last names. But if we have no reason to consider the first and last names separately, then breaking this column up is just an unnecessary complication. Atomization is necessary in order for the data to be searchable. If we want to find all books by Stephen Hawking, for example, it helps a great deal for author to be contained in its own column so that we can focus the search on this column. 
# 
# <ol start="3">
#     <li> There are no <b>repeating groups</b>. </li>
# </ol>
# 
# This point is one of the most [confusing and contentious](https://www.red-gate.com/simple-talk/sql/learn-sql-server/facts-and-fallacies-about-first-normal-form/) in the discourse on relational databases because different sources define the notion of "repeating groups" in different ways. Generally speaking, repeating groups are "[a repeating set of columns . . . containing similar kinds of values in a table](https://stackoverflow.com/questions/23194292/normalization-what-does-repeating-groups-mean)." But that's really vague and it can be hard to know from one case to the next whether columns are similar enough to be considered repeating. A better way to think about this rule is as follows: repeated groups are almost always problems that arise immediately after splitting up lists to atomize data. After atomization, answer the following two questions:
# 
#   i. Do we have to arbitrarily put numbers or ordering language into the new columns' names?
#   
#   ii. Does atomizing data and creating new columns generate new missing values?
#   
#   If the answer to either question is yes, then the data have repeating groups. Please note that the second question does not include missing values that already existed in the data prior to atomization.
#   
# The library data is not in 1NF because it fails on the second and third criteria. It passes criterion 1 because `CardNum`, `BookID`, and `Checkout` together comprise the primary key: these columns uniquely identify the rows because one person checks out a specific book only once on a particular day. But the data fail on criterion 2 because `Book` is not atomic: it is populated by lists that contain the books' titles and authors. If we break `Book` up into different columns, like this,
# 
# | Title | First Author | Second Author|
# |:---------|:-------------------|:-------|
# | A Brief History of Time | Stephen Hawking | NULL|
# | Love in the Time of Cholera| Gabriel Garcia Marquez| NULL|
# | Anne of Green Gables| L.M. Montgomery| NULL|
# | The Master and Margarita| Mikhail Bulgakov| NULL|
# | Freakonomics: A Rogue Economist Explores the Hidden Side of Everything| Steven Levitt| Stephen J. Dubner |
# | Moneyball: The Art of Winning an Unfair Game| Michael Lewis| NULL|
# 
# we see that the data also fail to satisfy criterion 3 because we had to include ordering language in names for the columns to store the authors' names. We could have equivalently listed Stephen J. Dubner as the first author of *Freakonomics* and Steven Levitt as the second author, so this placement is arbitrary. In addition, because most of the books do not have a second author, we created a lot of missing values in the `Second Author` column that did not exist in the data before. For both of these reasons, the data contain repeating groups.
# 
# To create a 1NF version of the library data, we replace `Book` with a foreign key. Then we create three new tables: one to contain the book titles, one to contain the author names with an author key, and one to match the books with their authors. We have to create three new tables because listing the authors next to the book title still results in a repeated groups problem.
# 
# The 1NF database has four tables, each called an **entity**, and the columns of each entity are called **attributes**. We generally name the entities after the unit of observation that defines the rows in the table. For our example, we have four entities: 
# <br>
# 
# $$TRANSACTIONS$$ 
# 
# |CardNum | Patron            | BookID                                                                                                       | Checkout | Return   | Librarian          | Branch          |
# |:---------|:-------------------|:------------------------------------------------------------------------------------------------------------|:----------|:----------|:--------------------|:-----------------|
# |18473   | Ernesto Hanna     | 100                                                                 | 8/20/19  | 9/3/19   | José María Chantal | Charlottesville |
# |29001   | Lakshmi Euripides | 101                                                      | 11/23/19 | 12/14/19 | José María Chantal | Charlottesville |
# |29001   | Lakshmi Euripides | 102                                                                    | 1/7/20   | 2/3/20   | Antony Yusif       | Charlottesville |
# |29001   | Lakshmi Euripides | 103                                                               | 4/2/20   | NULL     | Antony Yusif       | Charlottesville |
# |73498   | Pia Galchobhar    | 104 | 3/2/20   | 3/20/20  | Dominicus Mansoor  | Crozet          |
# |73498   | Pia Galchobhar    | 105                                              | 3/24/20  | NULL     | Antony Yusif       | Charlottesville |
# <br>
# 
# $$BOOKS$$
# 
# | BookID | Title |
# |:---------|:-------------------|
# |100 | A Brief History of Time |
# |101 | Love in the Time of Cholera| 
# |102 | Anne of Green Gables| 
# |103 | The Master and Margarita| 
# |104 | Freakonomics: A Rogue Economist Explores the Hidden Side of Everything|
# |105 | Moneyball: The Art of Winning an Unfair Game|
# <br>
# 
# $$AUTHORS$$
# 
# | AuthorID | Author |
# |:---------|:-------------------|
# |500 | Stephen Hawking |
# |501 | Gabriel Garcia Marquez| 
# |502 | L.M. Montgomery| 
# |503 | Mikhail Bulgakov| 
# |504 | Steven Levitt|
# |505 | Stephen J. Dubner|
# |506 | Michael Lewis|
# <br>
# 
# $$AUTHORSHIP$$
# 
# | BookID | AuthorID |
# |:---------|:-------------------|
# |100 | 500 |
# |101 | 501| 
# |102 | 502| 
# |103 | 503| 
# |104 | 504|
# |104 | 505|
# |105 | 506|
# 
# In the TRANSACTIONS entity, `CardNum`, `BookID`, and `Checkout` together comprise is the primary key, and `BookID` is also a foreign key. In the AUTHORSHIP entity, `BookID` and `AuthorID` together comprise the primary key and are individually both foreign keys.

# ##### Second Normal Form 
# Second normal form (2NF) solves more of the problems of Codd identified. When data are organized in second normal form, it helps enforce data consistency by making it harder for new data to be entered that contradicts existing data.
# 
# For data to qualify as being 2NF, it must meet the following criteria:
# 
# 1. The data must meet all the criteria to be 1NF,
# 
# 2. [Wikipedia](https://en.wikipedia.org/wiki/Second_normal_form) lists the second crition for 2NF as:
# 
# > It does not have any non-prime attribute that is functionally dependent on any proper subset of any candidate key of the relation. A non-prime attribute of a relation is an attribute that is not a part of any candidate key of the relation.
# 
# This one is tricky and takes some work to wrap your mind around, so let's discuss what this second criterion means in practical terms. A **candidate key** is the same thing as a primary key - it is one column or a combination of columns whose values uniquely identify the rows of a data table. A **non-prime attribute** is a column within an entity that is not the primary key and is not part of a collection of columns that together construct a primary key. In the TRANSACTIONS table in the library database `CardNum`, `BookID`, and `Checkout` comprise the primary key, and `Patron`, `Return`, `Librarian`, and `Branch` are non-prime attributes. 
# 
# One attribute (X) is **functionally dependent** on another (Y) if the value of Y implies a specific value for X. In other words, X is functionally dependent on Y if changing the value of X does not make sense unless we also change the value of Y. For example, suppose we had ID numbers for individuals in a medical study, and we had also measured the height of each person: height is functionally dependent on the ID because changing height should mean that we are talking about a different person because it makes no sense for one person to have two heights.
# 
# The condition for the data to be 2NF says that all the non-prime attributes need to depend on ALL of the attributes within the primary key, and not just SOME or ONE of them. That means if we change the values of `Patron`, `Return`, `Librarian`, or `Branch`, it should require that we must change `CardNum` and `BookID` and `Checkout`. Suppose we change `Patron`. Every patron has a unique library card number, so `CardNum` should change. But different people can check out the same book, or can check out a book on the same day. That means that `Patron` is functionally dependent `CardNum`, but not on `BookID` or `Checkout`. Because this non-prime attribute only depends on one of the three columns that comprise the primary key, the data are not in 2NF.
# 
# In general, data in 1NF will only fail to conform to 2NF if several columns together comprise the primary key. If the primary key is only one column, then it is not possible for any non-prime attribute to depend on only part of the primary key. The simplest way to revise our data so that it is 2NF is to create a new column called `TransactionID` that alone serves as the primary key:
# <br>
# 
# $$TRANSACTIONS$$ 
# 
# |TransactionID|CardNum | Patron            | BookID                                                                                                       | Checkout | Return   | Librarian          | Branch          |
# |:---|:---------|:-------------------|:------------------------------------------------------------------------------------------------------------|:----------|:----------|:--------------------|:-----------------|
# |1|18473   | Ernesto Hanna     | 100                                                                 | 8/20/19  | 9/3/19   | José María Chantal | Charlottesville |
# |2|29001   | Lakshmi Euripides | 101                                                      | 11/23/19 | 12/14/19 | José María Chantal | Charlottesville |
# |3|29001   | Lakshmi Euripides | 102                                                                    | 1/7/20   | 2/3/20   | Antony Yusif       | Charlottesville |
# |4|29001   | Lakshmi Euripides | 103                                                               | 4/2/20   | NULL     | Antony Yusif       | Charlottesville |
# |5|73498   | Pia Galchobhar    | 104 | 3/2/20   | 3/20/20  | Dominicus Mansoor  | Crozet          |
# |6|73498   | Pia Galchobhar    | 105                                              | 3/24/20  | NULL     | Antony Yusif       | Charlottesville |
# 
# 
# Now all of `CardNum`, `BookID`, `Checkout`, `Patron`, `Return`, `Librarian`, and `Branch` are non-prime attributes, and a change in any of them would imply a new transaction with a new transaction ID, so this entity now conforms to 2NF. Because the other three entities also conform to 2NF, the database is in 2NF.

# ##### Third Normal Form
# After creating `TransactionID`, changing any non-prime attribute will result in changing `TransactionID`. But if we change some non-prime attributes, it should imply that other non-prime attributes need to change as well. If we change the patron's name we are considering a different person, so it should imply a new library card number. In other words, this situation arises because of functional dependence between non-prime attributes. The purpose of third normal form (3NF) is to eliminate the possibility of accidentally invalidating the data by changing some non-prime attributes without also changing the non-prime attributes they are functionally dependent on.
# 
# The criteria for a database to qualify as being in 3NF are:
# 
# 1. All of the criteria necessary for the database to be in 2NF.
# 
# 2. "[Every non-prime attribute . . . is non-transitively dependent on every [attribute]](https://en.wikipedia.org/wiki/Third_normal_form)"
# 
# To understand the second criterion, let's define **transitive dependence**. There are two ways that a non-prime attribute (X) can be functionally dependent on the primary key (Z). X can be directly dependent on Z, or indirectly dependent through a functional dependence on another non-prime attribute (Y) that directly depends on Z. If an attribute depends on another in this indirect way, that is a transistive dependency.
# 
# This condition can only violated if *non-prime attributes depend on one another*. So a simpler and more intuitive way to state the condition is:
# <ol start=2>
#     <li>No non-prime attribute has a functional dependency on another non-prime attribute.</li>
# </ol>
# 
# Our library database is not in 3NF because there are two functional dependencies among the non-prime attributes in the TRANSACTIONS table. First, as described above, `Patron` depends on `CardNum` because changing the patron's name implies a new person, who would have a different library card. Second, `Branch` depends on `Librarian` because changing the branch must imply that there is a different librarian who handled the transaction. Note that `Return` does not depend on `Checkout` because it is possible for a book checked out on a specific day to be returned on different days.
# 
# To convert a database that is in 2NF to 3NF, first find all the non-prime attributes (X) that depend on another non-prime attribute (Y) in the same table. Then replace the Y attributes with foreign keys and remove the X attributes. Finally, create a new entity table for each Y that contains the X that depends on that Y. In the TRANSACTIONS table, `CardNum` can already serve as a foreign key and we replace `Librarian` with `LibrarianID`, while removing `Patron` and `Branch`:
# <br>
# 
# $$TRANSACTIONS$$ 
# 
# |TransactionID|CardNum | BookID                                                                                                       | Checkout | Return   | LibrarianID          | 
# |:---|:-------------|:--------------------------------------------------------------------------------------------------------|:----------|:----------|:--------------------|
# |1|18473   | 100                                                                 | 8/20/19  | 9/3/19   | 31 |
# |2|29001   | 101                                                      | 11/23/19 | 12/14/19 | 31 |
# |3|29001   | 102                                                                    | 1/7/20   | 2/3/20   | 34       |
# |4|29001   | 103                                                               | 4/2/20   | NULL     | 34       |
# |5|73498   | 104 | 3/2/20   | 3/20/20  | 47  |
# |6|73498   | 105        | 3/24/20  | NULL     | 34       |
# 
# 
# We created two new entities for patrons and for librarians:
# <br>
# 
# $$PATRONS$$
# 
# |CardNum|Patron|
# |:---|:---|
# |18473|Ernesto Hanna|
# |29001|Lakshmi Euripides|
# |73498|Pia Galchobhar|
# <br>
# 
# $$LIBRARIANS$$
# 
# |LibrarianID|Librarian|Branch|
# |:---|:---|:---|
# |31|José María Chantal|Charlottesville|
# |34|Antony Yusif|Charlottesville|
# |47|Dominicus Mansoor|Crozet|
# 
# The BOOKS and AUTHORS tables are also in complicance with 3NF because these tables have two attributes: a primary key and a non-prime attribute, so there's no room for transitive dependence. The AUTHORSHIP table contains two attributes which together comprise the primary key and individually are each foreign keys. Because both of these attributes are part of the primary key the 2NF and 3NF restrictions on non-prime attributes do not apply, so this table is also compliant to 3NF. The rest of the 3NF database is:
# <br>
# 
# $$BOOKS$$
# 
# | BookID | Title |
# |:---------|:-------------------|
# |100 | A Brief History of Time |
# |101 | Love in the Time of Cholera| 
# |102 | Anne of Green Gables| 
# |103 | The Master and Margarita| 
# |104 | Freakonomics: A Rogue Economist Explores the Hidden Side of Everything|
# |105 | Moneyball: The Art of Winning an Unfair Game|
# <br>
# 
# $$AUTHORS$$
# 
# | AuthorID | Author |
# |:---------|:-------------------|
# |500 | Stephen Hawking |
# |501 | Gabriel Garcia Marquez| 
# |502 | L.M. Montgomery| 
# |503 | Mikhail Bulgakov| 
# |504 | Steven Levitt|
# |505 | Stephen J. Dubner|
# |506 | Michael Lewis|
# <br>
# 
# $$AUTHORSHIP$$
# 
# | BookID | AuthorID |
# |:---------|:-------------------|
# |100 | 500 |
# |101 | 501| 
# |102 | 502| 
# |103 | 503| 
# |104 | 504|
# |104 | 505|
# |105 | 506|
# 
# It can be difficult to remember the specific criteria that need to be met in order for a database to be in 1NF, 2NF, and 3NF. It helps to remember that for 1NF every data table must include a primary key (even if several columns comprise it), for 2NF every non-prime attribute must depend on the entire primary key, and for 3NF the non-prime attributes must not depend on anything other than the primary key. If it helps you, these three rules are summarized in the following sentence:
# 
# > Give me the key (1NF), the whole key (2NF), and nothing but the key (3NF), so help me Codd.
# 
# There are [many versions of normalization above and beyond 3NF](https://en.wikipedia.org/wiki/Database_normalization#Normal_forms). They are mainly designed to prevent rare anomalies in the data. 

# #### Entity-Relationship Diagrams 
# The process of normalizating a relational database requires separating the data into different tables. While normalization has a number of benefits, the logic of piecing together data as it exists across many different tables can be hard to follow. The best way to communicate the organizational structure (the schema) of a database is through a visualization called **entity-relationship (ER) diagram**.  ER diagrams show how the different tables (entities) in your database are connected to each other through primary and foreign keys, they explain how different tables relate to one another, and they illustrate where every feature in the data is stored. 
# 
# There are three types of ER diagram: the **conceptual model**, the **logical model**, and the **physical model**. These models differ only in the amount of information each one includes in the ER diagram. The conceptual model contains the least amount of information, and generally just shows the entities and the connections between them. The logical model includes the information from the conceptual model, adds the attributes within each entity, and denotes the primary and foreign keys in each entity. The physical model includes all of the information contained in the logical model and adds information about how the data will exist on a computer system, such as the data type for each attribute.
# 
# The problem with ER diagrams, however, is that there are many competing standards for constructing one and there is a great deal of confused language and contradictory terminology surrounding them. The first standard, now usually called **Chen's notation**, was first described by [Peter Pin-Shan Chen in 1976](https://dl.acm.org/doi/10.1145/320434.320440), and uses a flow-chart like system that includes rectangles, ovals, diamonds, and connecting lines to illustrate a database. Today the most commonly used standard, however, is to use **information engineering (IE) notation**, also called **crow's feet notation**. IE notation was first described by [Gordon C. Everest in 1976](https://www.researchgate.net/publication/291448084_BASIC_DATA_STRUCTURE_MODELS_EXPLAINED_WITH_A_COMMON_EXAMPLE), and represents entities as rectangles that contain lists of the attributes inside the entity, with lines connecting the rectangles to show the relationships between entities. Other standard notations for ER diagrams include [Unified Modeling Language (UML) notation](https://www.vertabelo.com/blog/uml-notation/), [Barker's notation](https://www.vertabelo.com/blog/barkers-erd-notation/) for Oracle systems, [Arrow notation](https://www.vertabelo.com/blog/arrow-notation/), and [Integration DEFinition for Information Modeling (IDEF1X) notation](https://www.vertabelo.com/blog/idef1x-notation/).
# 
# No matter what notational standard you use, every ER diagram maps symbols onto the same terminology:
# 
# * **Entity**: A single data table in the relational database. Entities are named after the concept represented in the rows of the table. 
# 
# * **Attribute**: A column within an entity.
# 
# * **Primary identifier attribute**: A single attribute that is an entity's primary key.
# 
# * **Partial identifier attribute**: If a collection of attributes together comprise an entity's primary key, each of these columns is a partial identifier attribute.
# 
# * **Weak entity**: An entity that uses a foreign key as part of its primary key. Conceptually, if an entity uses a foreign key from another entity, the entity cannot exist without the second entity. In our library database, AUTHORSHIP is a weak entity because its key is comprised of `BookID` and `AuthorID`, both of which are foreign keys. That means that the concept of authorship cannot exist without both an author and a book. The relationship (defined below) between a weak entity and the entity with which it shares a key is called a **weak relationship**. However, when a weak entity like AUTHORSHIP is used to resolve a relationship in which many records in one entity match to many records in a second, as with BOOKS and AUTHORS, the entity is also called an **associative entity**, and it might get a different symbol.
# 
# * **Multi-valued attribute**: An attribute in which individual values are lists or tuples that contain many values. Relational databases that contain multi-valued attributes are not in 1NF. In the original library data table, the `Book` column is a multi-valued attribute because it contains lists of the title, the author, and the second author if applicable.
# 
# * **Composite attribute**: An attribute that can be broken up into different columns, but doesn't necessarily have to be separated. In the library database, the patron names can be broken up into the patrons' first names and last names. But we don't have to break up the names if we do not want to be able to extract and search on first name or last name alone.
# 
# * **Derived attribute**: An attribute that is calculated from other attributes in the same entity. For example, in the TRANSACTIONS table in the library database, we could derive an attribute called `DaysCheckedOut` that calculates the number of days between the checkout and return dates.
# 
# * **Relationship**: When an entity contains a foreign key to another entity, there exists a relationship between the two entities. ER diagrams show the link between the two entities and include a few words to describe this relationship in plain-spoken terms. For example, in the library database, the TRANSACTIONS entity contains a foreign link to the PATRONS entity. The relationship between these two entities can be described as TRANSACTIONS "made by" PATRONS. 
# 
# * **Mandatory and optional replationships**: Relationships are spoken about directionally, from the entity that includes a foreign key as an attribute (for clarity, let's call this the "primary entity") to the the entity where that foreign key is the primary key (let's call this the "foreign entity"). A relationship between two entities is mandatory if every record in the primary entity must be matched by at least one record in the foreign entity. A relationship is optional if records in the primary entity do not necessarily have to be matched to any record in the foreign entity. For example, in the library database, the relationship between TRANSACTIONS and BOOKS is mandatory because every transaction must be matched by at least one book - a transaction is defined by checking out one or more books. But suppose the library participates in an inter-library loan program in which patrons can request material from other libraries, and for loaned books we want to collect information about the lendor library. The relationship between BOOKS "from" LENDORS is optional because most books would not be matched to a lendor ID as most books are not obtained through the inter-library loan program.
# 
# * **One-to-one, one-to-many, many-to-one, and many-to-many relationships**: A relationship is one-to-one if every record in the primary entity matches at most one record in the foreign entity. A relationship is one-to-many if one record in the primary entity can match more than one record in the foreign entity. Likewise, a relationship is many-to-one if many records in the primary entity can all match to the same record in the foreign entity. Finally, a relationship is many-to-many if one record in the primary entity can be matched to many records in the foreign entity, and if at the same time many records in the foreign entity can be matched to the same record in the primary entity. 
# 
#     To understand how the relationships in the library database should be categorized, imagine that the database is much bigger, containing several branches, dozens of librarians, and thousands of patrons, books, and authors. In the library database, there are no one-to-one relationships between the entities. In practice, one-to-one relationships are rare in relational databases because we can easily place the attributes from both entities in one table. Suppose we created a new entity called DATES to contain the checkout and return date of each transaction, and that we include `transactionID` as either the primary or foreign key in the DATES entity. Then DATES and TRANSACTIONS would have a one-to-one relationship, although as we see, it is easier to include the checkout and return dates in the TRANSACTIONS table. In contrast, TRANSACTIONS has a many-to-one relationship with PATRONS, LIBRARIANS, and BOOKS: each transaction is  on behalf of one patron, takes out one book, and is conducted by one librarian, but individual patrons can checkout many books, a book may be taken out many times, and librarians conduct many transactions. BOOKS and AUTHORS would have had a many-to-many relationship because individual books can have more than one author and individual authors may write more than one book, but because we created the AUTHORSHIP table to eliminate repeating groups, instead AUTHORSHIP has a many-to-one relationship with both BOOKS and AUTHORS: every instance of authorship maps to exactly one book and one author.
# 
# * **Total and partial participation**: If every record in one entity matches a record in another entity, then the first entity has **total participation** in the second entity. If some records in the entity are not matched in the second entity, the first entity has **partial participation** in the second. Sometimes these ideas are expressed with notation that means records in one entity are matched to "0 or 1" records or "0 or more" records in the second entity.
# 
# * **Specialization and generalization**: Sometimes it is useful to separate the records in one table in the database into groups. For example, in the LIBRARIANS table we can separate the individual librarians into groups based on the library branch where they are employed. We have a choice about how to organize this information. In our example, we included branch as an attribute in the LIBRARIANS entity, which is straightforward and in accordance with 3NL. Alternatively, we could have one table with all of the LIBRARIANS, and other tables named CHARLOTTESVILLE and CROZET that contain only the librarians at each branch. This second approach might be useful if we want to put extra security measures in place to access the data for certain groups. 
# 
#     If we take an entity and assign its records to subgroups, then the original entity is called the **parent** and the subgroup entities are called the **children**. The relationship from the parent to the children is called **specialization** because we move from the full listing of records to a more specific subset of the records, and the relationship from the children to the parent is called **generalization**. If every record can belong to only one subgroup, the children are **disjoint**, and if records can belong to more than one subgroup then the children are **overlapping**. If all records belong to at least one subgroup, then the specialization is **complete**, and if some records do not belong to any subgroups, then the specialization is **partial**.
#     
#     If you have a specific reason for creating entities for subgroups of records, then ER notations have specialized symbols to represent these relationships. But if there's no compelling reason to create subgroups, then it is much simpler to keep all the relevant information together if it still follows normalization rules.

# ##### Chen's Notation
# Chen's notation uses rectangles, ovals, diamonds, and lines to represent the database. The following tables and images come from [Eric Gcc's](https://medium.com/@ericgcc/dont-get-wrong-explained-guide-to-choosing-a-database-design-notation-for-erd-in-a-while-7747925a7531) and [Patrycja Dybka's](https://www.vertabelo.com/blog/chen-erd-notation/) excellent blogs on this subject.
# 
# |||
# |:-|:-|
# |<img src="https://miro.medium.com/max/1400/1*ntrH6a9uRVUKyjmKSP_l8w.jpeg" width="462">|<img src="https://miro.medium.com/max/1400/1*OVukinmawqG_plO-qGkdqQ.jpeg" width="500">|
# 
# Many ER diagrams use the letter **N** instead of **M** to represent "many" in a many-to-one or one-to-many relationship, and use both **N** and **M** for a many-to-many relationship. In addition, an associative entity that is used to match the records of two entities with a many-to-many relationship is represented by a diamond inside a rectangle:
# 
# <img src="https://www.vertabelo.com/blog/chen-erd-notation/chen-notation-associative-entity.png" width="200">
# 
# Associative entities themselves express the relationship between the two entities with the many-to-many relationship, so no relationship diamonds are needed on the lines that connect to associative entities. 
# 
# Sometimes total participation is represented by two lines, and partial participation is represented by one line,
# 
# <img src="https://www.vertabelo.com/blog/chen-erd-notation/chen-notation-participation-constraints.png" width="400">
# 
# and other times all relationships are illustrated with one line when the total/partial distinction is not important. For our example, we will use one line because all relationships are total: every transaction is on behalf of a patron, every transaction is conducted by a librarian, every transaction checks out a book, every book has an author, and every author writes a book.
# 
# To construct a conceptual ER diagram for the library database, we translate the properties of the database into the symbols shown above:
# 
# * The database has five regular entities, TRANSACTIONS, PATRONS, BOOKS, AUTHORS, LIBRARIANS, each of which get a rectangle, and a weak entity AUTHORSHIP which gets a double-layered rectangle.
# 
# * There are many-to-one relationships between TRANSACTIONS "on behalf of" PATRONS, TRANSACTIONS "checkout" BOOKS, TRANSACTIONS "conducted by" LIBRARIANS, which are represented with lines and diamonds, and a many-to-many relationship between BOOKS and AUTHORS via the associative entity AUTHORSHIP, which is represented by a diamond inside a rectangle. The connecting lines are labeled N and 1 for the many-to-one relationships. 
# 
# To create this conceptual ER diagram, I use Draw IO, an open source diagram interface available at https://app.diagrams.net/. I added some color, not because color means anything, but because I think it looks nicer. My conceptual ER diagram for the library database is:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/er1.png" width="900">
# 
# To generate a logical ER, I also add the attributes. Each attribute is represented by an oval with a connecting line to the entity in which that attribute is stored. The primary key in each entity is underlined. Foreign keys do not have to be represented in the ER diagram: when two entities are connected, it is assumed that the foreign keys are included. My logical ER is:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/er2.png" width="900">
# 
# A physical ER includes information to assist the reader in building and maintaining physical storage for the database. One helpful piece of information in this regard is the data type and size of each attribute. Typically, `int(n)` refers to interger values with up to `n` digits, `date` refers to dates, and `varchar(m)` refers to string values with up to `m` characters. This information should be placed close to each attribute so that the data types are clear. My physical ER is:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/er3.png" width="900">

# ##### Information Engineering (IE) Notation
# Chen's notation can very quickly become unwieldy as the number of entities and attributes increases. IE notation is more space efficient, and for that reason, IE notation is the most common notational standard for ER diagrams. The symbols for IE notation are shown in the following tables from [Eric Gcc's blog](https://medium.com/@ericgcc/dont-get-wrong-explained-guide-to-choosing-a-database-design-notation-for-erd-in-a-while-7747925a7531):
# 
# |||
# |:-|:-|
# |<img src="https://miro.medium.com/max/1400/1*RvlQ8GB_HbOa0xm3jw9JwQ.jpeg" width="450">|<img src="https://miro.medium.com/max/1400/1*7WZBJcvLsWPUTAO41iE_Pw.jpeg" width="450">|
# 
# For the most part, Chen's notation and IE notation express the same concepts, with a few exceptions. There's no concept of weak or associative entities in IE notation. Instead, the logical and physical IE models mark the attributes that are primary keys, and explicitly draw lines from entities to the foreign keys they link to. Weak and associative entities will have attributes that are foreign keys for other entities, but will not have a primary key. In addition, in contrast to Chen's notation the relationships are usually not described in words.
# 
# In IE notation, each entity is a box, titled after the name of the entity. The entities that are related are connected by a line. A many-to-one relationship is represented by a line (possibly curved) with the "crow's feet" symbol on one end representing "one or many". The end without the crow's feet represents just one. A conceptual ER diagram in IE notation creates these boxes and connects them, like this:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/er4_2.png" width="600">
# 
# The logical model in IE notation includes the attributes contained within each entity as a list underneath the title of each box. The first attribute should be the primary key. By default, [draw.io](https://app.diagrams.net/) places a horizontal divide after the first item in the list to emphasize that this first item is the primary key. To the left, there's room to write "PK" for further clarification about which attribute is the primary key. (Codes other than PK are allowed here for more complex identification relationships.) The relationship lines should terminate precisely at the location of the foreign key in the related entity. Here's my logical ER diagram in IE notation:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/er5.png" width="600">
# 
# The physical model contains all of the information that exists in the logical model and adds information that is important for the physical storage of the entities. In general, that means that we list the data type next to each attribute, like this:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/er6_2.png" width="600">

# #### Relational Database Management Systems (RDBMS)
# Once a database is up and running, it's time to choose software to handle the four CRUD operations: creating, reading, updating, and deleting records in the database. Issuing a query to the database is the same thing as performing a CRUD operation in which a selection of records is read and arranged in a table that is output by the operation. The software to perform CRUD operations on a relational database is called a relational database management system (RDBMS). 
# 
# If your purpose is to access data stored in an existing database maintained by someone else, an RDBMS has already been chosen to manage how the data can be accessed. All you need to do in that case is learn which RDBMS has been implemented and use an interface for that DBMS to access the data. In general, one database can only work with one DBMS, although some DBMSs like PostgreSQL have built-in [foreign wrappers](https://wiki.postgresql.org/wiki/Foreign_data_wrappers#mysql_fdw) to access data from databases connected to other DBMSs.
# 
# If, however, you are building a new database, the choice of RDBMS is up to you, and this choice can be very confusing. Wikipedia lists [62 distinct DBMSs](https://en.wikipedia.org/wiki/Comparison_of_relational_database_management_systems) for relational databases, and the these RDBMSs mostly overlap in their functionality. For example, all of them implement queries using a coding protocol called the **structured query language** (SQL), which is pronounced either by saying the letters "S-Q-L" or by saying "sequel". SQL is such a universal standard for working with relational databases that the phrases "relational database" and "SQL database" are synonymous, and non-relational databases are commonly called "NoSQL". SQL is a programming langauge that is separate from Python, R, or another environment, but modern RDMBSs make it easy to embed SQL code into standard Python, R, or another coding language's syntax. Although the vast majority of RDBMSs use SQL, many RDBMSs use their own implementations of SQL which can vary in small but important ways from RDBMS to RDBMS. Learning the basics of SQL code is an important topic in and of itself, and it is the focus of Module 7.
# 
# Despite the fact that RDBMSs are very similar, the question of [which RDBMS to use](https://stackoverflow.com/questions/27435/mysql-vs-postgresql-for-web-applications) comes up [again](https://stackoverflow.com/questions/1913547/mysql-vs-sql-server-vs-oracle), and [again](https://stackoverflow.com/questions/9299127/mysql-vs-db2-rdbms), and [again](https://stackoverflow.com/questions/4813890/sqlite-or-mysql-how-to-decide). Given all this confusion, how should you make this decision? First and foremost, it's important to understand that any advice on this question you will find online is a matter of opinion: there's no objectively best RDBMS, so before taking any advice from a blog or Stack Overflow post, please consider the biases of the post's author. Some DBMSs are proprietary, for example, and "advice" articles from these sources might be thinly veiled sales pitches. That said, there are important distinctions between RDBMSs. 
# 
# The biggest distinction is whether the RDBMS is proprietary or open source. This choice is similar to proprietary vs. open source choices in other domains, such as statistical computing, in which privately-owned options like SAS, SPSS, and Stata exist along with open source alternatives like R and Python. Proprietary database management software, like [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server/), [Oracle](https://www.oracle.com/database/), and [IBM DB2](https://www.ibm.com/analytics/db2) offer a lot of features, including cloud computing and storage. Paid licenses for these options also usually come with dedicated support resources, and that makes sense for large enterprise databases that do not want to depend on volunteers to build the framework of the DBMS and will not consult crowd-sourced forums for troubleshooting. But these options can be expensive. Alternatively, open source RDBMSs are free, and are covered under licenses like the [GNU General Public License](https://en.wikipedia.org/wiki/GNU_General_Public_License), which allows users the freedom to run, study, share, and modify the software. It can be argued that open source software cannot be trusted, as it is maintained by volunteers who lack the accountability of paid workers at a large firm like Oracle, Microsoft, or IBM. But there's a compelling argument that open-source software is even more trustworthy than proprietary software because open-source projects generally have [a lot more people checking the source code for errors](https://en.wikipedia.org/wiki/Linus%27s_law) and because software that does not allow users to view the source code can encourage [bad, secretive behaviors](https://www.gnu.org/philosophy/can-you-trust.html) from the software. As of April 2020, open source RDBMSs and proprietary RDBMSs were about [equally popular](https://db-engines.com/en/ranking_osvsc).
# 
# Python and jupyter lab are both open source, and many of the most important tools in data science are open source. So I recommend also using open source options for database management. The three most widely-used open source RDBMSs are 
# 
# ||||
# |:-|:-:|:-|
# | <div style="font-size: 50px">MySQL</div> | <img src="https://upload.wikimedia.org/wikipedia/en/thumb/6/62/MySQL.svg/1200px-MySQL.svg.png" width="200"> | <div style="font-size: 20px">https://www.mysql.com/</div>|
# | <div style="font-size: 50px">SQLite</div>| <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/SQLite370.svg/1200px-SQLite370.svg.png" width="200"> |<div style="font-size: 20px">https://www.sqlite.org/index.html</div>|
# | <div style="font-size: 50px">PostgreSQL</div>| <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1200px-Postgresql_elephant.svg.png" width="150">| <div style="font-size: 20px">https://www.postgresql.org/</div>|
# 
# The following discussion draws heavily on the excellent blog post by ["ostezer" and Mark Drake](https://www.digitalocean.com/community/tutorials/sqlite-vs-mysql-vs-postgresql-a-comparison-of-relational-database-management-systems) that carefully compares the SQlite, MySQL, and PostgreSQL RDBMSs. For more detailed explanations of the differences between the three systems, read their post.
# 
# MySQL (pronounced "my sequel"), SQLite (pronounced "sequel light"), and PostgreSQL (pronounced "post-gress") all have strengths and weaknesses relative to each other, and none of them are unambiguously better than the others. The best approach is to understand what is distinctive about each RDBMS and to choose the system that best suits your particular needs. There are several areas in which these three RDBMSs differ:
# 
# 1. **Local or networked connectivity**: Does the RDBMS work over networked connections, such as cloud storage, or does it only work on databases stored on a local harddrive? If it works over a network, does it depend on a single server? If so, what steps does it take to achieve ACID compliance even when that server goes down for some reason?
# 
# 2. **Size and speed of the software**: How much space does the RDBMS itself take up in local or remote memory? How quickly will the RDBMS process a query?
# 
# 3. **Security**: What procedures are in place to limit which users can access the data?
# 
# 4. **Popularity**: More popular DMBSs will have the bigger communities of developers. Those communities will in general produce better documentation for the software, and will develop more third party extensions for the software.
# 
# 5. **Functionality and SQL compliance**: Functionality refers to the set of tasks that a particular DBMS is able to run, and some DBMSs have abilities that other DBMSs do not. Functionality is in part determined by how much a DBMS complies with the entire SQL coding standard. SQL is a language that exists outside the control of any particular DBMS and the full set of SQL commands and syntax is maintained by the [American National Standards Institute (ANSI)](https://en.wikipedia.org/wiki/ANSI) and the [International Organization for Standardization (ISO)](https://en.wikipedia.org/wiki/ISO). Although most RDMSs use SQL, not every RDBMS implements everything from standard SQL. Some RDBMSs, however, provide new functions that are outside standard SQL.
# 
# The following table describes the strengths and weaknesses of open-source RDBMSs with regard to the considerations listed above:
# 
# |Consideration|MySQL|SQLite|PostgreSQL|
# |:-|:-|:-|:-|
# |Connectivity|MySQL is fully equipped for networks, and it a popular choice for web-applications. However, it can violate ACID protocols when many users are issuing read and write commands at the same time.|Unlike MySQL and PostgreSQL, SQLite does not run a server process, which means that it does not work over networked connections. It works strictly on a local machine. It's a good choice for organizing data for the use of one person, or to support an application that runs locally, but it is not a viable option for sharing data.|PostgreSQL is fuly capable of networked connections and employs advanced techniques to ensure transactions comply with the ACID standards.
# |Size and speed|MySQL has a reputation for being the fastest open source RDBMS.|SQLite is designed to be as lightweight as possible, taking up minimal space in memory. But the space available for storing data is limited by the space available on the local harddrive.| PostgreSQL is generally slower than MySQL (though the differences are often slight or negligable), but it efficiently uses multiple CPUs to handle queries faster.|
# |Security|MySQL allows database owners to manage the credentials and privileges of individual database users.|SQLite is designed for one person to access the data on local storage, so there's no mechanism for allowing different users to have different credentials for accessing the data.|PostgreSQL has all of the security features that MySQL has, and exceeds them in some cases, although there is [debate about whether PostgreSQL or MySQL is more secure](https://stackoverflow.com/questions/6475228/postgresqls-security-compared-to-mysql-etc).|
# |Popularity as of April 2020|MySQL is the [most popular](https://db-engines.com/en/ranking) open source RDBMS, and is the second most popular RDBMS overall.|SQLite is the [6th most popular](https://db-engines.com/en/ranking) open source RDBMS and 9th most popular overall. But it is a popular addition to application software that is deployed on local systems, such as web browsers.|PostgreSQL is the [2nd most popular](https://db-engines.com/en/ranking) open source RDBMS and 4th most popular RDBMS overall. It is also [growing in popularity](https://db-engines.com/en/ranking_trend) more quickly than MySQL or SQLite. There are many third party extensions, just not as many as are available for MySQL right now. While MySQL and SQLite have proprietary elements that sell extensions to the open source base software, PostgreSQL is fully open source.|
# |Functionality|MySQL does not implement the full set of SQL functions in order to boost the speed of queries. Specifically, it cannot perform full joins. But it does have a big community of developers that create extensions.| SQLite implements most of SQL, generally following the functionality of PostgreSQL. SQLite handles fewer data types than MySQL and PostgreSQL.|PostgreSQL implements most of SQL, more than MySQL does, and is designed to work well with object oriented programming languages. It handles more data types than MySQL, including JSON records.| 
# 
# To summarize, SQLite only works on local systems, although it has many advantages for applications that do not require a network connection: it is lightweight and easy to use and initialize. MySQL and PostgreSQL both work well for allowing users to access the data remotely, and can easily set up credentials for individual users to selectively access parts of the database. MySQL is the most popular open source option, and has been for a while, and is still the fastest option although it is missing some of the functionality that is present in universal SQL. PostgreSQL has functionality that is as close as possible to the complete SQL standard. Also, while MySQL remains open source, its development company is now owned by Oracle, which has been spinning off various proprietary extensions to MySQL. In contrast, PostgreSQL and its extensions all remain open source. 

# ### NoSQL Databases
# The term "NoSQL" refers to a database that is not organized according to a relational schema, and therefore cannot use any DBMS that uses SQL. A better name for these schema is "non-relational". NoSQL databases are a recent innovation that have gotten a lot of hype over the last ten years, and it is described in various places as "[modern](https://aws.amazon.com/nosql/)" and "[next generation](https://www.academia.edu/40346447/Next_Generation_Databases_NoSQL_NewSQL_and_Big_Data_-_What_every_professional_needs_to_know_about_the_future_of_databases_in_a_world_of_NoSQL_and_Big_Data_-_Guy_Harrison)". Although the language surrounding NoSQL has only existed since the 2000s, the concept of non-relational databases is as old as databases themselves, as the original navigational schema are be considered versions of NoSQL today. 
# 
# In addition to the key-value store, document store, wide-column store, and graph versions of NoSQL databases described below, there are specialized NoSQL DBMSs for time series data ([influxDB](https://github.com/influxdata/influxdb)), object oriented data stores ([InterSystems Caché](https://www.intersystems.com/products/cache/)), search engines ([Elasticsearch](https://www.elastic.co/elasticsearch/)), Triplestores, Resource Description Framework (RDF), or XML Stores ([MarkLogic](https://www.marklogic.com/)), Multivalue Systems ([Adabas](https://www.softwareag.com/corporate/products/adabas_natural/adabas/default.html)), Event Stores ([Event Store](https://eventstore.com/)), and Content Stores ([Apache Jackrabbit](http://jackrabbit.apache.org/jcr/index.html)).

# #### Comparing NoSQL Databases to Relational Databases
# Some people argue that NoSQL is a replacement for relational databases, but the reality is that NoSQL and relational databases are well-suited for different purposes and both are likely to remain in the standard toolkit of professionals who work with data for a long time. 
# 
# NoSQL differs from relational databases in three ways:
# 
# 1. Unlike relational databases, a NoSQL database allows for a **flexible schema**. 
# 
# The term "flexible schema" does not have a specific definition, but it is generally understood to mean a relaxation of the restrictions that relational databases require. For example, when describing [DynamoDB](https://aws.amazon.com/dynamodb/), a NoSQL DBMS owned by Amazon, Amazon's Chief Technology Officer Werner Vogels [wrote](https://www.allthingsdistributed.com/2012/01/amazon-dynamodb.html):
# 
# > Amazon DynamoDB is an extremely flexible system that does not force its users into a particular data model . . . . DynamoDB tables do not have a fixed schema but instead allow each data item to have any number of attributes, including multi-valued attributes.
# 
# In other words, when we input a record into a NoSQL database, the attributes in the record, the number of attributes, and the data type of each attribute can change from record to record. We alter the structure of the data to match the specific needs of each record. With NoSQL databases we do not have to follow the rules of any normal form, so multi-valued attributes and non-prime and transitive dependencies are fine.
# 
# Relational databases in contrast are very strictly organized. That makes the database easier to use once it is constructed because the ER diagram illustrates where all of the data are stored, and normalization goes a long way towards preventing errors. But in order for a relational database to be worthwhile, there's a lot of work that has to go in to the design and building of the database, and the data that goes into the database must fit within the tightly controlled schema. For example, the library database described earlier is in 3NF. It's easy to add new transactions, patrons, books, authors, or librarians to the data. It's also easy to add new attributes, just so long as they include a key that matches with a primary key in one of the attributes. But it is much more difficult to alter the schema to express the situation in which librarians can work at more than one library branch, or to add items to be checked out that aren't books, or to handle a patron whose library card has expired and is requesting a new card. All of these transactions are records that the library would want to keep track of, and there is nowhere in the relational database as it is currently organized to store these data. We can reorganize the database, but that would be a lot of work if we already have a great deal of data stored. We would also find ourselves in the same position of being unable to process new data every time the library provides a new class of items or another novel situation occurs that the library would want to keep track of. 
# 
# An alternative strategy is to store data in a NoSQL database. We can input a record of a patron using a public computer for 30 minutes into a NoSQL database in JSON format:
# 
# ```
# {cardNum=18473,
# Patron="Ernesto Hanna",
# Service="Public computer use",
# Duration=30,
# Date="04/24/2020"}
# ```
# In practice, relational databases require a lot of work when building the database, but all that work makes it easier to query and work with data once the database has been built. In contrast, NoSQL databases require much less work at the outset because every record may follow its own schema, but that flexibility results in more work being necessary to extract a selection of data and to prepare it to be analyzed.
# 
# <ol start=2>
#     <li>NoSQL databases are easier than relational databases to store on <b>distributed systems</b> by using <b>sharding</b>.</li>
# </ol>
# 
# A distributed system is network of many separate but connected computers or data servers. Sharding is the act of breaking a database into many distinct parts by storing subsets of the database's records in separate, smaller databases, called shards. Once a database has been sharded, it can be stored on a distributed system: instead of placing the entire database into one massive storage device (increasing the capacity of one storage device is called **vertical scaling**), we break the database into shards and store each shard on a different storage device (increasing the number of storage devices is called **horizontal scaling**). 
# 
# It is easier to shard a NoSQL database than it is to shard a relational database. A NoSQL database is a container for many records and does not use different data tables, and that's why it is straightforward to move single NoSQL records in their entirety to new storage. In contrast, a relational database has separate data tables for each entity, and the concept of a record is much fuzzier: given one library transaction, for example, data about that transaction comes from separate tables for the patron, the book, the book's authors, and the librarian. It's not possible to operate on a record in its entirety without first joining all of these tables, and even then, there's ambiguity about what counts as a record (is it a transaction? a patron? a book? an author? or all of the above?). The puzzle of how exactly to shard a relational database makes horizontal scaling much more difficult for relational databases. For startups and other organizations that cannot invest in the infrastructure to store massive databases in a single storage device, building a NoSQL database and sharding is an economical option.
# 
# <ol start=3>
# <li>Unlike relational databases, NoSQL databases do not always follow the [ACID](#acid) standards. Instead, they follow the <b>BASE</b> standards.</li>
# </ol>
# 
# ACID governs how layers of systems involved with one transaction communicate. One of the ACID standards is consistency, which requires that every system has the exact same data. Consistency takes time, as all of the systems need to be updated before a transaction is considered complete. We wait several moments for credit card transactions to process as the various banks and credit card companies sync their data, for example.
# 
# But consistency is sometimes too much of a burden on a data sharing system. Take for example a cloud storage system like Dropbox: when you save a file in the Dropbox folder on your computer, it may take several moments for the file to upload to the Dropbox server and several more moments for the server to sync your data with the other devices that are connected to your Dropbox account. During these moments, the data in your local folder differ from the data on the server, so this transaction does not satisfy the ACID requirements. While Dropbox is syncing your files, you are still able to use those files on your computer despite the fact that those files may be different from the ones on the server. This process works because a Dropbox user is confident that the files will all sync up *eventually*, once Dropbox processes the changes.
# 
# The way Dropbox syncs files does not accord with ACID, but it does meet a different set of standards called called [BASE](https://neo4j.com/blog/acid-vs-base-consistency-models-explained/) (get it? ACID vs BASE), which are:
# 
# * **Basic Availability**: The system should be usable at any given point in time, regardless of how much progress the system has made in syncing data across servers. For Dropbox, that means that a user can still access their files even if they haven't yet been uploaded to the Dropbox server or synced to other devices.
# 
# * **Soft-state**: Because the system is constantly updating and syncing data, at any point in time we do not know the true state of the system.
# 
# * **Eventual consistency**: The system will, given enough time, sync all data to be the same across all the servers connected to the database.
# 
# One advantage of relaxing ACID in favor of BASE is speed. Without the requirement that all data on the system must sync up in real time, individual transactions can proceed more quickly. That's a big advantage for organizations whose operations depend on quick responses. The disadvantage is that we cannot be certain without the assurances of ACID that the data we use are in fact correct. In some cases working with out-of-date data can be illegal or can lead to unacceptable business risks, but in other situations there can be a lot of tolerance for some incorrect data. Whether or not a database needs to follow the ACID protocols depends on what we need the database to do.
# 
# NoSQL databases often follow the BASE standards, and not ACID, because BASE makes more sense in a distributed system. When a database is sharded, it might exist across hundreds or thousands of servers, and updating data across all of those servers can take a significant amount of time. Waiting to achieve total data consistency before using the data to do something can take a prohibitive amount of time. The BASE standards are much more forgiving for applications that need to work faster than the speed at which data updates.

# #### Key-Value Stores
# The three most common types of NoSQL database are **key-value stores** (or key-value databases), **document stores** (or document-oriented databases), and **wide-column stores** (or column-based stores or column-oriented databases). Each format involves three types of data:
# 
# 1. A key that uniquely identifies each record and is queryable,
# 
# 2. A document (or array, or dictionary) that contains all of the data for a record,
# 
# 3. And metadata that describes the relationships between documents.
# 
# A key-value store is the simplest way to organize data in a NoSQL database. Every record is stored as a tuple of length 2: the first item is a key, and the second value is a string that contains all of the data for that key. For example, the library data can be stored in key-value format as follows:
# 
# |Key|Value|
# |:---|:---|
# |1| [18473, Ernesto Hanna, A Brief History of Time, Stephen Hawking, 8/20/19, 9/3/19, José María Chantal, Charlottesville]|
# |2| [29001, Lakshmi Euripides, Love in the Time of Cholera, Gabriel Garcia Marquez, 11/23/19, 12/14/19, José María Chantal, Charlottesville]|
# |3| [29001, Lakshmi Euripides, Anne of Green Gables, L.M. Montgomery, 1/7/20, 2/3/20, Antony Yusif, Charlottesville] |
# |4| [29001, Lakshmi Euripides, The Master and Margarita, Mikhail Bulgakov, 4/2/20, Antony Yusif, Charlottesville]|
# |5| [73498, Pia Galchobhar, Freakonomics: A Rogue Economist Explores the Hidden Side of Everything, Steven Levitt, Stephen J. Dubner, 3/2/20, 3/20/20, Dominicus Mansoor, Crozet]|
# |6| [73498, Pia Galchobhar, Moneyball: The Art of Winning an Unfair Game, Michael Lewis, 3/24/20, NULL, Antony Yusif, Charlottesville] |
# 
# In the key-value NoSQL structure, the key is **visible** to the DBMS, which means that we can perform searches or queries for particular keys, but the rest of the data are **opaque**, which means that they are only recognized by the DBMS as a single sting, and we cannot query or search for values of these attributes. Because the DBMS is agnostic about the content of the string, it is possible to put any kind of formatting into the Value field: it can organize the data in a list or array, in a JSON dictionary, or in another structure. It can contain column names, or not. The key-value DBMS can only import this string into another environment, like Python, and it is up to code in the import environment to parse the formatting. That can be extremely tricky because each Value field can contain different attributes and data types. In this example the 4th record is lacking a return date, and the 5th record has two authors: when we read the data, we need to use our knowledge of the data to catch and account for these discrepancies. The advantage of a key-value database is the speed with which it processes queries about a specific key, but the disadvantage is that is cannot query data beyond the key, and the data it returns might be in need of a lot of cleaning. As of April 2020, the [most popular key-value store DBMS](https://db-engines.com/en/ranking/key-value+store) is [Redis](https://redis.io/), which is open source. 

# #### Document Stores
# 
# A document store is similar to a key-value store, with two important differences: 
# 
# 1. The Value field in a document store must be formatted as JSON (or as XML for an XML-oriented database),
# 
# 2. And unlike a key-value database, it is possible to query data based on the fields within the JSON records.
# 
# The first transaction in the library data, for example, is stored in the document store like this:
# 
# ```
# {transactionID=1,
# cardNum=18473,
# Patron="Ernesto Hanna",
# Book=["A Brief History of Time", "Stephen Hawking"],
# Checkout="8/20/19",
# Return="9/3/19",
# Librarian="José María Chantal", 
# Branch="Charlottesville"}
# ```
# One JSON record in a document store is called, fittingly, a **document**. Documents contain the key and also the entirety of the Value field, so like a key-value store, it is possible to query the keys. But it is also possible to query any of the fields within this JSON. We could, for example, search for records in which the `Patron` field exists and is equal to `"Ernesto Hanna"`. 
# 
# Document stores have more functionality than key-value databases. In addition to the ability to issue more complex queries, document stores can be converted to **search engine databases** with [software that implements a search engine](https://github.com/elastic/elasticsearch) to extract data from the documents. In addition, it is possible to store metadata in a JSON record along with the regular data to organize documents or to create an extra layer of security for particular documents. The disadvantage of a document store relative to a key-value store is that the extra functionality results in bigger DBMSs and slower responses, in general. While document stores allow for flexible schema that cannot fit within a relational framework, queries return lists of JSON-formatted records which need to be parsed by code in an external environment.
# 
# The [most popular document store as of April 2020](https://db-engines.com/en/ranking/document+store) is [MongoDB](https://www.mongodb.com/), which is also the most popular DBMS among all NoSQL options, and the 5th most popular DBMS overall. 

# #### Wide-Column Stores
# A wide column store, like a relational database, contains tables. However unlike a relational database, every table has only one row, and each of these tables might have different columns. 
# 
# Two of the records in the library data look like this in wide-column format:
# 
# $$TransactionID = 4$$
# 
# | CardNum | Patron            | BookTitle | Author                                                                                                       | Checkout | Librarian          | Branch          |
# |:---------|:-----------------------------------------|:-------------------------------------------------------------------|:----------|:----------|:--------------------|:-----------------|
# | 29001   | Lakshmi Euripides | The Master and Margarita | Mikhail Bulgakov                                                               | 4/2/20   | NULL     | Antony Yusif       | Charlottesville |
# 
# 
# $$TransactionID = 5$$
# 
# | CardNum | Patron            | BookTitle | Author | SecondAuthor                                                                                                        | Checkout | Return   | Librarian          | Branch          |
# |:---------|:-------------------|:-------------------|:------------|:-----------------------------------------------------------------------------|:----------|:----------|:--------------------|:-----------------|
# | 73498   | Pia Galchobhar    | Freakonomics: A Rogue Economist Explores the Hidden Side of Everything | Steven Levitt | Stephen J. Dubner | 3/2/20   | 3/20/20  | Dominicus Mansoor  | Crozet          |
# 
# Like key-value and document stores, wide-column stores have records with a unique key and a document that contains the data where the schema is flexible. In this case, the table associated with `TransactionID=4` lacks a return date, and the table associated with `TransactionID=5` adds a second author column. Wide-column stores are very similar to document stores in that it is possible to issue a query based on any of the columns. It is also possible to include metadata by clustering columns under shared tags called **supercolumns**. For example, `BookTitle`, `Author`, and `SecondAuthor` may all be clustered within the supercolumn `Book`. These supercolumn families follow exactly the same logic as fields nested within other fields in a JSON tree.
# 
# Generally speaking wide-column stores offer the same functionality as document stores, but operate on tables instead of on JSON records. The [most popular column-oriented DBMS as of April 2020](https://db-engines.com/en/ranking/wide+column+store) is [Cassandra](https://cassandra.apache.org/).

# #### Graph Databases
# **Graph databases** describe an entirely different paradigm of data models. The key-value, document, and wide-column stores work with *independent* records. For these systems to work, no record should contain attributes that point to other records in the data. That way, it's not a problem to treat records separately and store them on different servers. Relational databases on the other hand contain dependencies because the different entities in the data are related to one another. However these relationships exist between columns stored in different tables, not between the records themselves. 
# 
# If the records in a database are directly related to each other, a graph database provides a way to store specific data about these relationships. The [graph database schema](https://neo4j.com/docs/getting-started/current/graphdb-concepts/) combines a relational and wide-column framework. First, each record is stored in a table with one row, as would be the case in a wide-column store. Next the tables are broken into separate entities, as we would do in a relational schema. That is, attributes that would continue to exist in the same entity in a relational database also exist in the same entity in a graph database.
# 
# Every entity for every record in a graph database is called a **node**. Every node has at least one **label**, the name of the entity, attached to it. In the library data, we have nodes for transaction, patron, librarian, book, and author. The attributes within one node are called **properties**. Nodes are connected to other nodes through **relationships**, which are represented by an arrow that is directed from one node to another. The node the arrow starts from is called the **source node**, and the relationship for this node is called an **outgoing relationship**; the node the arrow points to is called the **target node**, and the relationship for this node is called an **incoming relationship**. Every arrow is labeled with text describing the **relationship type**. 
# 
# It can be confusing to know which node is the source and which is the target and what direction the arrow should point, but it is easier to remember that these symbols should follow natural language. We usually say the target node first and the source node second. For example, in the library data, *transactions are conducted on behalf of patrons*. In this case:
# 
# * TRANSACTION is a source node,
# 
# * PATRON is a target node,
# 
# * and the relationship points from TRANSACTION to PATRON and is labeled "on behalf of".
# 
# Breaking a database into nodes for individual records and entities adds complication. But it does provide the advantage of allowing relationships to exist between records in addition to entities. For example, suppose that the library has a program in which parents can apply for library cards for their children. The library might want to know the parent of a child in their patrons table.  Suppose that library patron Pia Galchobhar checks out "Freakonomics: A Rogue Economist Explores the Hidden Side of Everything" by Steven Levitt and Stephen J. Dubner on March 2, 2020 from the Crozet branch, where she is helped by librarian Dominicus Mansoor, and returns it on March 20. Four days later she visits the Charlottesville branch with her daughter Dina where librarian Antony Yusif checks out "Moneyball: The Art of Winning an Unfair Game" by Michael Lewis for her, and "Alice in Wonderland" by Lewis Carroll for Dina. These data have the following graph representation:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/graph2.png" width="900">
# 
# The arrow that points from the patron node for Pia Galchobhar to the patron node for Dina tells us that Pia is Dina's parent. All of the other information, however, is also possible to represent in a relational database with an ER diagram. So unless there is compelling information regarding the relationship between records, a relational database is a more elegant and compact representation of the data. As of April 2020, the [most popular graph database](https://db-engines.com/en/ranking/graph+dbms) is [neo4j](https://neo4j.com/), which has a great deal of functionality to store graph structured data and to query based on nodes, relationships, labels, or properties. neo4j is also compliant with the ACID standards.

# ## Working With Databases in Python
# Now that we've covered so much of the background of the art and science of databases, it's time to work with databases in a Python environment. You will need to know how to create a database stored locally using SQLite, how to port that database onto cloud storage, and how to access databases on the cloud especially when those databases require credentials.
# 
# The following discussion does not get into how to clean data properly so that the various tables in the database conform to an organizational schema. If you need to convert a single dataframe into several tables that together abide by database normalization rules, then `pandas` is an excellent tool for cleaning data in this way. After first creating the tables, we will place them into a database using the code shown below. `pandas` is discussed in detail in modules 8 and 9. This discussion also does not cover SQL for issuing advanced queries: SQL is the focus of module 7.
# 
# To demonstrate how to work with a database in Python, we will use Kaggle data on over 100,000 [wine reviews that appeared in Wine Enthusiast Magazine](https://www.kaggle.com/zynicide/wine-reviews), which were compiled as a web scraping project by Zack Thoutt. 
# 
# Prior to doing any work in Python, let's load the relevant libraries and set the global parameters:

# In[1]:


import numpy as np
import pandas as pd
import sys
import os
sys.tracebacklimit = 0 # turn off the error tracebacks


# The entirety of the data are stored in one data frame:

# In[2]:


total = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/winemag.csv")
total


# The features in this dataframe are:
# 
# * `wine_id`: a primary key identifying one wine
# * `country`: the country of origin for the wine
# * `description`: the text of the wine review written by the Wine Enthusiast critic
# * `points`: the score given to the wine by the critic on a scale from 0 to 100 (although the lowest rated wine in the data is still rated 80, so even bad wine is pretty good!)
# * `price`: the price in U.S. dollars
# * `province`: the province or state within the country in which the wine was produced
# * `region`: the region within the province or state in which the wine was produced (for example, Central Virginia as opposed to NOVA or the Tidewater)
# * `taster_name`: the name of the Wine Enthusiast critic
# * `taster_twitter_handle`: the critic's Twitter handle
# * `title`: the official name and vintage of the wine
# * `variety`: the type of grapes that were used to make the wine
# * `winery`: the name of the winery that produced the wine
# 
# If we want to store these data in a relational database, we need to reorganize the data into separate tables to fit with the rules of database normalization. I create four tables for four separate entities: REVIEWS for the reviews of individual wines, TASTERS for information about the critics, WINERIES for information about the wineries, and LOCATION for the details on where the wine was produced. All relationships are many-to-one: many wines are reviewed by the same critic, many wines are produced by the same winery, and many wines are produced in the same location, but every wine comes from one winery at one location and is reviewed by one critic. The logical entity-relationship diagram for the database is:
# 
# <img src="https://github.com/jkropko/DS-6001/raw/master/localimages/wine_er4.png" width="400">
# 
# Technically, the data are in second normal form. Every entity has a primary key, all attributes are atomic, and there are no repeating groups so the database conforms to the 1NF standards, and every table has a single attribute for the primary key, so the data are also in 2NF. The data are not in 3NF because the location foreign key and the winery foreign key have a many-to-many relationship: many wineries can exist in the same location, and some wineries are spread out among many locations. However, because any one wine is produced in one location even when the winery has many locations, it makes more sense to me to include location as a foreign key in the REVIEWS table.
# 
# I did the work to generate these tables using `pandas`, and I saved each entity as a separate CSV file:

# In[3]:


reviews = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/wines_reviews.csv")
tasters = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/wines_tasters.csv")
wineries = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/wines_wineries.csv")
locations = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/wines_locations.csv")


# Once you create a database with a particular DBMS, the easiest workflow is to continue to use that DBMS as implemented in Python, and not to switch DBMSs. SQLite, MySQL, and PostgreSQL all have specific strengths for working with relational databases and MongoDB is a popular choice for document stores, but there are always other DBMS options. Use the DBMS that you like best, or the DBMS that matches the preferences of other people in your organization. 

# ### Using SQLite
# The `sqlite3` library is the best tool for creating a local relational database with the SQlite DBMS in Python. SQLite is fast, offers a high degree of functionality, and works very well with `pandas`. If you haven't yet done so, install this library by typing `pip install sqlite3` in a terminal or console window. Then we start by importing this library:

# In[4]:


import sqlite3


# To create a new database, first set the working directory to the folder on your machine where you want to save the database. For example:

# In[5]:


os.chdir("/Users/jk8sd/Box Sync/Practice and Applications 1 online/Module 6 - Building and Connecting to Databases")


# The `.connect()` method in the `sqlite3` library takes a filename as its argument. An entire database is stored in a single file that contains all of the data tables along with auxilliary code to handle queries. Database files usually have the extension ".db". The following command creates the specified file if it does not yet exist on your system:

# In[6]:


wine_db = sqlite3.connect("winereviews.db") 


# Take a moment and use a file browser to view the files in your working directory. You should now see a "winereviews.db" file in this folder. If the file already existed in your working directory, the `.connect()` method opens the file. Either way, the `.connect()` method establishes a database connection, which takes up RAM in your local environment. When you are done working with the database, it is important to remember to use the `.close()` method (demonstrated below) to [free up these resources and to prevent other applications from manipulating the database](https://softwareengineering.stackexchange.com/questions/214730/should-i-close-database-connections-after-use-in-php).
# 
# The database now exists as "winereviews.db" in your local storage and as `wine_db` in the Python environment. But the database is currently empty. To add data frames to serve as entities in the database, use the `.to_sql()` method, which operates on the four `pandas` data frames we created above:

# In[7]:


reviews.to_sql('reviews', wine_db, index=False, chunksize=1000, if_exists='replace')
tasters.to_sql('tasters', wine_db, index=False, chunksize=1000, if_exists='replace')
wineries.to_sql('wineries', wine_db, index=False, chunksize=1000, if_exists='replace')
locations.to_sql('locations', wine_db, index=False, chunksize=1000, if_exists='replace')


# The first argument of `.to_sql()` names the entity, the second argument specifies the database in which these entities should be placed, the third argument switches off the default behavior of creating a primary key in each entity (we already did that), `chunksize` breaks the data transfer into smaller parts to avoid overwhelming the database server (that's more of a problem for MySQL and PostgreSQL), and the last argument tells the method to overwrite each entity if a table with the given name already exists in the database. The `wine_db` database now contains four entities, named `reviews`, `tasters`, `wineries`, and `locations`.
# 
# Now that the database exists and is populated with the data, we can begin to issue queries. Queries employ SQL code, which we will discuss in great detail in module 7. Here I will make a couple basic queries.
# 
# To make queries of a database, the first step is to create a **cursor** for the database. The cursor takes in a query, passes it to the databases, and collects the output. To create a cursor, use the `.cursor()` method:

# In[8]:


wine_cursor = wine_db.cursor()


# The cursor works with two associated methods: `.execute()` takes as its argument a string that contains the query in SQL code, and `.fetchall()` supplies the output. For example, the SQL query that extracts all of the data that exists in the `reviews` entity is
# ```
# SELECT * FROM reviews
# ```
# The output of this query returned by the `.fetchall()` method is a list-of-tuples, much like a Python dictionary. To arrange the output in a data frame, pass it to the `pd.DataFrame()` function:

# In[9]:


wine_cursor.execute("SELECT * FROM reviews")
reviews_df = wine_cursor.fetchall()
pd.DataFrame(reviews_df)


# There are two ways to include column names in the data frame. First, we can extract these name from the `.description` attribute of the cursor. They are stored as the first element in each of a series of lists, so we can use a comprehension loop to quickly extract these column names:

# In[10]:


colnames = [x[0] for x in wine_cursor.description]
pd.DataFrame(reviews_df, columns=colnames)


# Another method of extracting the data to a data frame with the column headers is to use the `pd.read_sql_query()` function, which acts as a wrapper for the cursor functionality. All you need to do is pass the SQL query as a string as the first argument and the name of the database as the second argument, and the function returns the data frame we want:

# In[11]:


df = pd.read_sql_query("SELECT * FROM reviews", wine_db)
df


# `pd.read_sql_query()` is a great tool for performing Read queries: extracting data from the database without altering the database. But for other kinds of operations (create, update, and delete operations), we have to use the cursor. 
# 
# One useful feature of SQlite is that it automatically generates an entity named `sqlite_master` that contains metadata about the other tables in the database. For example, to see a list of all of the entity names in the database, we pass the following query to the cursor:

# In[12]:


wine_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
available_table=(wine_cursor.fetchall())
available_table


# Once we are done working with the database, we need to call two functions. First, if we've issued a query that alters the database in any way by creating, updating, or deleting data, we need to keep track of the changes we've made and save the new version of the database by using the `.commit()` method:

# In[13]:


wine_db.commit()


# And finally, to free up the resources on your machine that the database is using, use the `.close()` method:

# In[14]:


wine_db.close()


# SQlite works very well with locally-stored databases. However, it does not have the ability to operate over networked connections. For working with databases remotely, we can use MySQL or PostgreSQL.

# ### Using MySQL
# Unlike SQlite, MySQL requires external software on your machine in addition to Python libraries in order to run in your Python environment. To get started, follow these steps.
# 
# 1. Download and install MySQL: https://dev.mysql.com/downloads/mysql/. You will be taken to a screen that encourages you to sign up for Oracle services - don't bother with that, just select "No thanks, just start my download." 
# 
# (The reason why the MySQL DBMS, which is *open source*, advertises for Oracle - makers of *proprietary* database software - is that MySQL was recently [bought by Oracle](https://www.infoworld.com/article/2629625/users-nervous-about-oracle-s-acquisition-of-mysql.html), and that has caused a lot of worry and consternation among MySQL users. The concern is that Oracle will limit the future development of MySQL or make extensions proprietary to get people to pay for software that had been open and free. In response to this acquistion, independent and open source alternatives such as PostgreSQL have become more popular.)
# 
# 2. Once the software is downloaded, open up the installer and work through the windows that guide you through the installation. You will be asked to create a password: this is the password you will use to access all databases you create locally with MySQL, so make sure you remember this password. Also, choose the legacy password encryption, as that option works better with the libraries that connect Python to MySQL.
# 
# 3. Now that MySQL is installed on your computer, open the software to start the MySQL server:
# 
#     * On a Mac: click the apple in the upper-left corner of the screen, and select "System Preferences". That will open a window in which one icon is "MySQL". Click that icon, and you will see the screen with the "Start MySQL Server" button.
#     
#     * On a [Windows machine](https://superuser.com/questions/666521/how-do-i-start-a-mysql-server-on-windows): Open up the Services icon in the Control Panel, scroll alphabetically to the MySQL service, right click the service, and click Start Service. Alternatively, you can do this from  the command line: Open a DOS window, and from the C: Prompt, run this: `net start mysql`.
# 
# 4. To use MySQL within Python, you first have to download and install the MySQL connector for Python, which you can do by opening a console or terminal window and typing `pip install mysql-connector`. Then in your script or notebook, import this module:

# In[15]:


import mysql.connector


# One important difference between SQLite and MySQL is that MySQL always requires a password to access a database, and SQLite does not. Because SQLite is designed to work only on local storage, the idea of a password is considered redundant because a user would have already entered a password to access their personal operating system. The following examples require a password - but because I do not want to display my password in this notebook, I will use the same method we used in module 4 to keep API keys secret. Please refer to the "How to Keep Your Access Key Secret" section in module 4 for instructions. Here I load my MySQL password from a `.env` file on in my working directory:

# In[16]:


import dotenv
dotenv.load_dotenv()
mysqlpassword = os.getenv("mysqlpassword")


# MySQL sets up a server to store local databases on something called a [localhost](https://whatismyipaddress.com/localhost), which is temporary space on your computer. To access this server, you have to provide your password and specify "root" as your username (because the database will live on your local system, that makes you the [root user](https://en.wikipedia.org/wiki/Superuser), or administrator, of the database). In Python, type: 

# In[17]:


dbserver = mysql.connector.connect(
    user='root', 
    passwd=mysqlpassword, 
    host="localhost"
)


# This command accesses the MySQL server currently running on your computer and refers to it as `dbserver` in Python. To work with this server, create a cursor, which uses the `.execute()` and `.fetchall()` methods the same way it does with SQlite:

# In[18]:


cursor = dbserver.cursor()


# To create a new database within your MySQL server, type

# In[19]:


try:
    cursor.execute("CREATE DATABASE winedb")
except:
    cursor.execute("DROP DATABASE winedb")
    cursor.execute("CREATE DATABASE winedb")


# where `winedb` is the name of the new (empty) database on your server. If there is already a database named `winedb` on this server, `cursor.execute("CREATE DATABASE winedb")` will yield an error. The `try:` and `except:` syntax is called a **try-catch block**: it executes the code under `try:`, and if there is an error, executes the code under `except:` instead. In this case, if the database already exists, the `except` block drops the database then creates a new (empty) version of that database.
# 
# To see all of the databases that currently exist on the server, type

# In[20]:


cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()
databases


# Before we can place data into the empty wine database, we have to connect to this database. For that we use the same syntax that we used to connect to the MySQL server, but we issue an extra argument to specify the database we need to connect to:

# In[21]:


winedb = mysql.connector.connect(
    user='root', 
    passwd=mysqlpassword, 
    host="localhost",
    database="winedb"
)


# There are a few different ways to input data into a local MySQL database, but the most straightforward approach is to use a Python library called `sqlalchemy` (type `pip install sqlalchemy` if you haven't yet installed it). Here we just need the `create_engine()` function from the `sqlalchemy` library:

# In[22]:


from sqlalchemy import create_engine


# This function creates an "engine" that does all the work of interfacing with our database so that we can use functions in `pandas` to read and edit the data within the database. The difficult part is setting up the engine. We have to put together a URL that contains all the information `create_engine()` needs to access a database, and every combination of DBMS and Python library to work with that DBMS requires a different URL format. According to the [`sqlalchemy` documentation](https://docs.sqlalchemy.org/en/13/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqlconnector), the syntax for MySQL and the `mysql.connector` module is 
# ```
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
# ```
# where we have to supply the username ("root"), our MySQL password, the host and port (both covered under "localhost"), and the database name ("winedb" in this case). Using the `.format()` method allows us to input these parameters separately:

# In[23]:


engine = create_engine("mysql+mysqlconnector://{user}:{pw}@localhost/{db}"
                       .format(user="root", pw=mysqlpassword, db="winedb"))


# This engine allows us to use the `.to_sql()` method from `pandas` to place the four data frames into the wine database. First we set a name for each entity, then we pass the `sqlalchemy` engine, then we specify that the entity should be overwritten with new data if it already exists (we could also specify that the data is appended to the old, or that the operation provides an error if the entity already exists):

# In[24]:


reviews.to_sql('reviews', con = engine, index=False, chunksize=1000, if_exists = 'replace')
tasters.to_sql('tasters', con = engine, index=False, chunksize=1000, if_exists = 'replace')
wineries.to_sql('wineries', con = engine, index=False, chunksize=1000, if_exists = 'replace')
locations.to_sql('locations', con = engine, index=False, chunksize=1000, if_exists = 'replace')


# Now all four tables are entities within the `winedb` database.
# 
# To query the database, we can create a cursor that points to the database, and we can issue queries directly to this cursor directly:

# In[25]:


cursor = winedb.cursor()
cursor.execute("SELECT * FROM reviews")
reviews_df = cursor.fetchall()
colnames = [x[0] for x in cursor.description]
pd.DataFrame(reviews_df, columns=colnames)


# Or we can use the `pd.read_sql_query()` function by passing the `sqlalchemy` engine to this function:

# In[26]:


pd.read_sql_query("SELECT * FROM reviews", con=engine)


# Before ending our work with this MySQL database, we use the `.commit()` method to save and keep track of any changes we made in the MySQL server:

# In[27]:


dbserver.commit()


# And we close the connection to the server to prevent any other applications from interfacing with this server and to free up the resources that the server connection is taking up on the local machine:

# In[28]:


dbserver.close()


# To export the wine database to cloud storage or to another computer, we need to save the MySQL database as a file in a specific folder. To do that, following these steps: 
# 
# * Open a DOS window on a Windows system, or a terminal window on Mac and Linux systems.
# 
# * Use `cd` to change the directory to the folder on your computer where you want to save the PostgreSQL database.
# 
# * Type the following command: `mysqldump -u root -p --databases winedb --result-file wine.sql`, where
#     * `root` is the default user name, which you will need to change if you changed your MySQL username
#     * `winedb` is the name of the MySQL database we want to export to a file, 
#     * and `wine.sql` is the name of the file we are creating. Feel free to change the filename, but leave the extension `.sql`.
# 
# * You will be asked to type your MySQL password.
# 
# * If you see an error that reads `command not found`, try altering the path that the command line uses to connect with your local MySQL installion by typing `export PATH=$PATH:/usr/local/mysql/bin`, then trying the `mysqldump` command again.
# 
# You now have a self-contained database file for the wine database.

# ### Using PostgresSQL
# To use PostgreSQL, you must first download and install PostgreSQL. On Windows, the easiest way to do this is to download the PostgreSQL Core Distribution here: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads. In the installation wizard, leave the boxes checked for PostgreSQL server, pgAdmin 4, Stack Builder, and Command Line Tools. Choose a password, and use the default port number and locale. Stack Builder is useful for downloading and installing extensions to PostgreSQL, but no need to run Stack Builder at this time.
# 
# On Mac, the easiest way to get PostgreSQL is to use homebrew, a package manager for Mac systems. If you've never used homebrew before, follow the instructions for installing homebrew here: https://brew.sh/. Once you've installed homebrew, type `brew install postgres` into the [Mac terminal](https://www.businessinsider.com/how-to-open-terminal-on-mac) to install PostgreSQL. Then, to launch the local PostgreSQL server, type `brew services start postgresql`. To issue commands to the PostgreSQL server type `psql`. You should see something that looks like the following:
# ```
# psql (12.3)
# Type “help” for help.
# 
# myusername=#
# ```
# Next you will need to choose a password for accessing the PostgreSQL server. On the line next to `myusername=#` (the user name should be the same as the name of the primary user account for your Mac), type the following:
# ```
# ALTER USER user_name WITH PASSWORD 'new_password';
# ```
# Replace `user_name` with whatever appeared instead of `myusername` above, and replace `new_password` with the password you want for accessing the PostgreSQL server.
# 
# The next step is to install the `psycopg2` library for Python, which is the main library for working with PostgreSQL databases in Python. The problem is that `pip install psycopg2` will not work, in general, and the steps to install this library can be complicated and maddening. There are two versions of `psycopg2`: the binary version and the source version. The binary version is much easier to install as `pip install psycopg2-binary` should work. However, the [official documentation](https://www.psycopg.org/docs/install.html#binary-install-from-pypi) for `psycopg2` warns:
# 
# > The psycopg2-binary package is meant for beginners to start playing with Python and PostgreSQL without the need to meet the build requirements. . . . If you are the maintainer of a publish package depending on psycopg2 you shouldn’t use ‘psycopg2-binary’ as a module dependency. For production use you are advised to use the source distribution.
# 
# So if you want to learn the basics of PostgreSQL, install the `psycopg2-binary` package. However, if you think that you will be doing serious work with PostgreSQL in the future, do not install `psycopg2-binary` and instead follow these next instructions to install `psychopg2` from source:
# 
# On Windows machines, follow the guide on this GitHub repository: https://github.com/nwcell/psycopg2-windows
# 
# On Mac and Linux systems, follow these steps:
# 
# 1. Install the `wheel` and `setuptools` libraries:
# 
# ```
# pip install --upgrade wheel
# pip install --upgrade setuptools
# ```
# 
# 2. Find the path on your computer that leads to a file named `pg_config`. On my Mac, the path to this file is
# ```
# /Library/PostgreSQL/12/bin
# ```
# <br>This path might be different on your machine, however.
# 
# 3. Open a Terminal window and add a global variable named `PATH`:
# ```
# export PATH=/Library/PostgreSQL/12/bin:$PATH 
# ```
# <br>Here you will need to replace the address in the middle of this command with the path you found in step 2. This step tells `pip` where to find the appropiate backend PostgreSQL configuration files for the next step.
# 
# 4. Now type
# ```
# pip install psycopg2
# ```
# <br>Hopefully it installs without any errors!
# 
# 5. In a Python script, notebook, or console, try to run `import psycopg2`. If it loads without error, you have successfully installed this library. But you might get a cryptic error. I followed the steps described in this Youtube video to fix this error: https://www.youtube.com/watch?v=_1JrRFnO1UU. In my case, I returned to the terminal and issuing the following command:
# ```
# sudo ln -s /Library/PostgreSQL/12/lib/libpq.5.dylib /usr/local/lib
# ```
# <br>After running this command, `import psycopg2` successfully runs in my Python environment:

# In[29]:


import psycopg2


# Now that `psycopg2` library has been imported, the workflow for creating a local PostgreSQL database in Python is very similar to the workflow for creating a MySQL database. Please refer to the [discussion for MySQL](#mysqllocal) for more detail.
# 
# When installing the PostgreSQL core distribution, I chose a password for accessing the PostgreSQL server on my computer. I saved that password in a `.env` file, so as not to display it in this notebook, and I bring that password into my Python environment by loading the environmental variable:

# In[30]:


dotenv.load_dotenv()
pgpassword = os.getenv("pgpassword")


# To connect to the PostgreSQL server, we can use the `.connect()` method by supplying a username and password, and setting `host="localhost"` to refer to the server that runs locally. By default, the user name for a PostgreSQL database is `postgres` (if you installed from the Enterprise DB Core Distribution), or your Mac username if you installed using homebrew on a Mac. My username happens to be "jk8sd". It is also important for the `.autocommit` attribute of the server to be set to `True` to allow us to create databases on the server:

# In[31]:


dbserver = psycopg2.connect(
    user='jk8sd', 
    password=pgpassword, 
    host="localhost"
)
dbserver.autocommit = True


# Now that I have established a connection with the local PostgreSQL server, I can use a cursor that points to the server:

# In[32]:


cursor = dbserver.cursor()


# The cursor takes in SQL queries with the `.execute()` method and returns output with the `.fetchall()` method. To create an (empty) database for our wine data, we can query `"CREATE DATABASE winedb"`.  If this database already exists, this query will result in an error, so I use a try-catch block that first drops the "winedb" database from the server if it already exists:

# In[33]:


try:
    cursor.execute("CREATE DATABASE winedb")
except:
    cursor.execute("DROP DATABASE winedb")
    cursor.execute("CREATE DATABASE winedb")


# Next, to connect to the "winedb" database itself, we can use the same call to `.connect()`, only this time specifying `database="windedb"`:

# In[34]:


winedb = psycopg2.connect(
    user='jk8sd', 
    password=pgpassword, 
    host="localhost",
    database="winedb"
)


# The easiest way to input whole data frames into the database is to create an engine with `sqlalchemy`, which enables us to use the `.to_sql()` method in `pandas`. The syntax for creating an engine for PostgreSQL and the `psycopg2` library for the `create_engine()` function is available in the `sqlalchemy` [documentation](https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2). In this case, the code that creates the engine is:

# In[35]:


engine = create_engine("postgresql+psycopg2://{user}:{pw}@localhost/{db}"
                       .format(user="jk8sd", pw=pgpassword, db="winedb"))


# We can now pass this engine to the `.to_sql()` method to place the four data frames that comprise the entities of the wine database into `winedb`: 

# In[36]:


reviews.to_sql('reviews', con = engine, index=False, chunksize=1000, if_exists = 'replace')
tasters.to_sql('tasters', con = engine, index=False, chunksize=1000, if_exists = 'replace')
wineries.to_sql('wineries', con = engine, index=False, chunksize=1000, if_exists = 'replace')
locations.to_sql('locations', con = engine, index=False, chunksize=1000, if_exists = 'replace')


# We can now pass queries to `winedb` that read the data and return structures that we can organize in a data frame. First we establish a cursor that points to `winedb`:

# In[37]:


cursor = winedb.cursor()


# To extract the entirety of the `reviews` entity, we pass the query `"SELECT * FROM reviews"` to the `.execute()` method of this cursor and extract the data with `.fetchall()`. We also extract the column names and arrange them along with the output data in a data frame:

# In[38]:


cursor.execute("SELECT * FROM reviews")
reviews_df = cursor.fetchall()
colnames = [x[0] for x in cursor.description]
pd.DataFrame(reviews_df, columns=colnames)


# Alternatively, we can use the `sqlalchemy` engine to issue the same query with the `pd.read_sql_query()` function:

# In[39]:


pd.read_sql_query("SELECT * FROM reviews", con=engine)


# Before ending our work with the local PostgreSQL server, we apply the `.commit()` method to the server to save and keep track of the changes we made:

# In[40]:


dbserver.commit()


# And we conclude the session by closing the server:

# In[41]:


dbserver.close()


# To export the wine database to cloud storage or to another computer, we need to save the PostgreSQL database as a file in a specific folder. To do that, use the `pg_dump` method by following the steps outlined in [this article](https://www.a2hosting.com/kb/developer-corner/postgresql/import-and-export-a-postgresql-database#Method-1.3A-Use-the-pg-dump-program), which I summarize here: 
# 
# * Open a DOS window on a Windows system, or a terminal window on Mac and Linux systems.
# 
# * Use `cd` to change the directory to the folder on your computer where you want to save the PostgreSQL database.
# 
# * Type the following command: `pg_dump -U postgres winedb > wine.pgsql`, where
#     * `postgres` is the default user name, which you will need to change if you changed your PostgreSQL username
#     * `winedb` is the name of the PostgreSQL database we want to export to a file, 
#     * and `wine.pgsql` is the name of the file we are creating. Feel free to change the filename, but leave the extension `.pgsql`.
# 
# * You will be asked to type your PostgreSQL password.
# 
# The database will now exist as a single file in the folder you specified.

# ### Using MongoDB
# MongoDB works with document stores, a type of NoSQL database that stores records as documents, often in JSON format. As with MySQL and PostgreSQL, the first step is to install the external MondoDB software on to your computer. The version we will use is the Community Edition, which is open source. Please follow the instructions listed here to install MongoDB on your own system: https://docs.mongodb.com/manual/installation/. For example, I was able to install MongoDB on my Macbook by following these instructions:
# 
# 1. Download the Apple Command Line Tools: https://apps.apple.com/us/app/xcode/id497799835?mt=12
# 
# 2. Open the Terminal and install [Homebrew](https://brew.sh/#install) by typing:
# ```
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# ```
# <br>
# 3. In the Terminal I access the repository where MongoDB exists online by typing
# ```
# brew tap mongodb/brew
# ```
# <br>
# 4. In the Terminal I download and install MongoDB by typing
# ```
# brew install mongodb-community@4.2
# ```
# <br>
# 5. In the Terminal, I start a local MongoDB server on my computer by typing
# ```
# brew services start mongodb-community@4.2
# ```
# 
# For this example, we'll use a JSON version of the wine database. The following code converts the total wine reviews dataset to JSON format and registers it as JSON formatted data:

# In[42]:


import requests
import json
wine_json_text = total.to_json(orient="records")
wine_json = json.loads(wine_json_text)


# The first record in the JSON data is

# In[43]:


wine_json[0]


# To work with MongoDB in Python, we use the `pymongo` library. Fortunately, unlike `mysql.connector` and `psycopg2`, `pymongo` is easy to install by typing `pip install pymongo`. We import this library:

# In[44]:


import pymongo


# To access the local MongoDB server that is up and running, use the `.MongoClient()` method. The address inside the following call to `.MongoClient()` tells Python that this server is running on the local machine:

# In[45]:


myclient = pymongo.MongoClient("mongodb://localhost/")


# To create a database on this server, we pass a string element to `myclient` named after the database we want to create. Here we create a database called "winedb" on the MongoDB server, and we refer to this database as `winedb` in the Python environment:

# In[46]:


winedb = myclient["winedb"]


# One database can contain many collections of documents. Here we set up a new collection named "winecollection" on the MongoDB server, and we refer to this collection as `winecollection` in the Python environment. The first three lines of code in this block check whether this collection already exists in the "winedb" database, and if so, drops this collection before creating a new (currently empty) collection with this name:

# In[47]:


collist = winedb.list_collection_names()
if "winecollection" in collist:
  winedb.winecollection.drop()


# In[ ]:


winecollection = winedb["winecollection"]


# It's time to put some documents into this document store. To put one document into a collection, use the `.insert_one()` method which operates on the Python variable that refers to the collection we are editing. Here we put the first wine in the data into "winecollection":

# In[ ]:


onewine = winecollection.insert_one(wine_json[0])


# When we operate on a MongoDB database by creating, reading, updating, or deleting records, and set this operation equal to a Python variable (`onewine` in this case), that variable acts as the cursor for the database. 
# 
# When we put documents into a MongoDB document store, MongoDB places a unique primary key onto the document. To see the primary key for the record we just placed into the database, call the `.inserted_id` attribute of the cursor:

# In[ ]:


onewine.inserted_id 


# To query the database, write the query in JSON format, not in SQL format. For example, to find the wine whose title is "Nicosia 2013 Vulkà Bianco (Etna)", we write: 

# In[ ]:


myquery = { 'title': 'Nicosia 2013 Vulkà Bianco  (Etna)'}


# To execute this query, specify the collection and apply the `.find()` method, passing the query to `.find()`. To see the query results, use a loop across elements of the cursor (`mywine` in this case) and print the elements. Here, because we are issuing a query for the only record in the database, we see one result:

# In[ ]:


mywine = winecollection.find(myquery) 
for x in mywine:
    print(x)


# To delete documents, query the documents you want to delete and pass this query to the `.delete_one()` method:

# In[ ]:


myquery = { 'title': 'Nicosia 2013 Vulkà Bianco  (Etna)'}
winecollection.delete_one(myquery) 


# Now "winecollection" is empty again.
# 
# Next, let's insert all of the records into "winecollection". In this case, we use the `.insert_many()` method applied to `winecollection` and pass the entire JSON file:

# In[ ]:


allwine = winecollection.insert_many(wine_json)


# To see the number of documents in a collection, use the `.count_documents()` method on the collection. Passing an empty set `{}` counts all documents, and passing a JSON query counts the number of documents that match that query:

# In[ ]:


winecollection.count_documents({})


# Of all of these wines, we can use a query to identify all of the reviews of wines from Virginia. We can further narrow that search down to only the Cabernet Sauvignons from Virginia. The query that identifies these documents is:

# In[ ]:


myquery = {'province': 'Virginia',
          'variety': 'Cabernet Sauvignon'}
vawine = winecollection.find(myquery) 
winecollection.count_documents(myquery)


# There are 13 Cabernet Sauvignons from Virginia in the data. To collect the data from these records and output a JSON file with only these wines, we use the `dumps` and `loads` functions from the `bson.json_util` module. Do not type `pip install bson`: the `bson` library is installed along with `pymongo` with matching versions. Installing `bson` separately acquires the old version of `bson`, which can clash with `pymongo`. 
# 
# `bson.json_util` is similar to the `json` library, but it contains extra functionality to work with the `pymongo` curser to extract the data. 

# In[ ]:


from bson.json_util import dumps, loads


# To convert the query to plain text, we pass the query directly to `dumps()`:

# In[ ]:


vawine_text = dumps(winecollection.find(myquery))


# Then to register the text as JSON formatted data, we pass the result to `loads()`:

# In[ ]:


vawine_records = loads(vawine_text)
vawine_records[0]


# The output of the `loads()` function is a list of individual JSON records. To pass these records to a data frame, we use the `pd.DataFrame.from_records()` function:

# In[ ]:


vawine_df = pd.DataFrame.from_records(vawine_records)
vawine_df


# `pymongo` does not require that we commit the changes, but we do end our session by closing the connection to the MongoDB server:

# In[ ]:


myclient.close()


# To export the MongoDB database to a local file, open a DOS or Terminal window and use `cd` to navigate to the folder where you want to save the database. Then simply type `mongodump`.
# 
# If you receive an error that says the `mongodump` command is not found, try typing `sudo port install mongo-tools`, then retry `mongodump`.
# 
# If this command is successful you will see a folder named "dump" within the directory you specified. Inside this folder are folders for each database that currently exists on your MongoDB server, and within the "winedb" folder there are two files: a `.bson` file containing the data and a `.json` file containing metadata like collections.

# ### Connecting to Remote Databases on Amazon Web Services (AWS)
# All of the previous examples work with a database that is hosted on your own computer. But in most cases, you will be connecting to a database that is stored elsewhere, accessing it remotely. At the University of Virginia, we have a high performance cluster of computers called [Rivanna](https://www.rc.virginia.edu/userinfo/rivanna/overview/), and many of the research projects that require large amounts of data store these databases on Rivanna. But in industry, the most popular cloud computing service is [Amazon Web Services (AWS)](https://aws.amazon.com/). AWS is so widely used that it accounted for [$2.2 billion in revenue in the first quarter of 2019, and accounted for 50% of Amazon’s overall operating income.](https://www.cnbc.com/2019/04/25/aws-earnings-q1-2019.html)
# 
# AWS provides many services, but the two most important services are **S3 buckets** and **EC2 instances**. An S3 bucket is physical storage - an actual storage device located at one of Amazon's many [data centers](https://aws.amazon.com/compliance/data-center/data-centers/). Industrial application with massive data storage requirements can put all of their data onto an S3 bucket, which has benefits for keeping the data secure and accessible, for a fee. An EC2 instance is a virtual computer, where users can perform tasks and run code. There are many different [types of EC2 instances](https://aws.amazon.com/ec2/instance-types/) which have different price points and which allocate different numbers of CPUs and amounts of memory. Tech companies that use machine learning for predictive modeling can store the training, test, and validation sets on S3 buckets and import the data to an EC2 instance to run a model. Depending on the amount of data and on the performance requirements of the virtual machine, these businesses can end up owing AWS an incredible amount of money.
# 
# Another use of virtual computing on AWS is running database servers. Relational databases are stored and run on AWS's [Relational Database Service (RDS)](https://console.aws.amazon.com/rds/home?region=us-east-1), and document store NoSQL databases are stored and run on AWS's [DocumentDB](https://console.aws.amazon.com/docdb/home?region=us-east-1#clusters) service. 
# 
# There is a high likelihood that your future employers will want you to be able to access and work with databases stored on AWS. Fortunately, the methods to access AWS databases are very similar to the methods described above for accessing data locally. There are only a couple differences:
# 
# First, the host will be an AWS endpoint URL instead of "localhost". For the following example, I created a version of the MySQL wine database on AWS, and the endpoint for this database is
# ```
# wine-mysql.cp6gfvxaumkx.us-east-1.rds.amazonaws.com
# ```
# 
# Second, you will usually not be the primary administrator (or "root user") of a database you access remotely. If you are granted access to a database, you will be granted an [Identity and Access Management (IAM) token](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAM.html). The root user of the database controls the database and can edit it, delete it, and control who has access to it and how others can use the database. IAM users are granted rights to use the database in limited ways by the root user. It is common, for example, for the root user to grant IAM users the ability to read the data, but not to create, update, or delete data.
# 
# Otherwise, so long as you pass the new host, and your IAM username and password, the same code listed above works for making queries to AWS databases.
# 
# To access the MySQL wine database, the root user makes me an IAM user - I then receive an email from AWS inviting me to register and select my own username and password. I store this password in an `.env` file and load it into this notebook:

# In[ ]:


dotenv.load_dotenv()
mysqlpassword = os.getenv("mysqlpassword")


# Next I connect to the "winedb" database on the AWS server. Here I use the `mysql.connector.connect()` method, and I pass my IAM username and password, along with the host name:
winedb = mysql.connector.connect(
    user='jkropko', 
    passwd=mysqlpassword, 
    host="wine-mysql.cp6gfvxaumkx.us-east-1.rds.amazonaws.com",
    database="winedb"
)
# I am now free to issue queries to this remote database. I can use the same methods I applied above, changing the host, username, and password where necessary. To make the job of querying easier, I use `create_engine()` from the `sqlalchemy` library:
engine = create_engine("mysql+mysqlconnector://{user}:{pw}@wine-mysql.cp6gfvxaumkx.us-east-1.rds.amazonaws.com/{db}"
                       .format(user="jkropko", pw=mysqlpassword, db="winedb"))
# To pull all the data from the "reviews" table, I issue the following query using the `pd.read_sql_query()` function:

# pd.read_sql_query("SELECT * FROM reviews", con=engine)

# Finally, like before, I wrap up my work by closing the connection:
winedb.close()