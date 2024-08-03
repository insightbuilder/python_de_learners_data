/* Locate the tables inside the DB*/

select *
from information_schema.tables
where table_schema ='public'

/*Need to create a table. start by thinking about 
what the table will hold. ETL 
- Check the tables in the DB
- Decide which columns in the tables you require
- Decide which rows in those columns you require
**/

select *
from reviews_details rd 
order by rd.reviewer_id desc 

/*
 * Lets create index on the table reviews_details
 */

drop index if exists rd_rid_idx

create index rd_rid_idx
on reviews_details(reviewer_id)

/*
 * Lets check the created index
 */

select *
from pg_catalog.pg_indexes
where tablename = 'reviews_details'

/*
 * Lets check the constraints on this table
 */
select table_catalog , table_name ,constraint_type ,
		constraint_name 
from information_schema.table_constraints
where table_name ='reviews_details'
/*
 * There will be no constraints
 */

/*
 * Lets create sequences
 */
create sequence rev_id_seq

select *
from information_schema.sequences

/*
 * Will throw error
 */
select currval('rev_id_seq') 


drop sequence if exists rev_id_seq

/*
 * Create sequence per spec
 */

create sequence test_rev
start with 10
minvalue 0
maxvalue 1100
increment by 1

select nextval ('test_rev') 

select currval('test_rev') 

/*
 * Using the sequence in the table (2ways)
 */
CREATE SEQUENCE tab_col_id_seq 
    START WITH 7
    MINVALUE 1

ALTER TABLE table_name 
    ALTER COLUMN col_name 
    SET DEFAULT nextval('tab_col_id_seq')


select count(distinct(rd.reviewer_name))
from reviews_details rd 

/*count |
------+
54244|*/

select count(distinct(rd.reviewer_id))
from reviews_details rd 

select count(*) from reviews_details rd 

/*count |
------+
431830|*/

/*After reviewing the reviews_details table
 * the reviewer names are repeated. We can 
 * create a new table which has reviewer_name, 
 * number of reviews, and a name_id
 */

create table reviewer (
	name_id int,
	reviewer_name varchar,
	number_of_reviews int
)

select constraint_name ,constraint_type ,
		table_name ,table_schema 
from information_schema.table_constraints
where table_name ='reviewer'


alter table reviewer 
	alter column name_id set not null,
	alter column reviewer_name set not null 

select constraint_name ,constraint_type ,
		table_name ,table_schema 
from information_schema.table_constraints
where table_name ='reviewer'

alter table reviewer 
	alter column number_of_reviews set default 0

alter table reviewer 
	add column update_ts timestamp default current_timestamp
	
select constraint_name ,constraint_type ,
		table_name ,table_schema 
from information_schema.
where table_name ='reviewer'

/*
 * Lets test the table
 */

insert into reviewer(reviewer_name)
values('first person'),('second person')


insert into reviewer(name_id,reviewer_name)
values(1, 'first person'),(2,'second person')


select *
from reviewer

/*
 * Lets make the name_id generate automatically
 * Drop table reviewer. And we know to add
 * constraints this time, so lets add them 
 * when creating the table itself
 */

drop table if exists reviewer


create table reviewer(
	name_id serial primary key,
	reviewer_name varchar,
	num_reviews int default 0,
	update_ts timestamp default current_timestamp
)

select table_catalog ,table_name ,
constraint_name , constraint_type 
from information_schema.table_constraints
where table_name ='reviewer'

select *
from information_schema.sequences

select nextval('reviewer_name_id_seq') 

insert into reviewer(reviewer_name)
values('first person'),('second person')

select *
from reviewer

select currval('reviewer_name_id_seq')

delete from reviewer 
where name_id > 1

truncate table reviewer

/*
 * Next lets make another table, which contains the 
 * details of the listings and their ids, their host_ids,
 * host_names, and num of reviews each of listing has
 */

select rd.listing_id ,count(rd.id)
from reviews_details rd 
group by rd.listing_id 
limit 5

/*
 * Above table provides the id and count. 
 * We need the name and host of the listing
 */

select l.id ,l.host_id ,l.host_name 
from listings l 
limit 5

/*
 * We can join the above results as follows
 */

with temp_reviews as(
	select rd.listing_id ,count(rd.id) as review_count
	from reviews_details rd 
	group by rd.listing_id 
)
select tr.listing_id , tr.review_count,
	l.host_id, l.host_name,l."name" as prop_name
from temp_reviews tr
join listings l 
on l.id = tr.listing_id
where l."name" is not null and l.host_name is not null


drop table if exists listing_reviews;

create table listing_reviews(
	prop_id int unique primary key,
	prop_name varchar not null,
	host_id int not null,
	host_name varchar not null,
	reviews_count int default 0
)

select table_name ,constraint_type ,constraint_name,
	constraint_schema 
from information_schema.table_constraints
where table_name ='listing_reviews'

select *
from information_schema.sequences

insert into listing_reviews (prop_id,prop_name,host_id,host_name,reviews_count)
with temp_reviews as(
	select rd.listing_id ,count(rd.id) as review_count
	from reviews_details rd 
	group by rd.listing_id 
)
select tr.listing_id ,l."name" as prop_name,
	l.host_id, l.host_name,tr.review_count
from temp_reviews tr
join listings l 
on l.id = tr.listing_id
where l."name" is not null and l.host_name is not null














