--PREAMBLE--

create view authors_per_paper as (select PaperId,count(*) as cnt from PaperByAuthors group by PaperId);

create view papers_per_author as (select AuthorId,count(*) as cnt from PaperByAuthors group by AuthorId);

create view papers_in_2009 as (select V.VenueId, count(*) as cnt from Venue V,Paper P where P.VenueId=V.VenueId and V.type='journals' and P.year=2009 group by V.VenueId);

create view papers_in_2010 as (select V.VenueId, count(*) as cnt from Venue V,Paper P where P.VenueId=V.VenueId and V.type='journals' and P.year=2010 group by V.VenueId);
create view papers_in_2011 as (select V.VenueId, count(*) as cnt from Venue V,Paper P where P.VenueId=V.VenueId and V.type='journals' and P.year=2011 group by V.VenueId);
create view papers_in_2012 as (select V.VenueId, count(*) as cnt from Venue V,Paper P where P.VenueId=V.VenueId and V.type='journals' and P.year=2012 group by V.VenueId);
create view papers_in_2013 as (select V.VenueId, count(*) as cnt from Venue V,Paper P where P.VenueId=V.VenueId and V.type='journals' and P.year=2013 group by V.VenueId);

Create view num_papers_per_author_per_venue AS (select V.name as vname, A.name as aname,count(*) as cnt from Venue V,Author A,PaperByAuthors PA, Paper P where V.VenueId = P.VenueId and PA.AuthorId=A.AuthorId and P.PaperId=PA.PaperId and V.type='journals' group by A.name,V.name);

--1--

select type,count(PaperId) as cnt from Paper P,Venue V where P.VenueId=V.VenueId group by type order by cnt desc,type asc;

--2--

select avg(cnt) from authors_per_paper; 

--3--

select Title from Paper P,authors_per_paper temp where temp.cnt>20 and P.PaperId=temp.PaperId order by Title;

--4-- 

(select name from Author order by name) except (select A.name from Author A,PaperByAuthors PA1,authors_per_paper temp where A.AuthorId = PA1.AuthorId and PA1.PaperId=temp.PaperId and temp.cnt=1 order by A.name);

--5--

select temp1.name from (select A.name,temp.cnt 
from Author A,papers_per_author temp where A.AuthorId=temp.AuthorId order by temp.cnt desc,A.name asc) temp1 LIMIT 20;

--6--

select A.name from (select PA.AuthorId from authors_per_paper temp,PaperByAuthors PA where temp.cnt=1 and temp.PaperId = PA.PaperId group by PA.AuthorId having count(*)>50) temp1,Author A where temp1.AuthorId = A.AuthorId order by A.name;

--7--
(select distinct(name) from Author order by name) except (select distinct(A.name) from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId=PA.AuthorId and P.PaperId = PA.PaperId and V.VenueId = P.VenueId and V.type='journals' order by A.name);

--8-- 
(select distinct(A.name) from Author A,Paper P,PaperByAuthors PA,Venue V where P.PaperId=PA.PaperId and A.AuthorId=PA.AuthorId and P.VenueId=V.VenueId and V.type='journals' order by A.name) except 
(select distinct(A.name) from Author A,Paper P,PaperByAuthors PA,Venue V where P.PaperId=PA.PaperId and A.AuthorId=PA.AuthorId and P.VenueId=V.VenueId and V.type!='journals' order by A.name);

--9--

(select distinct(A.name) from Author A,Paper P, PaperByAuthors PA where PA.AuthorId = A.AuthorId and P.PaperId = PA.PaperId and P.year = 2012 group by A.AuthorId,A.name having count(*)>=2 order by A.name) INTERSECT (select distinct A.name from Author A,Paper P, PaperByAuthors PA where PA.AuthorId = A.AuthorId and P.PaperId = PA.PaperId and P.year = 2013 group by A.AuthorId,A.name having count(*)>=3 order by A.name) ;


--10--

select temp.name from (select A.name,count(PA.PaperId) as paper_count from Author A,PaperByAuthors PA,Paper P,Venue V where A.AuthorId=PA.AuthorId and P.PaperId = PA.PaperId and V.VenueId = P.VenueId and V.type = 'journals' and V.name = 'corr' group by A.AuthorId,A.name order by paper_count desc,A.name asc) temp LIMIT 20;

--11--
select distinct(A.name) from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='amc' group by PA.AuthorId,A.name having count(*)>3 order by A.name asc;

--12--
(select distinct A.name from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='ieicet' group by PA.AuthorId,A.name having count(*)>10 order by A.name asc) except (select distinct A.name from Author A,Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='tcs' group by PA.AuthorId,A.name);

--13--

