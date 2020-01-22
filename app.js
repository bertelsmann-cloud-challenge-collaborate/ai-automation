var app = new Vue({
  el: '#app',
  data() {
    return {
      text: 'I feel bad that I neglected this project for so long',
      show: true,
      seen: false,
      ok: false,
      nok: false,
      sentiment : '',
      msg: '',
      dspSecs: 5,
      dspCntDwn: 0,
      id : 0,
      emotions: [
        { eid: 1, emo: 'fear' },
        { eid: 2, emo: 'guilt' },
        { eid: 3, emo: 'joy' },
        { eid: 4, emo: 'anger' },
        { eid: 5, emo: 'disgust' },
        { eid: 6, emo: 'sadness' },
        { eid: 7, emo: 'shame' }
      ]
    }
  },
  methods: {
    onSubmit(evt) {

      var review = $.trim($("#review").val());
      var json = {};
      json["review"]  = review;

      console.log(json);

      axios({
        "method": "POST",
        "url": "http://localhost:3000/getSentiment",
        "data": json,
        "headers": { "content-type": "application/json" }
      }).then(result => {
                    this.res = result.data;
          console.log(this.res);
                    console.log(this.res.classification);
          this.sentiment = this.res.classification;
          this.seen = true;
          this.id = this.res.id;

                }, error => {

                    console.error(error);
            });

    },
    reclassify(sentiment) {

      var json = {};
          //json["id"] = this.id;
          json["sentiment"]  = this.sentiment;
          console.log(json);

      axios({
        "method": "POST",
        "url": "http://localhost:3000/setSentiment",
        "data": json,
        "headers": { "content-type": "application/json" }
      }).then(result => {
                    this.res = result.data;
                    console.log(this.res.payload);
                    this.ok = true;
                    this.msg = 'Reclassification result succesfully revised.';
                    this.dspCntDwn = this.dspSecs;

                }, error => {

                    console.error(error);
                    this.nok = true;
                    this.msg = 'Error ... Reclassification result has not been revised.';
                    this.dspCntDwn = this.dspSecs;

            });

       },
       approve(){
         var json = {};
            //json["id"] = this.id;
            console.log(json);

        axios({
          "method": "POST",
          "url": "http://localhost:3000/approveSentiment",
          "data": json,
          "headers": { "content-type": "application/json" }
        }).then(result => {
                      this.res = result.data;
                      console.log(this.res.payload);
                      this.ok = true;
                      this.msg = 'Acceptance successfully approved.';
                      this.dspCntDwn = this.dspSecs;

                  }, error => {

                      console.error(error);
                      this.nok = true;
                      this.msg = 'Error ... Acceptance has not been approved.';
                      this.dspCntDwn = this.dspSecs;
              });

        },
        dspCntDwnChg(dspCntDwn) {
          this.dspCntDwn = dspCntDwn
        }
 }
});
