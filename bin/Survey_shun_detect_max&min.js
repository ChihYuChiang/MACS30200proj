Qualtrics.SurveyEngine.addOnload(function () {
	/*Place Your JavaScript Here*/
    var Q_TARGET = 1;
    var MIN_NO = 2;
    var MIN_THR = 15;
    var values = [
        "${q://QID1/ChoiceNumericEntryValue/1}",
        "${q://QID1/ChoiceNumericEntryValue/2}",
        "${q://QID1/ChoiceNumericEntryValue/3}",
        "${q://QID1/ChoiceNumericEntryValue/4}",
        "${q://QID1/ChoiceNumericEntryValue/5}"];
    var texts = [
        "${q://QID1/ChoiceDescription/1}",
        "${q://QID1/ChoiceDescription/2}",
        "${q://QID1/ChoiceDescription/3}",
        "${q://QID1/ChoiceDescription/4}",
        "${q://QID1/ChoiceDescription/5}"];

    function Item(text, value) {
        this.text = text;
        this.value = value;
    }

    var items = [];
    for(i = 0; i < values.length; i++) {
        items[i] = new Item(texts[i], values[i]);
    }

    items.sort(function(a, b){return a.value - b.value});
    mins = [];
    for(i = 0; i < MIN_NO; i++) {
        if(items[i].value > MIN_THR) {break;}
        mins[i] = items[i];
    }

    items.reverse();
    max = items[0];

    textReplaces = [];
    textReplaces[0] = "The max option is " + max.text;
    switch(mins[0]) {
        case undefined:
            textReplaces[1] = "";
            break;
        default:
            textReplaces[1] = "<br>The min option is " + mins[0].text;
    }
    switch(mins[1]) {
        case undefined:
            textReplaces[2] = "";
            break;
        default:
            textReplaces[2] = "<br>The second min option is " + mins[1].text;
    }

    var textReplace = ""
    for(i = 0; i < textReplaces.length; i++) {
        textReplace += textReplaces[i];
    }

    var questionText = document.getElementsByClassName('QuestionText');
    questionText[Q_TARGET - 1].innerHTML = textReplace;
});

