Qualtrics.SurveyEngine.addOnload(function () {
	/*Place Your JavaScript Here*/
	
	//Onclick answer
	this.hideNextButton();
	this.questionclick = function(event, element){
        //for a single answer multiple choice question, the element type will be radio
        if (element.type == 'radio')
        {	
			var that = this;
			(function(){that.clickNextButton();}).delay(0.1);
        }
    }

	var start;
	var gap;
	var index;
	var kk = "${lm://Field/1}";
	kk = kk.trim();
	var arr = "${e://Field/playedGames}";
	console.log("arr", arr);
	var arr1 = arr.toString();
	//console.log("arr1",arr1);
	var kk1 = arr1.split(",");
	var array = [];
	var times = "${e://Field/tripletTimes}"
	for (var i = 0; i < kk1.length; i++) {
		if (kk1[i].trim() == kk) {
			index = i;
		}
		array.push(kk1[i].trim());
	}
	console.log(array);
	if (index > -1) {
		var forSwitch;
		times = parseInt(times);
		//console.log("times="+times);
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
		console.log(array[index] + ", " + array[start] + ", " + array[gap]);

		var choices = document.getElementsByClassName('SingleAnswer');
		choices[choices.length - 2].innerHTML = array[start];
		choices[choices.length - 1].innerHTML = array[gap];
	}
	
	Qualtrics.SurveyEngine.addEmbeddedData(
		"triplet" + times,
		this.getQuestionInfo().QuestionID + ", " + array[index] + ", " + array[start] + ", " + array[gap]
	);

	Qualtrics.SurveyEngine.addEmbeddedData("tripletTimes", times + 1);

});