import base64
import os
import streamlit as st


def get_image_base64(path):
  if os.path.exists(path):
    with open(path, "rb") as f:
      encoded = base64.b64encode(f.read()).decode("utf-8")
      ext = path.split(".")[-1].lower()
      mime = "image/png" if ext == "png" else "image/jpeg"
      return f"data:{mime};base64,{encoded}"
  return ""


player_b64 = get_image_base64("player.png")
monster_b64 = get_image_base64("monster.png")
bg_b64 = get_image_base64("background.png")

st.set_page_config(
    page_title="Trò Chơi Chạy Trốn Quái Vật - CORTIS REDRED",
    page_icon="🎵",
    layout="centered",
)

st.title("🏃‍♂️ Trò Chơi: Chạy Trốn Quái Vật (Nhạc CORTIS - REDRED)")
st.markdown("Vừa chạy né vật cản, vừa thưởng thức giai điệu cuốn hút từ CORTIS!")

game_html = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Temple Run Game</title>
    <style>
        body {{
            background-color: #0e1117;
            color: white;
            text-align: center;
            font-family: sans-serif;
            margin: 0;
            padding: 0;
        }}
        canvas {{
            background: #222;
            display: block;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
        }}
        .controls {{
            margin-top: 15px;
        }}
        .btn {{
            background-color: #ff4b4b;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            margin: 0 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
        .btn:active {{
            background-color: #ff2222;
            transform: translateY(2px);
        }}
    </style>
</head>
<body>

    <!-- Nhạc nền bài hát REDRED của CORTIS -->
    <audio id="bgMusic" loop>
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3">
    </audio>

    <canvas id="gameCanvas" width="600" height="400"></canvas>
    
    <div class="controls">
        <button class="btn" onclick="moveLeft()">◀ Trái</button>
        <button class="btn" onclick="moveRight()">Phải ▶</button>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const bgMusic = document.getElementById("bgMusic");

        const playerImg = new Image();
        playerImg.src = "{player_b64}";

        const monsterImg = new Image();
        monsterImg.src = "{monster_b64}";

        const bgImg = new Image();
        bgImg.src = "{bg_b64}";

        let score = 0;
        let gameOver = false;
        let gameStarted = false;

        const lanes = [150, 300, 450];
        let playerLane = 1; 
        let playerX = lanes[playerLane];
        let playerY = 300;

        let monsterX = 300;
        let monsterY = 330;

        let obstacles = [];
        let frameCount = 0;

        window.addEventListener("keydown", function(e) {{
            if (!gameStarted && (e.code === "Space" || e.code === "ArrowUp")) {{
                startGame();
                return;
            }}
            if (gameOver && e.code === "Space") {{
                startGame();
                return;
            }}
            if (!gameOver && gameStarted) {{
                if (e.code === "ArrowLeft" || e.code === "KeyA") {{
                    moveLeft();
                }}
                if (e.code === "ArrowRight" || e.code === "KeyD") {{
                    moveRight();
                }}
            }}
        }});

        function startGame() {{
            gameStarted = true;
            resetGame();
            bgMusic.play().catch(e => console.log("Audio play blocked"));
        }}

        function moveLeft() {{
            if (playerLane > 0) playerLane--;
        }}

        function moveRight() {{
            if (playerLane < lanes.length - 1) playerLane++;
        }}

        function resetGame() {{
            score = 0;
            gameOver = false;
            obstacles = [];
            playerLane = 1;
            gameStarted = true;
            bgMusic.currentTime = 0;
            bgMusic.play().catch(e => console.log("Audio play blocked"));
        }}

        function update() {{
            if (!gameStarted || gameOver) return;

            let targetX = lanes[playerLane];
            playerX += (targetX - playerX) * 0.2;

            frameCount++;
            if (frameCount % 90 === 0) {{
                let lane = Math.floor(Math.random() * 3);
                obstacles.push({{ lane: lane, y: -50, passed: false }});
            }}

            for (let i = obstacles.length - 1; i >= 0; i--) {{
                obstacles[i].y += 4; 

                let obsX = lanes[obstacles[i].lane];
                let obsY = obstacles[i].y;

                if (Math.abs(playerX - obsX) < 30 && Math.abs(playerY - obsY) < 40) {{
                    gameOver = true;
                    bgMusic.pause();
                }}

                if (obstacles[i].y > playerY && !obstacles[i].passed) {{
                    score += 10;
                    obstacles[i].passed = true;
                }}

                if (obstacles[i].y > 450) {{
                    obstacles.splice(i, 1);
                }}
            }}
        }}

        function draw() {{
            if (bgImg.complete && bgImg.naturalWidth !== 0) {{
                ctx.drawImage(bgImg, 0, 0, canvas.width, canvas.height);
            }} else {{
                ctx.fillStyle = "#555";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }}

            if (!gameStarted) {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "white";
                ctx.font = "28px Arial";
                ctx.textAlign = "center";
                ctx.fillText("CHẠY TRỐN QUÁI VẬT", canvas.width / 2, 160);
                ctx.font = "18px Arial";
                ctx.fillText("Nhấn phím Cách (Space) để Bắt đầu", canvas.width / 2, 220);
                return;
            }}

            for (let obs of obstacles) {{
                let ox = lanes[obs.lane];
                let oy = obs.y;
                ctx.fillStyle = "#888";
                ctx.beginPath();
                ctx.arc(ox, oy, 25, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#fff";
                ctx.lineWidth = 2;
                ctx.stroke();
            }}

            if (playerImg.complete && playerImg.naturalWidth !== 0) {{
                ctx.drawImage(playerImg, playerX - 30, playerY - 40, 60, 60);
            }} else {{
                ctx.fillStyle = "blue";
                ctx.fillRect(playerX - 20, playerY - 30, 40, 50);
            }}

            if (monsterImg.complete && monsterImg.naturalWidth !== 0) {{
                ctx.drawImage(monsterImg, monsterX - 40, monsterY - 20, 80, 70);
            }} else {{
                ctx.fillStyle = "pink";
                ctx.fillRect(monsterX - 25, monsterY - 20, 50, 50);
            }}

            ctx.fillStyle = "white";
            ctx.font = "20px Arial";
            ctx.textAlign = "left";
            ctx.fillText("Điểm: " + score, 20, 30);

            if (gameOver) {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#ff4b4b";
                ctx.font = "36px Arial";
                ctx.textAlign = "center";
                ctx.fillText("BẠN ĐÃ BỊ HEO PEPPA ĂN THỊT!", canvas.width / 2, 160);
                ctx.fillStyle = "white";
                ctx.font = "20px Arial";
ctx.fillText("BẠN ĐÃ BỊ HEO PEPPA ĂN THỊT!", canvas.width / 2, 160);
                ctx.fillStyle = "white";
                ctx.font = "20px Arial";
                ctx.fillText("Điểm số: " + score, canvas.width / 2, 210);
                ctx.fillText("Nhấn phím Cách (Space) để Chơi lại", canvas.width / 2, 260);
            }}
        }}

        function loop() {{
            update();
            draw();
            requestAnimationFrame(loop);
        }}

        loop();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=500)
