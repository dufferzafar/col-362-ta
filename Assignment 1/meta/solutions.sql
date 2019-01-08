-- 1) --

select type,count(PaperId) from Paper P,Venue V where P.VenueId=V.VenueId group by type;

-- 2) --

select avg(temp.authCnt) from (select count(*) as authCnt from PaperByAuthors group by PaperId);

-- 3) --

select Title from Paper P, PaperByAuthors PA where P.PaperId=PA.PaperId group by PA.PaperId having count(PA.AuthorId)>20 order by Title;

-- 4) --
(select distinct(name) from Author order by name) - (select distinct(A.name) from Author A,PaperByAuthors PA1, PaperByAuthors PA2 where A.AuthorId = PA1.AuthorId and PA1.PaperId=PA2.PaperId and PA1.AuthorId!=PA2.AuthorId order by A.name);

-- 5) --

select temp.name from (select A.name,count(PA.PaperId) as paper_count from Author A,PaperByAuthors PA where A.AuthorId=PA.AuthorId group by A.AuthorId order by paper_count desc,A.name asc) temp LIMIT 20;

-- 6) --

select distinct(A1.name) from (select PA.PaperId from Author A,PaperByAuthors PA where A.AuthorId = PA.AuthorId group by PA.PaperId having count(*)=1) temp,Author A1,PaperByAuthors PA1 where temp.PaperId=PA1.PaperId and A1.AuthorId = PA1.AuthorId group by PA1.AuthorId having count(*)>100 order by A1.name;

-- 7) --

(select distinct(name) from Author order by name) - (select distinct(A.name) from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId=PA.AuthorId and P.PaperId = PA.PaperId and V.VenueId = P.VenueId and V.type='journal' group by PA.AuthorId order by A.name);

-- 8) --

(select A.name from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId=PA.AuthorId and P.PaperId = PA.PaperId and V.VenueId = P.VenueId group by PA.AuthorId having V.type='journal' order by A.name);

-- 9) --

(select A.name from Author A,Paper P, PaperByAuthors PA where PA.AuthorId = A.AuthorId and P.PaperId = PA.PaperId where P.year = 2012 group by A.AuthorId having count(*)>=2) INTERSECT (select A.name from Author A,Paper P, PaperByAuthors PA where PA.AuthorId = A.AuthorId and P.PaperId = PA.PaperId where P.year = 2013 group by A.AuthorId having count(*)>=3) ;

-- 10) --

select temp.name from (select A.name,count(PA.PaperId) as paper_count from Author A,PaperByAuthors PA,Paper P,Venue V where A.AuthorId=PA.AuthorId and P.PaperId = PA.PaperId and V.VenueId = P.VenueId and V.type = 'journal' and V.name = 'corr' group by A.AuthorId order by paper_count desc) temp LIMIT 20;

-- 11) --
select distinct(A.name) from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journal' and V.name='amc' group by PA.AuthorId having count(*)>3 order by A.name asc;

-- 12) --
(select A.name from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journal' and V.name='ieicet' group by PA.AuthorId having count(*)>10 order by A.name asc) - (select A.name from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journal' and V.name='tcs' group by PA.AuthorId);


-- 13) --

select P.year,count(*) from Paper P,Venue V where P.VenueId = V.VenueId and V.name='DBLP' and P.year between 2004 and 2013 group by P.year;


-- 14 --

select count(distinct PA.AuthorId) from Paper P,PaperByAuthors PA where P.PaperId = PA.PaperId and 
lower(P.Title) LIKE "%query%optimization%";

-- 15 --

select temp.Title from ( select P.Title, count(*) as cnt from Paper P, Citation C where P.PaperId = C.Paper1Id group by C.Paper1Id) temp order by temp.cnt desc;

-- 16 --

select P.Title as cnt from Paper P, Citation C where P.PaperId = C.Paper1Id group by C.Paper1Id having count(*)>10 order by P.Title;


-- 17 --
select P.Title from (select Paper1Id,count(*) as cnt from Citation group by Paper1Id) cited,(select Paper2Id,count(*) as cnt from Citation group by Paper2Id) cites where P.PaperId = cited.id and cited.id = cites.id and cited.cnt-cites.cnt>10 order by P.Title;

-- 18 --

(select distinct Title from Paper order by Title) - (select P.Title from Paper P,Citation C where P.PaperId = C.Paper1Id order by Title);

-- 19 --

select distinct A.name from Author A,PaperByAuthors p1,PaperByAuthors p2,Citation C where C.Paper1Id = p1.PaperId and C.paper2Id = p2.paperId and A.AuthorId = p1.AuthorId and A.AuthorId = p2.AuthorId order by A.name;

-- 20 --


(select A.name from Author A, Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PaperByAuthors.PaperId and P.VenueId = V.VenueId and V.type='journal' and V.name='corr' and P.year between 2009 and 2013 order by A.name) - (select A.name from Author A, Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PaperByAuthors.PaperId and P.VenueId = V.VenueId and V.type='journal' and V.name='ieicet' and P.year=2019 order by A.name);

-- 21 --

-- TODO -- 


-- 22 --

select out.name,out.year from (select V.name, P.year ,count(*) as cnt from Paper P,Venue V where P.VenueId = V.VenueId group by (V.name,P.year) 
order by cnt desc) LIMIT 1;
