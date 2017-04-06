Qualtrics.SurveyEngine.addOnload(function () {
	/*Place Your JavaScript Here*/

	var start;
	var gap;
	var index;
	var kk = "${lm://Field/1}";
	kk = kk.trim();
	var arr = "${e://Field/xx}";
	console.log("arr", arr);
	var arr1 = arr.toString();
	//console.log("arr1",arr1);
	var kk1 = arr1.split(",");
	var array = [];
	var times = "${e://Field/times}"
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
				gap = (index + 4) % 5;
				break;
			case 4:
				start = (index + 2) % 5;
				gap = (index + 3) % 5;
				break;
			case 5:
				start = (index + 1) % 5;
				gap = (index + 2) % 5;
				break;
			case 6:
				start = (index + 1) % 5;
				gap = (index + 3) % 5;
				break;
		}
		console.log(array[index] + "," + array[start] + ", " + array[gap]);

		var kkk = document.getElementsByClassName('ques_choices');
		kkk[kkk.length - 2].innerHTML = array[start];
		kkk[kkk.length - 1].innerHTML = array[gap];
	}
	console.log("kkk", kkk[kkk.length - 2].innerHTML);

	Qualtrics.SurveyEngine.addEmbeddedData("times", times + 1);

});