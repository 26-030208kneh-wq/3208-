import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기")
st.write("← → 또는 A / D 키로 패들을 움직이세요.")

game = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
    body {
        margin: 0;
        background: transparent;
        font-family: Arial, sans-serif;
    }

    #game-container {
        width: 100%;
        max-width: 800px;
        margin: auto;
    }

    #info {
        display: flex;
        justify-content: space-between;
        color: white;
        background: #111827;
        padding: 12px 20px;
        border-radius: 10px 10px 0 0;
        font-size: 18px;
        font-weight: bold;
    }

    canvas {
        display: block;
        width: 100%;
        background: #0f172a;
        border: 2px solid #334155;
        box-sizing: border-box;
    }

    #buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }

    button {
        flex: 1;
        padding: 12px;
        border: none;
        border-radius: 8px;
        background: #2563eb;
        color: white;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }

    button:hover {
        background: #1d4ed8;
    }

    #message {
        position: absolute;
        left: 50%;
        top: 45%;
        transform: translate(-50%, -50%);
        color: white;
        background: rgba(0,0,0,0.8);
        padding: 25px 40px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        display: none;
    }
</style>
</head>

<body>

<div id="game-container">

    <div id="info">
        <span>점수: <span id="score">0</span></span>
        <span>목숨: <span id="lives">3</span></span>
        <span>레벨: <span id="level">1</span></span>
    </div>

    <canvas id="canvas" width="760" height="520"></canvas>

    <div id="buttons">
        <button onclick="startGame()">게임 시작</button>
        <button onclick="togglePause()">일시정지</button>
        <button onclick="restartGame()">다시 시작</button>
    </div>

</div>

<div id="message"></div>

<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;


// ========================
// 게임 변수
// ========================

let score = 0;
let lives = 3;
let level = 1;

let gameRunning = false;
let paused = false;

let keys = {};


// ========================
// 공
// ========================

let ball = {
    x: WIDTH / 2,
    y: HEIGHT - 80,
    radius: 8,
    dx: 4,
    dy: -5
};


// ========================
// 패들
// ========================

let paddle = {
    width: 120,
    height: 15,
    x: WIDTH / 2 - 60,
    y: HEIGHT - 40,
    speed: 8
};


// ========================
// 벽돌
// ========================

const rows = 6;
const cols = 10;

const brickWidth = 65;
const brickHeight = 22;

const brickPadding = 8;
const brickTop = 60;
const brickLeft = 22;

let bricks = [];


function createBricks() {

    bricks = [];

    for (let row = 0; row < rows; row++) {

        for (let col = 0; col < cols; col++) {

            bricks.push({
                x: brickLeft +
                   col * (brickWidth + brickPadding),

                y: brickTop +
                   row * (brickHeight + brickPadding),

                alive: true
            });

        }
    }
}


// ========================
// 키보드
// ========================

document.addEventListener("keydown", function(e) {

    keys[e.key] = true;

});

document.addEventListener("keyup", function(e) {

    keys[e.key] = false;

});


// ========================
// 공 초기화
// ========================

function resetBall() {

    ball.x = WIDTH / 2;
    ball.y = HEIGHT - 80;

    ball.dx = (Math.random() > 0.5 ? 1 : -1) *
              (4 + level * 0.3);

    ball.dy = -(5 + level * 0.2);

}


// ========================
// 게임 시작
// ========================

function startGame() {

    if (lives <= 0) {
        restartGame();
        return;
    }

    gameRunning = true;
    paused = false;

    hideMessage();

}


// ========================
// 일시정지
// ========================

function togglePause() {

    if (!gameRunning) return;

    paused = !paused;

    if (paused) {

        showMessage("⏸ 일시정지");

    } else {

        hideMessage();

    }

}


// ========================
// 다시 시작
// ========================

function restartGame() {

    score = 0;
    lives = 3;
    level = 1;

    gameRunning = false;
    paused = false;

    paddle.x = WIDTH / 2 - paddle.width / 2;

    createBricks();
    resetBall();

    updateUI();

    showMessage("🧱 벽돌깨기<br><small>게임 시작 버튼을 눌러주세요</small>");

}


// ========================
// UI
// ========================

