'use strict';
var express = require('express');
var router = express.Router();
const db  = require('../db')

/* GET users listing. */
router.get('/', function (req, res) {
    console.log('Hi');
    res.send('respond with a resource');
});

router.get('/product/:prodId', async function (req, res) {
  // res.send(req.params.prodId)
    var data1 = await db.product(req.params.prodId);
    var data2 = await db.bar(req.params.prodId);
    var title = await db.title(req.params.prodId);
    res.send({"title": title, "bubble": data1, "bar":data2});
});

module.exports = router;
