async function fetchPredictions() {
    try {
        const response = await fetch('/api/camera/predictions');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const videoBox = document.getElementById('Camerabox');
        const predictionElement = document.getElementById('predictionBox');
        const testDiv = document.getElementById('test');

        // 更新預測文字
        

        // 根據預測結果更改邊框顏色
        if (data.class_name === '0 Mask') {
            videoBox.className = 'Video border-mask';
        } else if (data.class_name === '0 NoMask') {
            videoBox.className = 'Video border-nomask';
        } else {
            videoBox.className = 'Video';
        }

        // 當信心分數小於90%時更新test區域
        if (parseFloat(data.confidence_score.replace('%', '')) > 90) {
            predictionElement.innerHTML = `<p>Prediction: ${data.class_name} - Confidence: ${data.confidence_score}</p>`;
        } 
    } catch (error) {
        console.log('Failed to fetch predictions:', error);
        testDiv.innerHTML = '<p>Error fetching predictions.</p>';
    }
}

// 每2秒鐘獲取一次預測結果
setInterval(fetchPredictions, 2000);
