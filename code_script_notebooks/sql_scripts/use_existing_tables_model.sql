/*Idea is to use the existing table and model the data*/

select table_name ,constraint_name ,constraint_type,table_schema  
from information_schema.table_constraints
where table_schema ='public'

alter table listings 
add constraint list_pk primary key (id) 


alter table reviews_details 
add constraint rev_pk primary key (id)

drop foreign key 

alter table calendar 
add foreign key (listing_id)
references listings(id)

alter table listing_details 
add foreign key (id)
references listings(id)

alter table reviews_details  
add foreign key (listing_id)
references listings(id)

select n.*
from neighbourhood n 

alter table neighbourhood 
add constraint neigh_pk primary key (neighbourhood)

alter table listing_details  
add foreign key (neighbourhood_cleansed)
references neighbourhood(neighbourhood)

alter table listings
add foreign key (neighbourhood)
references neighbourhood(neighbourhood)


select distinct(ld.neighbourhood_cleansed)
from listing_details ld 

alter table reviews 
add foreign key (listing_id)
references listings(id)

alter table listings 
drop constraint list_pk cascade

alter table reviews_details  
drop constraint rev_pk cascade

alter table neighbourhood 
drop constraint neigh_pk cascade
