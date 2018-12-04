USE DVA;  
GO  

--CREATE TABLE ReviewsFull   
--(
--marketplace nvarchar(MAX) NULL,  
--customer_id nvarchar(MAX) NULL,  
--review_id nvarchar(MAX) NULL,  
--product_id nvarchar(MAX) NULL,  
--product_parent nvarchar(MAX) NULL,  
--product_title nvarchar(MAX) NULL, 
--product_category nvarchar(MAX) NULL,  
--star_rating nvarchar(MAX) NULL,  
--helpful_votes nvarchar(MAX) NULL,  
--total_votes nvarchar(MAX) NULL,  
--vine nvarchar(MAX) NULL, 
--verified_purchase nvarchar(MAX) NULL,  
--review_headline nvarchar(MAX) NULL,  
--review_body nvarchar(MAX) NULL,  
--review_date nvarchar(MAX) NULL
--);  
--GO

BULK INSERT ReviewsFull
FROM '/dva-DB/DVA/amazon_reviews_us_Electronics_v1_00.tsv'
WITH (
  DATAFILETYPE = 'char',
  FIELDTERMINATOR = '\t',
  ROWTERMINATOR = '0x0a'
);
 
INSERT INTO Products(createdAt, updatedAt, productId, productTitle, productCategory)
Select 
CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)) AS createdAt,
CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)) AS updatedAt,
CAST(product_id AS nvarchar(255)) AS productId, 
product_title AS productTitle, 
product_category AS productCategory
from ReviewsFull 
GROUP BY product_id, product_title, product_category

INSERT INTO Reviews(Id, createdAt, updatedAt, marketplace, customerId, reviewId, starRatin, helpfulVotes, 
totalVotes, vine, verifiedPurchase, reviewHeadline, reviewBody, reviewDate, productId)
Select
NEWID() AS Id,
CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)) AS createdAt,
CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)) AS updatedAt,
marketplace AS marketplace,
customer_Id AS customerId,
review_Id AS reviewId,
star_rating AS starRatin,
helpful_votes AS helpfulVotes, 
total_votes AS totalVotes, 
vine AS vine,
verified_purchase AS verifiedPurchase,
review_headline AS reviewHeadline,
review_body AS reviewBody,
review_date AS reviewDate,
CAST(product_id AS nvarchar(255)) AS productId
FROM ReviewsFull 

Select count(*) from Products
Select count(*) from Reviews
--delete from products;
--delete from Reviews
 
--SELECT NEWID()

--INSERT INTO Products VALUES('a','b','c','d',CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)),CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)));

--DELETE FROM Products

--SELECT CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7))

--INSERT INTO JACK VALUES(CAST('11-24-2018 6:10:00 PM' AS datetimeoffset(7)))

--CREATE TABLE Jack
