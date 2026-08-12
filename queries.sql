SELECT *
FROM educator as e
INNER JOIN qualifications as q
WHERE e.id = q.educator_id
AND e.adt = "ΑΜ327077"
GROUP BY e.adt
HAVING count(*) > 1


-- FIND DUPLICATE POSITIONS
select qq.specialization, ee.*, qq.* 
from educator as ee 
inner join qualifications as qq
where ee.id in (
    SELECT e.id
    FROM educator as e
    INNER JOIN qualifications as q
    WHERE e.id = q.educator_id
    GROUP BY e.adt
    HAVING count(*) > 1
) 
AND ee.id = qq.educator_id
AND ee.adt = "ΑΜ327077"
Order By ee.adt;

select * from educator;



select q.specialization, e.*, q.*
from educator as e 
inner join qualifications as q
where
    e.id = q.educator_id
    AND lastname = "ΚΑΡΑΚΩΣΤΑ" ;

-- TRUNCATE TABLES
truncate table educator;
truncate table qualifications;