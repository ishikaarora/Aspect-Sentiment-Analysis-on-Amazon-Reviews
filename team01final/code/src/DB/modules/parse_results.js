var fs = require('fs'),
  JSONStream = require('JSONStream'),
  es = require('event-stream');
var db = require('../db')

var clusters = {};
var aspects = {};
var count = 0;
var getStream = function () {
    var jsonData = '../results_file_4L.json',
        stream = fs.createReadStream(jsonData, {encoding: 'utf8'}),
        parser = JSONStream.parse('*');
        return stream.pipe(parser);
};

async function asyncForEach(array, callback) {
  for (let index = 0; index < array.length; index++) {
    await callback(array[index], index, array);
  }
}

async function test() {
	getStream()
  .pipe(await es.mapSync(async function (data) {
    var productId = Object.keys(data)[0];
	var reviews = data[productId];
    console.log(productId);
	await asyncForEach(reviews,async function(review) {
		console.log(count++);
		var reviewId = review.review_id;
		var aspectPairs = review.aspect_pairs;
		await asyncForEach(aspectPairs, async function(aspectPair) {
			var cluster = aspectPair.cluster;
			var clusterId, aspectId;
			if (cluster in clusters) {
				clusterId = clusters[cluster];
			} else {
				clusterId = await db.addCluster(cluster);
//				console.log(count++);
				clusters[cluster] = clusterId;
				// Insert in db
				// Insert fetched clusterId in clusters {cluster: clusterId}
			}
			var key = aspectPair.noun+','+aspectPair.adj+','+aspectPair.rule+','+aspectPair.polarity;
			if (key in aspects) {
				aspectId = aspects[key]
			} else {
				aspectId = await db.addAspect(aspectPair.noun, aspectPair.adj, aspectPair.polarity, clusterId);
				// console.log(count++);
				aspects[key] = aspectId;
				// Insert in db
				// Insert fetched clusterId in clusters {key: aspectId}
			}
			// insert clusterId, productId
			// insert reviewId, aspectId
			await db.addReviewAspect(reviewId, aspectId);
			
			console.log(aspectPair);
		});
	});
	console.log(clusters);
	console.log(aspects);
  }));
}

test();