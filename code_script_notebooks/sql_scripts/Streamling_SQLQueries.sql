/*
 * Lets begin by seeing what is there inside the Database metadata
 */
select *
from information_schema.tables
where table_schema = 'public'

/*
 * Lets start with the CTAS on the largest table... listing_details
 */

select *
from listing_details ld 
limit 5

/*
 * Select only five columns that is related to reviews 
 */

drop table if exists listing_neigh

create table listing_neigh as
select ld.id, ld.summary, ld.description ,ld.neighborhood_overview 
from listing_details ld


/* Lets create views */

drop view if exists review_listing

create view review_listing as
select ld.id ,ld.host_id ,ld.review_scores_rating , ld.review_scores_accuracy ,
ld.review_scores_checkin , ld.review_scores_value ,
ld.review_scores_communication , ld.review_scores_location 
from listing_details ld 

select avg(rl.review_scores_rating) as avg_rating, 
	count(rl.review_scores_accuracy) as num_reviews,
	rl.host_id
from review_listing rl 
group by rl.host_id
having count(rl.review_scores_accuracy) > 10


select round(avg(rl.review_scores_rating)::numeric ,1) as avg_rating, 
	count(rl.review_scores_accuracy) as num_reviews,
	rl.host_id
from review_listing rl 
group by rl.host_id
having count(rl.review_scores_accuracy) > 10

/* Selecting from CTAS table */

select ln2.id , ln2.description 
from listing_neigh ln2 
limit 5

/* Selecting from views */

select rl.review_scores_rating , rl.review_scores_checkin 
from review_listing rl 
limit 5

/* Starting CTEs */

with cte_review as(
	select rd.listing_id ,rd."date" as review_date,
	rd.reviewer_name ,rd.reviewer_id 
	from reviews_details rd 
)
select cr.listing_id, cr.review_date
from cte_review as cr
limit 5

/* Subqueries */

select * from (
	select l.id , l.host_id ,l.host_name ,l.price 
	from listings l 
	where l.id > 2800
) as sq
where sq.host_id = 59484

/* inner join */

/* Lets make some preparations */

select rd.listing_id , rd.reviewer_id ,rd.reviewer_name 
from reviews_details rd 
limit 5

select ld.id ,ld.host_id ,ld."name" as listing_name
from listing_details ld 
limit 5

/* we can join these two tables on listing id */

select rd.listing_id ,rd.reviewer_id ,rd.reviewer_name ,
ld.host_id ,ld."name" as listing_name
from reviews_details rd 
inner join listing_details ld 
on rd.listing_id = ld.id 
limit 5

/*Inner Join – Returns matching data from both tables.

Full outer join – Returns matching data and unmatched data from both tables.

Left outer join or Left join – Returns matching data from both the tables 
and all the unmatched data from the left table.

 Right outer join or Right join – Returns matching data from both the
  tables and all the unmatched data from the right table.
*/

select count(*) as daily_booking, cq.day_date 
from (
	select to_date(c."date",'YYYY-MM-DD') as day_date, c.listing_id, 
	c.available, c.price
	from calendar c
	where c.available = 'f'
) cq
group by cq.day_date
order by count(*) desc 


select c.listing_id,
	count(c.listing_id) as times_booked
from calendar c
where c.available = 'f'
group by c.listing_id 
limit 5



























