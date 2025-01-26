let raspberryPiIp = '';
let serverIp = '';

function updateIps() {
    raspberryPiIp = document.getElementById('raspberryPiIp').value;
    serverIp = document.getElementById('serverIp').value;

    document.getElementById('cameraImage').src = `http://${raspberryPiIp}:5000/video_feed`;

    // 設置樹莓派IP地址到Flask服務器通過ASP.NET
    fetch('/api/camera/set_raspberry_pi_ip', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ RaspberryPiIp: raspberryPiIp, FlaskIp: serverIp })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Camera IP set successfully');
            } else {
                console.error('Failed to set camera IP:', data.message);
            }
        })
        .catch(error => {
            console.error('Error setting camera IP:', error);
        });

    fetchPredictions();
}

async function fetchPredictions() {
    try {
        const response = await fetch(`/api/camera/predictions?ip=${serverIp}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const videoBox = document.getElementById('Camerabox');
        const predictionElement = document.getElementById('predictionBox');

        // 更新預測文字和邊框顏色
        const confidenceScore = parseFloat(data.confidence_score.replace('%', ''));
        if (confidenceScore < 70) {
            data.class_name = 'NoMask';
        }

        if (data.class_name === 'Mask') {
            videoBox.className = 'Video border-mask';
        } else if (data.class_name === 'NoMask') {
            videoBox.className = 'Video border-nomask';
        } else {
            videoBox.className = 'Video';
        }

        if (confidenceScore > 20) {
            predictionElement.innerHTML = `<p>Prediction: ${data.class_name} - Confidence: ${data.confidence_score}</p>`;
        }
        //else {
        //    predictionElement.innerHTML = `<p>Prediction: Low Confidence</p>`;
        //}
    } catch (error) {
        console.log('Failed to fetch predictions:', error);
        const predictionElement = document.getElementById('predictionBox');
        predictionElement.innerHTML = '<p>Error fetching predictions.</p>';
    }
}

// 每2秒鐘獲取一次預測結果
setInterval(fetchPredictions, 1000);
