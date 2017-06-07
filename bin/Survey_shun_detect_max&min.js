Qualtrics.SurveyEngine.addOnload(function () {
	/*Place Your JavaScript Here*/
    //--Parameters
    var Q_TARGET = 1; //The order of question of that page
    var MIN_NO = 2; //Retain n minimum value
    var MIN_THR = 15; //Only retain minimum value smaller than it

    //Acquire answer value and item text from previous question
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
    

    //--Item prototype
    function Item(text, value) {
        this.text = text;
        this.value = value;
    }

    //Initiate each item
    var items = [];
    for(i = 0; i < values.length; i++) {
        items[i] = new Item(texts[i], values[i]);
    }


    //--Acquire min (smallest n values)
    //Sort item by answer value
    items.sort(function(a, b){return a.value - b.value});
    mins = [];
    for(i = 0; i < MIN_NO; i++) {
        if(items[i].value > MIN_THR) {break;}
        mins[i] = items[i];
    }


    //--Acquire max
    items.reverse();
    max = items[0];


    //--Forge text to replace question text
    textReplaces = [];
    textReplaces[0] = "The max option is " + max.text;
    switch(mins[0]) {
        case undefined: //If the min values are filtered out then do not show
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

    //Concatenate the prepared texts
    var textReplace = ""
    for(i = 0; i < textReplaces.length; i++) {
        textReplace += textReplaces[i];
    }


    //--Impute the prepared texts as the question text
    var questionText = document.getElementsByClassName('QuestionText');
    questionText[Q_TARGET - 1].innerHTML = textReplace;
});

