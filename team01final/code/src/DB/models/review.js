const uuid = require('uuid/v4');
'use strict';
// var models = require('../models');
module.exports = (sequelize, DataTypes) => {
    var Review = sequelize.define('Review', {
        id: { type: DataTypes.UUID, primaryKey: true},
        marketplace: DataTypes.TEXT,
        customerId: DataTypes.TEXT,
        reviewId: DataTypes.TEXT,
        starRatin: DataTypes.TEXT,
        helpfulVotes: DataTypes.TEXT,
        totalVotes: DataTypes.TEXT,
        vine: DataTypes.TEXT,
        verifiedPurchase: DataTypes.TEXT,
        reviewHeadline: DataTypes.TEXT,
        reviewBody: DataTypes.TEXT,
        reviewDate: DataTypes.TEXT
    });

    Review.associate = function (models) {
        models.Review.belongsTo(models.Product, { foreignKey: 'productId', targetKey: 'productId'});
    };

    //marketplace',
    //'customer_id',
    //    'review_id',
    //    'product_id',
    //    'product_parent',
    //    'product_title',
    //    'product_category',
    //    'star_rating',
    //    'helpful_votes',
    //    'total_votes',
    //    'vine',
    //    'verified_purchase',
    //    'review_headline',
    //    'review_body',
    //    'review_date' ]

    return Review;
};
