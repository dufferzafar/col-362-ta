-- VIEWS --

create view authors_per_paper as (select PaperId,count(*) as cnt from PaperByAuthors group by PaperId);

create view papers_per_author as (select AuthorId,count(*) as cnt from PaperByAuthors group by AuthorId);

-- 1) --

select type,count(PaperId) as cnt from Paper P,Venue V where P.VenueId=V.VenueId group by type order by cnt desc,type asc;

-- 2) --

select avg(cnt) from authors_per_paper; 

-- 3) --

select Title from Paper P,authors_per_paper temp where temp.cnt>20 and P.PaperId=temp.PaperId order by Title;

-- 4) -- 

(select name from Author order by name) except (select A.name from Author A,PaperByAuthors PA1,authors_per_paper temp where A.AuthorId = PA1.AuthorId and PA1.PaperId=temp.PaperId and temp.cnt=1 order by A.name);

-- 5) --

select temp1.name from (select A.name,temp.cnt 
from Author A,papers_per_author temp where A.AuthorId=temp.AuthorId order by temp.cnt desc,A.name asc) temp1 LIMIT 20;

-- 6) --

select A.name from (select PA.AuthorId from authors_per_paper temp,PaperByAuthors PA where temp.cnt=1 and temp.PaperId = PA.PaperId group by PA.AuthorId having count(*)>10) temp1,Author A where temp1.AuthorId = A.AuthorId order by A.name;

-- 7) --
(select distinct(name) from Author order by name) except (select distinct(A.name) from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId=PA.AuthorId and P.PaperId = PA.PaperId and V.VenueId = P.VenueId and V.type='journals' order by A.name);

-- 8) -- 
(select distinct(A.name) from Author A,Paper P,PaperByAuthors PA,Venue V where P.PaperId=PA.PaperId and A.AuthorId=PA.AuthorId and P.VenueId=V.VenueId and V.type='journals' order by A.name) except 
(select distinct(A.name) from Author A,Paper P,PaperByAuthors PA,Venue V where P.PaperId=PA.PaperId and A.AuthorId=PA.AuthorId and P.VenueId=V.VenueId and V.type!='journals' order by A.name);

-- 9) --

(select distinct(A.name) from Author A,Paper P, PaperByAuthors PA where PA.AuthorId = A.AuthorId and P.PaperId = PA.PaperId and P.year = 2012 group by A.AuthorId,A.name having count(*)>=2 order by A.name) INTERSECT (select distinct A.name from Author A,Paper P, PaperByAuthors PA where PA.AuthorId = A.AuthorId and P.PaperId = PA.PaperId and P.year = 2013 group by A.AuthorId,A.name having count(*)>=3 order by A.name) ;


-- 10) --

select temp.name from (select A.name,count(PA.PaperId) as paper_count from Author A,PaperByAuthors PA,Paper P,Venue V where A.AuthorId=PA.AuthorId and P.PaperId = PA.PaperId and V.VenueId = P.VenueId and V.type = 'journals' and V.name = 'corr' group by A.AuthorId,A.name order by paper_count desc,A.name asc) temp LIMIT 20;

-- 11) --
select distinct(A.name) from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='amc' group by PA.AuthorId,A.name having count(*)>3 order by A.name asc;

-- 12) --
(select A.name from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='ieicet' group by PA.AuthorId,A.name having count(*)>10 order by A.name asc) except (select A.name from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='tcs' group by PA.AuthorId,A.name);


-- 13) --

select P.year,count(*) from Paper P,Venue V where P.VenueId = V.VenueId and P.year between 2004 and 2013 group by P.year order by P.year;

-- 14 --

select count(distinct PA.AuthorId) from Paper P,PaperByAuthors PA where P.PaperId = PA.PaperId and 
lower(P.Title) LIKE '%query%optimization%';

-- 15 --

select temp.Title from ( select P.Title, count(*) as cnt from Paper P, Citation C where P.PaperId = C.Paper2Id group by C.Paper2Id,P.Title) temp order by temp.cnt desc,P.Title asc;

-- 16 --

select P.Title as cnt from Paper P, Citation C where P.PaperId = C.Paper2Id group by C.Paper2Id,P.Title having count(*)>10 order by P.Title;


-- 17 --
select P.Title from Paper P,(select Paper2Id as id,count(*) as cnt from Citation group by Paper2Id) cited,(select Paper1Id as id,count(*) as cnt from Citation group by Paper1Id) cites where P.PaperId = cited.id and cited.id = cites.id and (cited.cnt-cites.cnt)>=10 order by P.Title;

-- 18 --

(select distinct Title from Paper order by Title) except (select P.Title from Paper P,Citation C where P.PaperId = C.Paper2Id order by Title);

-- 19 --

select distinct A.name from Author A,PaperByAuthors p1,PaperByAuthors p2,Citation C where C.Paper1Id = p1.PaperId and C.paper2Id = p2.paperId and A.AuthorId = p1.AuthorId and A.AuthorId = p2.AuthorId order by A.name;

-- 20 --

select temp.name from 
((select distinct A.name from Author A, Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='corr' and P.year between 2009 and 2013) except (select distinct A.name from Author A, Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='ieicet' and P.year=2009)) temp order by temp.name asc;

-- 21 --



-- 22 --

select out.name,out.year from (select V.name, P.year ,count(*) as cnt from Paper P,Venue V where P.VenueId = V.VenueId group by (V.name,P.year) 
order by cnt desc) out LIMIT 1;


-- DROP VIEWS --

drop view papers_per_author;
drop view authors_per_paper;
