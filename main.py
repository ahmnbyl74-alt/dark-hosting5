<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لعبة كشف الجاسوس العراقية 🕵️‍♂️</title>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap" rel="stylesheet">
    
    <style>
        * { box-sizing: border-box; font-family: 'Cairo', sans-serif; }
        body {
            background: radial-gradient(circle, #280654, #0b011a);
            display: flex; justify-content: center; align-items: center;
            height: 100vh; margin: 0; overflow: hidden; color: white;
            position: relative;
        }
        
        /* زر كتم الصوت الكرتوني الفاخر */
        .audio-control {
            position: absolute; top: 20px; right: 20px;
            background: #ffca28; border: 3px solid #000; border-radius: 50%;
            width: 50px; height: 50px; font-size: 1.5rem; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            box-shadow: 0 4px 0 #b36600; transition: all 0.1s; z-index: 10;
        }
        .audio-control:active { transform: translateY(3px); box-shadow: 0 1px 0 #b36600; }

        .game-container {
            background: #211063; border: 8px solid #ffca28; border-radius: 30px;
            padding: 25px; width: 95%; max-width: 420px; text-align: center;
            box-shadow: 0 15px 0 #0d0436, 0 25px 15px rgba(0,0,0,0.6);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        h1 {
            color: #ffca28; font-size: 1.9rem; font-weight: 900;
            text-shadow: 3px 3px 0 #e65100, 5px 5px 0 #000; margin: 0 0 15px 0;
        }
        .status-badge {
            background: #ff9800; border: 3px solid #000; padding: 10px;
            border-radius: 15px; font-weight: 900; margin-bottom: 15px;
            text-shadow: 1px 1px 0 #000; box-shadow: 0 5px 0 #b36600;
            animation: pulse 1.5s infinite;
        }
        .cartoon-btn {
            background: #4caf50; color: white; font-size: 1.25rem; font-weight: 900;
            padding: 14px 25px; border: 3px solid #000; border-radius: 20px;
            cursor: pointer; width: 100%; box-shadow: 0 6px 0 #1b5e20;
            transition: all 0.1s ease; text-shadow: 2px 2px 0 #000;
        }
        .cartoon-btn:active {
            transform: translateY(5px); box-shadow: 0 1px 0 #1b5e20;
        }
        input[type="text"] {
            width: 100%; padding: 14px; border: 3px solid #000;
            border-radius: 18px; font-size: 1.05rem; font-weight: 700;
            margin-bottom: 15px; text-align: center; background-color: #fff; color:#000;
        }
        .spy-theme { background: #8e0000 !important; border-color: #ff3d00 !important; box-shadow: 0 15px 0 #4a0000; }
        .detective-theme { background: #003699 !important; border-color: #2979ff !important; box-shadow: 0 15px 0 #001f5c; }
        
        .log-box {
            background: rgba(0, 0, 0, 0.6); border-radius: 20px;
            padding: 15px; height: 180px; overflow-y: auto;
            margin-top: 15px; text-align: right; border: 3px solid #000;
            font-size: 1rem; color: #e0e0e0;
        }
        .chat-input-area { display: flex; gap: 8px; margin-top: 15px; }
        .chat-input-area input { margin: 0; }
        .chat-input-area button { width: 35%; padding: 10px; font-size: 1.1rem; background: #2979ff; box-shadow: 0 5px 0 #0d47a1;}
        .chat-input-area button:active { box-shadow: 0 1px 0 #0d47a1; }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.03); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>

    <button class="audio-control" id="audioBtn" onclick="toggleAudio()">🔊</button>

    <audio id="bgMusic" loop src="https://assets.mixkit.co/active_storage/sfx/123/123.wav"></audio>

    <div class="game-container" id="mainCard">
        <h1 id="gameTitle">السالفة وين؟ 🕵️‍♂️</h1>
        
        <div id="turnBadge" class="status-badge" style="display: none;">انتظر يكتمل اللوبي...</div>
        
        <div id="setupArea">
            <input type="text" id="usernameInput" placeholder="اكتب اسمك هيبة هنا...">
            <button class="cartoon-btn" onclick="joinLobby()">افوت للعبة! 🔥</button>
        </div>

        <div id="roleArea" style="display: none; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 15px; border: 3px dashed #ffca28; margin-bottom: 10px;">
            <p id="roleDisplay" style="margin: 0; font-weight: 700; font-size: 1.1rem; line-height: 1.5;"></p>
        </div>

        <div class="log-box" id="logBox">يا هلا بيك.. سجل اسمك حتى نبلش التحقيق والسوالف!</div>

        <div id="actionArea" class="chat-input-area" style="display: none;">
            <input type="text" id="chatMessage" placeholder="اسأل اللوتي أو جاوب ع السالفة...">
            <button class="cartoon-btn" onclick="sendMessage()">دزّ 🚀</button>
        </div>
    </div>

    <script>
        const socket = io();
        const bgMusic = document.getElementById('bgMusic');
        let isMuted = false;

        // دالة تشغيل صوت كرتوني خفيف للأزرار (Synthesized Sound)
        // المتصفحات تمنع تشغيل الصوت تلقائياً إلا بعد أول ضغطة شاشة للاعب
        function playClickSound() {
            if (isMuted) return;
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(400, ctx.currentTime); // تردد الصوت الكرتوني
            osc.frequency.exponentialRampToValueAtTime(150, ctx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            gain.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.1);
            osc.connect(gain); gain.connect(ctx.destination);
            osc.start(); osc.stop(ctx.currentTime + 0.1);
        }

        // دالة تشغيل صوت بدء اللعبة الحماسي
        function playStartSound() {
            if (isMuted) return;
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(200, ctx.currentTime);
            osc.frequency.linearRampToValueAtTime(600, ctx.currentTime + 0.3);
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.linearRampToValueAtTime(0, ctx.currentTime + 0.3);
            osc.connect(gain); gain.connect(ctx.destination);
            osc.start(); osc.stop(ctx.currentTime + 0.3);
        }

            
            const name = document.getElementById('usernameInput').value.trim();
            if(!name) return alert("صار زحمة بس اكتب اسمك أول شي عيني!");
            socket.emit('join_game', { username: name });
            document.getElementById('setupArea').style.display = 'none';
        }

        socket.on('message', (data) => {
            const logBox = document.getElementById('logBox');
            logBox.innerHTML += `<div style='margin-bottom:6px;'>${data.text}</div>`;
            logBox.scrollTop = logBox.scrollHeight;
        });

        socket.on('game_init', (data) => {
            playStartSound(); // تشغيل الصوت الحماسي لبدء التحقيق!
            document.getElementById('roleArea').style.display = 'block';
            document.getElementById('roleDisplay').innerText = data.role;
            document.getElementById('mainCard').className = "game-container " + data.style;
            document.getElementById('gameTitle').innerText = "منو اللوتي؟ 🔎";
        });

        socket.on('turn_update', (data) => {
            const turnBadge = document.getElementById('turnBadge');
            const actionArea = document.getElementById('actionArea');
            
            turnBadge.style.display = 'block';
            
            if(data.current_player_sid === socket.id) {
                turnBadge.innerText = "🌟 دورك هسة! اسأل لو جاوب ليروحون يصيدوك! 🌟";
                turnBadge.style.background = "#4caf50";
                turnBadge.style.boxShadow = "0 5px 0 #1b5e20";
                actionArea.style.display = 'flex';
            } else {
                turnBadge.innerText = `انكتم وسولف بقلبك.. السرة هسة يم: ${data.current_player_name}`;
                turnBadge.style.background = "#ff9800";
                turnBadge.style.boxShadow = "0 5px 0 #b36600";
                actionArea.style.display = 'none';
            }
        });

        function sendMessage() {
            playClickSound();
            const msgInput = document.getElementById('chatMessage');
            const text = msgInput.value.trim();
            if(!text) return;
            
            socket.emit('send_question', { text: text });
            msgInput.value = "";
        }

        socket.on('error', (data) => { alert(data.message); });
    </script>
</body>
</html>
