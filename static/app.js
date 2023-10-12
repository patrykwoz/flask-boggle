let score = 0
let timer = 60000

$(function(){
    $('#game-finished').remove()
    
    $('#current-score').empty();
    const newScore = $(`<p>Your score is ${score}</p>`)
    $('#current-score').append(newScore);


    $("#user-guess-form").on('submit', handleSubmission);

    setTimeout(()=>{
        $("#user-guess-form").off('submit', handleSubmission);
        $("#user-guess-form").on('submit', prefentDefSubmit);
        console.log('Stoppped listening')
        handleGameEnd()
    }, 60000)
})

function handleSubmission(e){
    e.preventDefault();
    const userGuess = $("#user-guess").val();

    axios.post('/handle-response', {userGuess:userGuess})
        .then(function(response){
            console.log(response.data.result)
            const res = response.data.result
            $('#guess-response').empty();
            $('#current-score').empty();

            if (res === "ok"){
                score += userGuess.length;
                const newResponse = $(`<p class="victory">${userGuess} is ${response.data.result}</p>`)
                $('#guess-response').append(newResponse);
            } else {
                const newResponse = $(`<p class="warning">${userGuess} is ${response.data.result}</p>`)
                $('#guess-response').append(newResponse);
            }
            console.log(score)
            const newScore = $(`<p>Your score is ${score}</p>`)
            $('#current-score').append(newScore);
        })
        .catch(function(error){
            console.log(error)
        })
    e.target.reset()
}

function handleGameEnd(){
    console.log(score)
    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    axios.post('/game-finished', {score:score}, config)
        .then(function(response){
            console.log(response.data.message)
            const message = response.data.message
            const highestScore = response.data.highestscore
            const gameFinished = $(`<div class="game-finished-container" id="game-finished">
            <p>${message}</p>
            <p>You scored in this game: ${score} point(s).</p>
            <p>Your highest score is ${highestScore}.</p>
            <a href="/handle-reset"><button>New Game</button></a>
            </div>`)
            $('body').prepend(gameFinished)
        })
        .catch(function(error){
            console.log(error)
        })

}

function prefentDefSubmit(e){
    e.preventDefault();
}
