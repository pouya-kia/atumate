const showAlert = document.querySelector('.btn-info-next');
const questionAlert = document.querySelector('.question-alert');
const infoAnswerBtn = document.querySelector('.btn-info-answer');

const clickHandlerAlert = event => {
    questionAlert.classList.remove('d-hide');
    questionAlert.classList.add('d-show');
    infoAnswerBtn.classList.add('d-hide');
}

showAlert.addEventListener('click', clickHandlerAlert);

/////////////////////

const questionAnswerN = document.querySelector('.btn-answer-n');

const questionAnswerNo = event => {
    infoAnswerBtn.classList.remove('d-hide');
    infoAnswerBtn.classList.add('d-show');
    questionAlert.classList.remove('d-show');
    questionAlert.classList.add('d-hide');
}

questionAnswerN.addEventListener('click', questionAnswerNo);

/////////////////////

const secondQuestionAlert = document.querySelector('.second-question-alert');
const questionAnswerY = document.querySelector('.btn-answer-y');

const questionAnswerYes = event => {
    secondQuestionAlert.classList.remove('d-hide');
    secondQuestionAlert.classList.add('d-show');
    questionAlert.classList.remove('d-show');
    questionAlert.classList.add('d-hide');
}

questionAnswerY.addEventListener('click', questionAnswerYes);

/////////////////////

const thirdQuestionAlert = document.querySelector('.third-question-alert');
const btnTrash = document.querySelector('.btn-trash');

const questionAnswerThird = event => {
    secondQuestionAlert.classList.remove('d-show');
    secondQuestionAlert.classList.add('d-hide');
    thirdQuestionAlert.classList.remove('d-hide');
    thirdQuestionAlert.classList.add('d-show');
}

btnTrash.addEventListener('click', questionAnswerThird);

/////////////////////

const fourthQuestionAlert = document.querySelector('.fourth-question-alert');
const questionAnswerThirdN = document.querySelector('.btn-answer-third-n');

const questionAnswerThirdNo = event => {
    thirdQuestionAlert.classList.remove('d-show');
    thirdQuestionAlert.classList.add('d-hide');
    fourthQuestionAlert.classList.remove('d-hide');
    fourthQuestionAlert.classList.add('d-show');
}

questionAnswerThirdN.addEventListener('click', questionAnswerThirdNo);

/////////////////////

const questionAnswerThirdY = document.querySelector('.btn-answer-third-y');

const questionAnswerThirdYes = event => {
    thirdQuestionAlert.classList.remove('d-show');
    thirdQuestionAlert.classList.add('d-hide');
    infoAnswerBtn.classList.remove('d-hide');
    infoAnswerBtn.classList.add('d-show');
}

questionAnswerThirdY.addEventListener('click', questionAnswerThirdYes);
