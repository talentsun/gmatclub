/*
 * Question Javascript Library v 1.0.0
 * need jQuery support
 */
(function() {
	console.log('Question Library Loaded!');
	
	var Question = {
		version: '1.0.0',
		display: undefined,
		enable: undefined,
		disable: undefined,
		getSelectedOptions: undefined,
		getOptions: undefined,
		getCorrectOptions: undefined
	};

	if (typeof module !== 'undefined' && module.exports) {
		module.exports = Question;
	} else if (typeof define === 'function' && define.amd) {
		define(function(){return Question;});
	} else {
		(function(){ return this || (0,eval)('this'); }()).Question = Question;
	}

	Question.display = function(id) {
		$('#question').load('question.html');

		this.current_question_id_ = id;
	};

	Question.enable = function() {
		$('#question .option input[type="radio"]').removeAttr('disabled');
	};

	Question.disable = function() {
		$('#question .option input[type="radio"]').attr('disabled', 'disabled');
	};

	Question.getSelectedOptions = function() {
		return $('#question .option input[type="radio"]:checked').map(function(index, option){
			return $(option).val();
		});
	};

	Question.getOptions = function() {
		return $('#question .option input[type="radio"]').map(function(index, option){
			return $(option).val();
		});
	}

	Question.getCorrectOptions = function() {
		return $('#question .correct-option input[type="hidden"]').map(function(index, option){
			return $(option).val();
		});
	}
}());