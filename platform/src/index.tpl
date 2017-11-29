<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/static/lib/chessboardjs/css/chessboard-0.3.0.css">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
<div id="board" class="board"></div>
<div class="info">
    <span>Time: <span id="time"></span></span>
    <br>
    <div id="move-history" class="move-history">
    </div>
</div>
<script src="/static/lib/jquery/jquery-3.2.1.min.js"></script>
<script src="/static/lib/chessboardjs/js/chess.js"></script>
<script src="/static/lib/chessboardjs/js/chessboard-0.3.0.min.js"></script>
<script>
var stu_id = {{ stu_id }};
var board,
    game = new Chess();


var onDragStart = function (source, piece, position, orientation) {
    if (game.in_checkmate() === true || game.in_draw() === true ||
        piece.search(/^b/) !== -1) {
        return false;
    }
};

var makeBestMove = function () {
    var bestMove = getBestMove(game);
    game.move(bestMove, { sloppy: true });
    board.position(game.fen());
    renderMoveHistory(game.history());
    if (game.game_over()) {
        alert('Game over');
    }
};


var positionCount;
var getBestMove = function (game) {
    if (game.game_over()) {
        alert('Game over');
    }
    var uci;

    var d = new Date().getTime();
    $.post( {
       url: 'http://10.141.209.144:54321/api/movement', 
       headers: { 'Content-Type': 'application/json' },
       data: JSON.stringify({ 'stu_id': stu_id, 'fen': game.fen() }),
       success: function(data) {uci = data; },
       async: false
    } );
    var d2 = new Date().getTime();
    var moveTime = (d2 - d);

    $('#time').text(moveTime/1000 + 's');
    return uci
};

var renderMoveHistory = function (moves) {
    var historyElement = $('#move-history').empty();
    historyElement.empty();
    for (var i = 0; i < moves.length; i = i + 2) {
        historyElement.append('<span>' + moves[i] + ' ' + ( moves[i + 1] ? moves[i + 1] : ' ') + '</span><br>')
    }
    historyElement.scrollTop(historyElement[0].scrollHeight);

};

var onDrop = function (source, target) {

    var move = game.move({
        from: source,
        to: target,
        promotion: 'q'
    });

    removeGreySquares();
    if (move === null) {
        return 'snapback';
    }

    renderMoveHistory(game.history());
    window.setTimeout(makeBestMove, 250);
};

var onSnapEnd = function () {
    board.position(game.fen());
};

var onMouseoverSquare = function(square, piece) {
    var moves = game.moves({
        square: square,
        verbose: true
    });

    if (moves.length === 0) return;

    greySquare(square);

    for (var i = 0; i < moves.length; i++) {
        greySquare(moves[i].to);
    }
};

var onMouseoutSquare = function(square, piece) {
    removeGreySquares();
};

var removeGreySquares = function() {
    $('#board .square-55d63').css('background', '');
};

var greySquare = function(square) {
    var squareEl = $('#board .square-' + square);

    var background = '#a9a9a9';
    if (squareEl.hasClass('black-3c85d') === true) {
        background = '#696969';
    }

    squareEl.css('background', background);
};

var cfg = {
    draggable: true,
    position: 'start',
    onDragStart: onDragStart,
    onDrop: onDrop,
    onMouseoutSquare: onMouseoutSquare,
    onMouseoverSquare: onMouseoverSquare,
    onSnapEnd: onSnapEnd
};
board = ChessBoard('board', cfg);
</script>
<script>

</script>
</body>
</html>