select P.year,count(*) from Paper P,Venue V where P.VenueId = V.VenueId and P.year between 2004 and 2013 group by P.year order by P.year;

--14--

select count(distinct PA.AuthorId) from Paper P,PaperByAuthors PA where P.PaperId = PA.PaperId and 
lower(P.Title) LIKE '%query%optimization%';

--15--

select temp.Title from ( select P.Title, count(*) as cnt from Paper P, Citation C where P.PaperId = C.Paper2Id group by C.Paper2Id,P.Title) temp order by temp.cnt desc,temp.Title asc;

--16--

select P.Title as cnt from Paper P, Citation C where P.PaperId = C.Paper2Id group by C.Paper2Id,P.Title having count(*)>10 order by P.Title;


--17--
select P.Title from Paper P,(select Paper2Id as id,count(*) as cnt from Citation group by Paper2Id) cited,(select Paper1Id as id,count(*) as cnt from Citation group by Paper1Id) cites where P.PaperId = cited.id and cited.id = cites.id and (cited.cnt-cites.cnt)>=10 order by P.Title;

--18--

(select distinct Title from Paper order by Title) except (select P.Title from Paper P,Citation C where P.PaperId = C.Paper2Id order by Title);

--19--

select distinct A.name from Author A,PaperByAuthors p1,PaperByAuthors p2,Citation C where C.Paper1Id = p1.PaperId and C.paper2Id = p2.paperId and A.AuthorId = p1.AuthorId and A.AuthorId = p2.AuthorId order by A.name;

--20--

select temp.name from 
((select distinct A.name from Author A, Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='corr' and P.year between 2009 and 2013) except (select distinct A.name from Author A, Paper P,PaperByAuthors PA, Venue V where A.AuthorId = PA.AuthorId and P.PaperId = PA.PaperId and P.VenueId = V.VenueId and V.type='journals' and V.name='ieicet' and P.year=2009)) temp order by temp.name asc;

--21--

select V.name from Venue V,papers_in_2009 p1,papers_in_2010 p2,papers_in_2011 p3,papers_in_2012 p4 ,papers_in_2013 p5 where V.VenueId = p1.VenueId and p1.VenueId = p2.VenueId and p2.VenueId = p3.VenueId and p3.VenueId = p4.VenueId and p4.VenueId = p5.VenueId and p1.cnt>=p2.cnt and p2.cnt>=p3.cnt and p3.cnt >=p4.cnt and p4.cnt>=p5.cnt order by V.name;

--22--

select out.name,out.year from (select V.name, P.year ,count(*) as cnt from Paper P,Venue V where P.VenueId = V.VenueId group by (V.name,P.year) 
order by cnt desc) out LIMIT 1;

--23--

select t1.vname, t1.aname from num_papers_per_author_per_venue t1, (select vname, MAX(cnt) as mcnt from num_papers_per_author_per_venue GROUP BY vname) t2 where t1.vname = t2.vname and t1.cnt = t2.mcnt order by t1.vname, t1.aname; 

--24--

with numpublications as
(select Venue.name as name, count(*) as num_publications
from Paper join Venue on Paper.VenueId = Venue.VenueId
where Venue.type='journals' and (Paper.year=2007 or Paper.year=2008)
group by Venue.name),
numcitations as (select V.name as name, count(*) as num_citations from Venue V,Citation C,Paper P1,Paper P2 where V.type='journals' and V.venueid= P1.venueid and P1.year=2009 and P1.paperId=C.paper1id and P2.paperid = c.paper2id and (P2.year=2007 or P2.year=2008) group by V.name)
select np.name as journal_name, num_citations*1.0/num_publications as impact_value
from numpublications np,numcitations nc where num_publications>0 and np.name=nc.name
order by impact_value desc, journal_name asc;

--25--

select A.name from (select AuthorId, count(*)
from (SELECT PA.AuthorId, PA.PaperId, COUNT(c.Paper1Id) AS citations_count,
             rank() over (partition by PA.AuthorId, PA.PaperId order by count(c.Paper1Id) desc) as ranking
      FROM PaperByAuthors PA LEFT OUTER JOIN
           Citation c
           ON PA.PaperId = c.Paper2Id
      GROUP BY PA.AuthorId, PA.PaperId
     ) t
where ranking <= citations_count
group by AuthorId) final_res ,Author A where A.AuthorId = final_res.AuthorId order by A.name;


--CLEANUP--

drop view papers_per_author;
drop view authors_per_paper;
drop view papers_in_2009;
drop view papers_in_2010;
drop view papers_in_2011;
drop view papers_in_2012;
drop view papers_in_2013;
drop view num_papers_per_author_per_venue;
