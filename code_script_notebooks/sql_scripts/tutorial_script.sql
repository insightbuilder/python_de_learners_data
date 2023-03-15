/*This is a comment*/

select *
from information_schema.tables
where table_schema ='public'


/*from the table first */

select ld.id, ld.host_id ,ld."name" as listing_name,
	ld.description ,ld.neighbourhood ,ld.review_scores_rating ,
	ld.city 
from listing_details ld 
limit 5

/*creating views */

create view listing_view as
select ld.id ,ld.host_id ,ld."space" as rent_space,  ld.summary 
from listing_details ld 

/*creating table as select */

create table reviewer_table as
select rd.listing_id ,rd.id ,rd."comments" as review_comments,
rd.reviewer_name 
from reviews_details rd 

/* common table expression */
with listing_cte as (
	select l.id , l.host_id ,l.room_type ,l.price 
	from listings l 
)
select lc.id, lc.host_id, lc.room_type , lc.price,
	ld."space" as listingSpace, ld.description 
from listing_cte lc
join listing_details as ld 
on ld.id = lc.id
limit 5

/*Subqueries needs to be avoided*/

select *
from calendar c 
limit 5

select to_date(c."date",'YYYY-MM-DD') as day_date, count(c.listing_id) 
from calendar c 
group by to_date(c."date",'YYYY-MM-DD')
limit 5

select day_date, count(listing_id) 
from (
	select to_date(c."date",'YYYY-MM-DD') as day_date, c.listing_id ,c.price  
	from calendar c 
) sq
group by day_date
limit 5












