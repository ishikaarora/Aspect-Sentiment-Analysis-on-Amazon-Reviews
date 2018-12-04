const uuid = require('uuid/v4');
'use strict';
module.exports = (sequelize, DataTypes) => {
    var ReviewAspect = sequelize.define('ReviewAspect', {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true // Automatically gets converted to SERIAL for postgres
        },
    });

    ReviewAspect.associate = function (models) {
        models.ReviewAspect.belongsTo(models.Review, { foreignKey: 'reviewId'});
        models.ReviewAspect.belongsTo(models.Aspect, { foreignKey: 'aspectId' });
    };

    return ReviewAspect;
};
