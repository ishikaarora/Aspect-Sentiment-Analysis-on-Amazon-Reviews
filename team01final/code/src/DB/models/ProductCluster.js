const uuid = require('uuid/v4');
'use strict';
module.exports = (sequelize, DataTypes) => {
    var ProductCluster = sequelize.define('ProductCluster', {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true // Automatically gets converted to SERIAL for postgres
        },
    });

    ProductCluster.associate = function (models) {
        models.ProductCluster.belongsTo(models.Product, { foreignKey: 'productId' });
        models.ProductCluster.belongsTo(models.Cluster, { foreignKey: 'clusterId' });
    };

    return ProductCluster;
};
