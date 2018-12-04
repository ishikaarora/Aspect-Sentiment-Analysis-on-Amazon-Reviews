'use strict';
var Sequelize = require('sequelize');
var models = require('./models');
const uuid = require('uuid/v4');
models.sequelize.sync();
const sequelize = models.sequelize;


const Review = models.Review;
const ProductCluster = models.ProductCluster;
const Cluster = models.Cluster;
const Aspect = models.Aspect;
const ReviewAspect = models.ReviewAspect;
const Product = models.Product;

async function addCluster(name) {
    // return clusterId
    var cluster = await Cluster.findOrCreate({
        where: {
            name: name
        },
        defaults: {
            name: name
        }
    });
    return cluster[0].id;
}

async function addAspect(noun, adjective, polarity, clusterId) {
    // return clusterId
    var aspect = await Aspect.findOrCreate({
        where: {
            noun: noun,
            adjective: adjective,
            polarity: polarity,
	    clusterId: clusterId
        },
        defaults: {
            noun: noun,
            adjective: adjective,
            polarity: polarity,
	    clusterId: clusterId
        }
    });
    return aspect[0].id;
}

async function addReviewAspect(reviewId, aspectId) {
    // return clusterId
    var review  = await Review.findOne({where :{reviewId: reviewId}});
    var id = review.dataValues.id;
    var reviewAspect =  await ReviewAspect.findOrCreate({
        where: {
            reviewId: id,
            aspectId: aspectId
        },
        defaults: {
            reviewId: id,
            aspectId: aspectId
        }
    });
    return reviewAspect[0].id;
}

async function addProductCluster(productId, clusterId) {
    // return clusterId
    return await ProductCluster.findOrCreate({
        where: {
            productId: productId,
            clusterId: clusterId
        },
        defaults: {
            productId: productId,
            clusterId: clusterId
        }
    })[0].id;
}

async function addReview(reviewId, review, product) {
    //console.log(review);
    var productId = await addProduct(product);
    var review = await Review.findOrCreate({
            where: {
                reviewId: reviewId
            },
            defaults: review
    });
    return review[0].id;
}

async function addProduct(product) {
    //console.log(review);
    var product = await Product.findOrCreate({
        where: {
            productId: product.productId
        },
        defaults: product
    });
    return product[0].id;
}

async function product(productId) {
    await models.sequelize.sync();
    /* 'SELECT a.noun as Noun, a.cluster as Cluster, count(a.noun) as CountOfNouns, min(r.reviewBody) as Review ' + 
      'FROM Aspects2 AS a ' +
      'INNER JOIN ReviewAspects2 AS ra ON a.Id=ra.aspectId ' +
      'INNER JOIN Reviews AS r ON ra.reviewId=r.Id ' +
      'INNER JOIN Products AS p ON r.productId=p.productId ' +
      'WHERE p.productId= :pId ' +
      'GROUP BY a.noun, a.cluster', */
    var values = sequelize.query('SELECT a.noun as Noun, a.cluster as Cluster, count(a.noun) as CountOfNouns, min(r.reviewBody) as Review ' + 
      'FROM Aspects2 AS a ' +
      'INNER JOIN ReviewAspects2 AS ra ON a.Id=ra.aspectId ' +
      'INNER JOIN Reviews AS r ON ra.reviewId=r.Id ' +
      'INNER JOIN Products AS p ON r.productId=p.productId ' +
      'WHERE p.productId= :pId ' +
      'GROUP BY a.noun, a.cluster',      
      { replacements: { pId : productId }, type: sequelize.QueryTypes.SELECT });      
      return values;
}

async function bar(productId) {
    await models.sequelize.sync();
    /* 	SELECT cluster, avg(polarity) as polarity
       	from aspects2
       	where id in
	(select aspectid from reviewaspects2 where reviewid in
	(select id from reviews where productid = 'B000068O48'))
	group by cluster */

    var values = sequelize.query('SELECT cluster, avg(polarity) as polarity ' +
      	'FROM Aspects2 WHERE id IN ' +
       	'(SELECT aspectid FROM ReviewAspects2 WHERE reviewId in ' +
	'(SELECT id FROM reviews WHERE productId= :pId )) ' +
	'GROUP BY cluster',
	{ replacements : { pId: productId }, type: sequelize.QueryTypes.SELECT });
    return values;
}

async function title(productId) {
    await models.sequelize.sync();
    var values = sequelize.query('SELECT productTitle ' + 
	'FROM products where productId= :pId',
	{ replacements: { pId: productId }, type: sequelize.QueryTypes.SELECT });
     return values;
}

module.exports = {
    addReview: addReview,
    addProductCluster: addProductCluster,
    addReviewAspect: addReviewAspect,
    addCluster: addCluster,
    addAspect: addAspect,
    product: product,
    bar: bar,
    title: title
}
