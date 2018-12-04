const uuid = require('uuid/v4');
'use strict';
// var models = require('../models');
module.exports = (sequelize, DataTypes) => {
    var Product = sequelize.define('Product', {
        id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
        productId: { type: DataTypes.STRING, allowNull: false, unique: true },
        productParent: DataTypes.TEXT,
        productTitle: DataTypes.TEXT,
        productCategory: DataTypes.TEXT
    });

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

    return Product;
};
