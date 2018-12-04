const csv = require('csv-streamify')
var Parser = require('tsv').Parser
var TSV = new Parser("\t", { header: false })
var path = '/home/ec2-user/dva-DB/DVA/amazon_reviews_us_Electronics_v1_00.tsv';
var fs = require('fs')
    , es = require('event-stream');

var lineNr = 0;
var db = require('../db');
const uuid = require('uuid/v4');

async function hello() {
    var s = fs.createReadStream(path)
        .pipe(es.split())
        .pipe(es.mapSync(async function (line) {

            // pause the readstream
            s.pause();

            lineNr += 1;

            // process line here and call s.resume() when rdy
            // function below was for logging memory usage
            //console.log();
            item = TSV.parse(line)[0];
            // console.log(item);
            review = {
                id: uuid(),
                marketplace: item[0] + "",
                customerId: item[1] + "",
                reviewId: item[2] + "",                
                productId: item[3] + "",
                starRatin: item[7] + "",                
                helpfulVotes: item[8] + "",
                totalVotes: item[9] + "",
                vine: item[10] + "",
                verifiedPurchase: item[11] + "",
                reviewHeadline: item[12] + "",
                reviewBody: item[13] + "",
                reviewDate: item[14] + ""
            };
            var product = {
                productId: item[3] + "",
                productParent: item[4] + "",
                productTitle: item[5] + "",
                productCategory: item[6] + "",
            }
            //if (lineNr != 1) {
            //    
            //}
            // if (lineNr == 2) { process.exit(); }
            await db.addReview(review.reviewId, review, product);

            //logMemoryUsage(lineNr);

            // resume the readstream, possibly from a callback
            s.resume();
        })
            .on('error', function (err) {
                console.log('Error while reading file.', err);
            })
            .on('end', function () {
                console.log('Read entire file.')
            })
        );
}
hello();
// now pipe some data into it
//fs.createReadStream().pipe(parser)
