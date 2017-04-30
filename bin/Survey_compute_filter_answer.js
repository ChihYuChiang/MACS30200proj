Qualtrics.SurveyEngine.addOnload(function () {
	/*Place Your JavaScript Here*/
 
    var scores = [
        Number("${q://QID8/SelectedChoicesRecode}"),
        Number("${q://QID9/SelectedChoicesRecode}"),
        Number("${q://QID10/SelectedChoicesRecode}"),
        Number("${q://QID11/SelectedChoicesRecode}"),
        Number("${q://QID12/SelectedChoicesRecode}"),
        Number("${q://QID13/SelectedChoicesRecode}"),
        Number("${q://QID14/SelectedChoicesRecode}"),
        Number("${q://QID15/SelectedChoicesRecode}"),
        Number("${q://QID16/SelectedChoicesRecode}"),
        Number("${q://QID17/SelectedChoicesRecode}"),
        Number("${q://QID18/SelectedChoicesRecode}"),
        Number("${q://QID19/SelectedChoicesRecode}"),
        Number("${q://QID20/SelectedChoicesRecode}"),
        Number("${q://QID21/SelectedChoicesRecode}"),
        Number("${q://QID22/SelectedChoicesRecode}"),
        Number("${q://QID23/SelectedChoicesRecode}"),
        Number("${q://QID24/SelectedChoicesRecode}"),
        Number("${q://QID25/SelectedChoicesRecode}"),
        Number("${q://QID26/SelectedChoicesRecode}"),
        Number("${q://QID27/SelectedChoicesRecode}"),
        Number("${q://QID28/SelectedChoicesRecode}"),
        Number("${q://QID29/SelectedChoicesRecode}"),
        Number("${q://QID30/SelectedChoicesRecode}"),
        Number("${q://QID31/SelectedChoicesRecode}"),
        Number("${q://QID32/SelectedChoicesRecode}"),
        Number("${q://QID33/SelectedChoicesRecode}"),
        Number("${q://QID34/SelectedChoicesRecode}"),
        Number("${q://QID35/SelectedChoicesRecode}"),
        Number("${q://QID36/SelectedChoicesRecode}"),
        Number("${q://QID37/SelectedChoicesRecode}"),
        Number("${q://QID38/SelectedChoicesRecode}"),
        Number("${q://QID39/SelectedChoicesRecode}"),
        Number("${q://QID40/SelectedChoicesRecode}"),
        Number("${q://QID41/SelectedChoicesRecode}"),
        Number("${q://QID42/SelectedChoicesRecode}"),
        Number("${q://QID43/SelectedChoicesRecode}"),
        Number("${q://QID44/SelectedChoicesRecode}"),
        Number("${q://QID45/SelectedChoicesRecode}"),
        Number("${q://QID46/SelectedChoicesRecode}"),
        Number("${q://QID47/SelectedChoicesRecode}"),
        Number("${q://QID123/SelectedChoicesRecode}"),
        Number("${q://QID124/SelectedChoicesRecode}"),
        Number("${q://QID125/SelectedChoicesRecode}"),
        Number("${q://QID126/SelectedChoicesRecode}"),
        Number("${q://QID127/SelectedChoicesRecode}"),
        Number("${q://QID128/SelectedChoicesRecode}"),
        Number("${q://QID129/SelectedChoicesRecode}"),
        Number("${q://QID130/SelectedChoicesRecode}"),
        Number("${q://QID131/SelectedChoicesRecode}"),
        Number("${q://QID132/SelectedChoicesRecode}")
    ];

    var score_all = 0
    function computeScore(score) {
        var score_recode = 0;
        if (score==1) {
            score_recode = 1;
        }
        score_all += score_recode;
    }
    scores.forEach(computeScore, this);

    Qualtrics.SurveyEngine.addEmbeddedData(
    "filterScore",
    score_all);

});