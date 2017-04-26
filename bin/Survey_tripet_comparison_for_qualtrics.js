Qualtrics.SurveyEngine.addOnload(function (){
	
	//--Hide proceed button
	this.hideNextButton();


	//--Onclick answer, click next page button, with a small delay
	this.questionclick = function (event, element){
        //for a single answer multiple choice question, the element type will be radio
        if (element.type == 'radio')
        {	
			var that = this;
			(function(){that.clickNextButton();}).delay(0.1);
        }
    }


	//--(kk) The looped game from loop field
	var kk = "${lm://Field/1}";
	//Remove space and line break
	kk = kk.trim();


	//--(kk1) Get chosen games from embedded data
	var arr = "${e://Field/playedGames}";
	var arr1 = arr.toString();
	var kk1 = arr1.split(",");


	//--Shuffle chosen game order if this is the first triplet
	function shuffle(a){
		var j, x, i;
		for (i = a.length; i; i--){
			j = Math.floor(Math.random() * i);
			x = a[i - 1];
			a[i - 1] = a[j];
			a[j] = x;
		}
	}

	//Acquire current triplet count
	var times = "${e://Field/tripletTimes}";
	times = parseInt(times); //Convert str to int
	if (times == 1){
		shuffle(kk1);
		Qualtrics.SurveyEngine.addEmbeddedData("playedGames", kk1.toString());
	}


	//--Decide current game index within the chosen games
	var index;
	var array = [];
	for (var i = 0; i < kk1.length; i++){
		if (kk1[i].trim() == kk){
			index = i;
		}
		//Also tidy up the chosen game list
		array.push(kk1[i].trim());
	}


	//--Compute the games to be compared
	var start;
	var gap;
	if (index > -1) {
		var forSwitch;
		if (times <= 5) {
			forSwitch = 1;
		} else if (times <= 10) {
			forSwitch = 2;
		} else if (times <= 15) {
			forSwitch = 3;
		} else if (times <= 20) {
			forSwitch = 4;
		} else if (times <= 25) {
			forSwitch = 5;
		} else if (times <= 30) {
			forSwitch = 6;
		}
		switch (forSwitch) {
			case 1:
				start = (index + 3) % 5;
				gap = (index + 4) % 5;
				break;
			case 2:
				start = (index + 2) % 5;
				gap = (index + 4) % 5;
				break;
			case 3:
				start = (index + 1) % 5;
				gap = (index + 3) % 5;
				break;
			case 4:
				start = (index + 1) % 5;
				gap = (index + 2) % 5;
				break;
			case 5:
				start = (index + 2) % 5;
				gap = (index + 3) % 5;
				break;
			case 6:
				start = (index + 1) % 5;
				gap = (index + 4) % 5;
				break;
		}


		//--Get choice obj and Set choice text
		var choices = document.getElementsByClassName('SingleAnswer');
		choices[choices.length - 2].innerHTML = array[start];
		choices[choices.length - 1].innerHTML = array[gap];
	}
	

	//--Record what games are compared in each triplet
	Qualtrics.SurveyEngine.addEmbeddedData(
		"triplet" + times,
		this.getQuestionInfo().QuestionID + ", " + array[index] + ", " + array[start] + ", " + array[gap]
	);


	//--Counting triplet time
	Qualtrics.SurveyEngine.addEmbeddedData("tripletTimes", times + 1);

});
