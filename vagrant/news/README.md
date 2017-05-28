# Logs Analysis Project

This directory contains a script to make three queries on a PostgreSQL database:

* Obtain the 3 most popular articles by number of total views in descending order.
* Obtain the 3 most popular authors by number of total views on their articles in
  descending order.
* Obtain the dates when the percent of requests that resulted in an error was at
  least 1%.

## Prerequisites

* Python 3 is installed.
* PostgreSQL is installed.
* Database *news* exists.
* The *news* database is populated with the correct data.

## Setting up environment

The easiest way to set up your environment is to install a VirtualBox virtual machine
(VM) preconfigured with python and PostgreSQL, to launch the VM with Vagrant, and to
run a script to populate the database.

* Install VirtualBox from [virtualbox.org][1].
* Install Vagrant from [vagrantup.com][2].
* Download the VM configuration [FSND-Virtual-Machine.zip][3], or use git to clone
  the repo with the configuration:
  `git clone https://github.com/udacity/fullstack-nanodegree-vm.git`. Note this
  contains a `vagrant` directory containing `Vagrantfile`, the configuration file.
  The directory is shared with the VM at `/vagrant` after it is launched, so anything
  under `vagrant` will be visible under `/vagrant` in the VM.
* Download the data from [here][4] to the `vagrant` directory.
* Download `news.py` to the `vagrant` directory.

## Launching the environment

### Launch and connect to the virtual machine

Using a terminal, change working directory to the `vagrant` directory containing the
VM configuration file, i.e., directory containing `Vagrantfile`, launch the VM and then
connect to it:

```bash
vagrant up
vagrant ssh
```

### Setup the DB

Inside of the VM,

```bash
cd /vagrant
unzip newsdata.zip
psql -d news -f newsdata.sql
```

## Executing the script

Inside of the VM at `/vagrant`,

```bash
chmod 777 news.py
./news.py
```

## DB queries

### The most popular article by total views

```sql
select title, count(*) as total_views
from articles, log
where articles.slug = right(path, -9)
group by articles.title
order by total_views desc
limit 3;
```

### The most popular author by total article views

```sql
select authors.name, count(*) as total_views
from authors, articles, log
where authors.id = articles.author and articles.slug = right(path, -9)
group by authors.name
order by total_views desc
limit 3;
```

### Date and rate of days with request error rate of at least 1%

```sql
select hits_per_day.log_day, 100.0*err_per_day.total/hits_per_day.total as err_percent
from
  (select time::date as log_day, count(*) as total
   from log where status = '200 OK'
   group by log_day) as hits_per_day,
  (select time::date as log_day, count(*) as total
   from log where status != '200 OK'
   group by log_day) as err_per_day
where hits_per_day.log_day = err_per_day.log_day
  and 1.0*err_per_day.total/hits_per_day.total >= 0.01;
```

## Don't import it, run it!

My initial intention was to make the script more general by defining a function for
each query, since it is easy to parameretize aspects of the queries, such as the
limit number in both *most popular* queries, or the percent error rate in the
*percent of bad requests* query; however, in the end I decided to skip the function
definitions because the benefit of having a separate function for each query did not
justify the costs, at least not for me. For example, defining functions for each
query meant dealing with these tradeoffs

* Opening a DB connection in each query, making the whole thing less efficient.
* To avoid opening the DB connection in each query, either
  * define a global variable with the connection before calling the functions, or
  * Make the connection a parameter of each function, resulting in more complex
    function signatures with more complex error checking logic.

Besides resulting in more boilerplate code, it also seems highly unlikely that I or
anyone else would use these functions. Therefore, I decided to keep things simple and
make `news.py` a pure script.


[1]: https://www.virtualbox.org/wiki/Downloads
[2]: https://www.vagrantup.com/downloads.html
[3]: https://d17h27t6h515a5.cloudfront.net/topher/2017/May/59125904_fsnd-virtual-machine/fsnd-virtual-machine.zip
[4]: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
