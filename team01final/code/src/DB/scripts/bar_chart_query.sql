
SELECT cluster, avg(polarity) 
from aspects2 
where id in 
(select aspectid from reviewaspects2 where reviewid in 
(select id from reviews where productid = 'B000068O48')) 
group by cluster
