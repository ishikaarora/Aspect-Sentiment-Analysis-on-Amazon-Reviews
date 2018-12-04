
SELECT top(500) productid, avg(cast(starRatin as float)), avg((polarity + 2)*5/3) from reviews as r inner join reviewaspects2 as ra on r.id = ra.reviewid inner join aspects2 as a on ra.aspectid = a.id group by r.productid
Go
