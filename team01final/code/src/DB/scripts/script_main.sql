DECLARE @review NVARCHAR(MAX)
DECLARE @reviewId NVARCHAR(MAX)
DECLARE @aspectPairs NVARCHAR(MAX)
DECLARE @aspectPair NVARCHAR(MAX)
DECLARE @noun NVARCHAR(MAX)
DECLARE @adj NVARCHAR(MAX)
DECLARE @polarity FLOAT
DECLARE @rule INT
DECLARE @cluster NVARCHAR(MAX)
DECLARE @clusterId INT
DECLARE @aspectId INT
DECLARE @realReviewId NVARCHAR(MAX)
DECLARE @json VARCHAR(MAX)
DECLARE @ProductId NVARCHAR(MAX)

SELECT @json = BulkColumn
 FROM OPENROWSET (BULK '/dva-DB/DVA/r3.json', SINGLE_CLOB) as j

DECLARE C1 CURSOR 
  LOCAL STATIC READ_ONLY FORWARD_ONLY
FOR 
SELECT j2.[Key], j3.[Value] FROM OPENJSON(@json) j1
CROSS APPLY OPENJSON(j1.Value) j2
CROSS APPLY OPENJSON(j2.Value) j3

OPEN C1
FETCH NEXT FROM C1 INTO @ProductId, @Review
WHILE @@FETCH_STATUS = 0
BEGIN 
    -- Do Stuff Here
	SELECT @reviewId=Value FROM OPENJSON(@Review) j1
	WHERE [key] = 'review_id'
	SELECT @aspectPairs=Value FROM OPENJSON(@Review) j1
	WHERE [key] = 'aspect_pairs'

	SELECT @realReviewId=id FROM Reviews Where reviewId=@reviewId
	SELECT @realReviewId
	DECLARE C2 CURSOR 
	  LOCAL STATIC READ_ONLY FORWARD_ONLY
	FOR 
	SELECT Value FROM OPENJSON(@aspectPairs) j1


	OPEN C2
	FETCH NEXT FROM C2 INTO @aspectPair
	WHILE @@FETCH_STATUS = 0
	BEGIN 
		-- Do Stuff Here
		  SELECT @noun=JSON_VALUE(@aspectPair,'$.noun')
		 , @adj=JSON_VALUE(@aspectPair,'$.adj')
		 , @rule=JSON_VALUE(@aspectPair, '$.rule') 
		 , @polarity=JSON_VALUE(@aspectPair, '$.polarity')
		 , @cluster=JSON_VALUE(@aspectPair, '$.cluster')

		 --INSERT INTO Clusters(createdAt, updatedAt, name) VALUES(CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)), CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)), @cluster)
		 --SET @clusterId=@@IDENTITY
		 --SELECT @@IDENTITY		 
		 INSERT INTO Aspects2(noun, adjective, [rule], polarity, [cluster]) 
		 VALUES(@noun, @adj, @rule, @polarity, @cluster)
		 SET @aspectId=@@IDENTITY
		 INSERT INTO ReviewAspects2(reviewId, aspectId) VALUES(@realReviewId,@aspectId)
		 SELECT @aspectId, @@IDENTITY, @realReviewId
		 -- raiserror('Oh no a fatal error', 20, -1) with log
		 -- End of Stuff
		FETCH NEXT FROM C2 INTO @aspectPair
	END
	CLOSE C2
	DEALLOCATE C2
	-- End of Do Stuff Here
    FETCH NEXT FROM C1 INTO @ProductId, @Review
END
CLOSE C1
DEALLOCATE C1



--SET @Review = N'{"review_id": "R3ESIGAW4QQYAN", "aspect_pairs": [{"noun": "cord", "adj": "durable", "rule": 1, "polarity": 0.0, "cluster": "cord"}, {"noun": "angle", "adj": "right", "rule": 1, "polarity": 0.0, "cluster": "angle"}, {"noun": "product", "adj": "ok", "rule": 3, "polarity": 0.0, "cluster": "product"}, {"noun": "product", "adj": "easy", "rule": 3, "polarity": 0.0, "cluster": "product"}]}'

