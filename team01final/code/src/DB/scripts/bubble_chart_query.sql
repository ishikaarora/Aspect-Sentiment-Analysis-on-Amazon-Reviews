SELECT a.noun as Noun, a.cluster as Cluster, count(a.noun) as CountOfNouns, min(r.reviewBody) as Review
FROM Aspects2 AS a
INNER JOIN ReviewAspects2 AS ra ON a.Id=ra.aspectId
INNER JOIN Reviews AS r ON ra.reviewId=r.Id
INNER JOIN Products AS p ON r.productId=p.productId
WHERE p.productId= 'B000068O48'
GROUP BY a.noun, a.cluster
--FOR JSON AUTO

--SELECT a.noun as Noun, a.cluster as Cluster, r.reviewId
--FROM Aspects2 AS a
--INNER JOIN ReviewAspects2 AS ra ON a.Id=ra.aspectId
--INNER JOIN Reviews AS r ON ra.reviewId=r.Id
--INNER JOIN Products AS p ON r.productId=p.productId
--WHERE r.reviewId= 'R1JE9O80Z6D0E4'
-- 