function updateUI() {

    document.getElementById("score").textContent = score;
    document.getElementById("lives").textContent = lives;
    document.getElementById("level").textContent = level;

}


function showMessage(text) {

    const message = document.getElementById("message");

    message.innerHTML = text;
    message.style.display = "block";

}


function hideMessage() {

    document.getElementById("message").style.display = "none";

}


// ========================
// 패들
// ========================

function updatePaddle() {

    if (keys["ArrowLeft"] || keys["a"] || keys["A"]) {

        paddle.x -= paddle.speed;

    }

    if (keys["ArrowRight"] || keys["d"] || keys["D"]) {

        paddle.x += paddle.speed;

    }


    if (paddle.x < 0) {

        paddle.x = 0;

    }

    if (paddle.x + paddle.width > WIDTH) {

        paddle.x = WIDTH - paddle.width;

    }

}


// ========================
// 공 움직이기
// ========================

function updateBall() {

    ball.x += ball.dx;
    ball.y += ball.dy;


    // 왼쪽 / 오른쪽 벽

    if (
        ball.x - ball.radius <= 0 ||
        ball.x + ball.radius >= WIDTH
    ) {

        ball.dx *= -1;

    }


    // 위쪽 벽

    if (ball.y - ball.radius <= 0) {

        ball.dy *= -1;

    }


    // 패들 충돌

    if (
        ball.y + ball.radius >= paddle.y &&
        ball.y - ball.radius <= paddle.y + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width &&
        ball.dy > 0
    ) {

        let hitPosition =
            (ball.x - paddle.x) /
            paddle.width;

        ball.dx =
            (hitPosition - 0.5) * 10;

        ball.dy = -Math.abs(ball.dy);

    }


    // 바닥

    if (ball.y > HEIGHT + ball.radius) {

        loseLife();

    }


    // 벽돌 충돌

    for (let brick of bricks) {

        if (!brick.alive) continue;


        if (
            ball.x + ball.radius > brick.x &&
            ball.x - ball.radius <
                brick.x + brickWidth &&
            ball.y + ball.radius > brick.y &&
            ball.y - ball.radius <
                brick.y + brickHeight
        ) {

            brick.alive = false;

            ball.dy *= -1;

            score += 10;

            updateUI();

            break;

        }

    }


    // 모든 벽돌 제거

    if (bricks.every(brick => !brick.alive)) {

        nextLevel();

    }

}


// ========================
// 목숨 감소
// ========================

function loseLife() {

    lives--;

    updateUI();

    if (lives <= 0) {

        gameRunning = false;

        showMessage(
            "💀 GAME OVER<br>" +
            "<small>다시 시작을 눌러주세요</small>"
        );

        return;

    }


    resetBall();

}


// ========================
// 다음 레벨
// ========================

function nextLevel() {

    level++;

    createBricks();
    resetBall();

    updateUI();

}


// ========================
// 그리기
// ========================

function draw() {

    ctx.clearRect(
        0,
        0,
        WIDTH,
        HEIGHT
    );


    // 배경

    ctx.fillStyle = "#0f172a";

    ctx.fillRect(
        0,
        0,
        WIDTH,
        HEIGHT
    );


    // 벽돌

    for (let brick of bricks) {

        if (!brick.alive) continue;

        ctx.fillStyle = "#ef4444";

        ctx.beginPath();

        ctx.roundRect(
            brick.x,
            brick.y,
            brickWidth,
            brickHeight,
            5
        );

        ctx.fill();

    }


    // 패들

    ctx.fillStyle = "#38bdf8";

    ctx.beginPath();

    ctx.roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        8
    );

    ctx.fill();


    // 공

    ctx.fillStyle = "#facc15";

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fill();

}


// ========================
// 게임 루프
// ========================

function gameLoop() {

    if (gameRunning && !paused) {

        updatePaddle();
        updateBall();

    }

    draw();

    requestAnimationFrame(gameLoop);

}


// ========================
// 초기화
// ========================

createBricks();
resetBall();
updateUI();

showMessage(
    "🧱 벽돌깨기<br>" +
    "<small>게임 시작 버튼을 눌러주세요</small>"
);

gameLoop();

</script>

</body>
</html>
"""

components.html(game, height=650, scrolling=False)
