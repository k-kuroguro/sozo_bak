let reconnectFrequencySeconds = 2;
let reconnectInterval;

const createEventSource = () => {
   let es = new EventSource('/monitor');

   console.log(reconnectFrequencySeconds);

   es.addEventListener('message', function (event) {
      console.log(event.data);
   });
   es.addEventListener('close', function (event) {
      console.log('Connection closed');
   });
   es.addEventListener('error', function (event) {
      console.log('Error', event);
      es.close();
   });
   es.addEventListener('open', function (event) {
      console.log('Connection established');
      reconnectFrequencySeconds = 2; // 接続が確立したら再接続間隔をリセット
   });
   window.addEventListener('beforeunload', function () {
      es.close(); // ウィンドウが閉じられる前に接続をクローズ
   });

   return es;
};


es = createEventSource();

// 再接続の試行を行う関数
const attemptReconnect = () => {
   if (es.readyState === 2) {  // 接続が切れていれば
      es = createEventSource();  // 新しい EventSource を作成
      reconnectFrequencySeconds = Math.min(reconnectFrequencySeconds * 2, 64);  // 再接続間隔を倍増、最大64秒に制限
   }
   console.log(reconnectFrequencySeconds);
   restartReconnectInterval();  // 再接続インターバルを再設定
};

// 再接続インターバルを管理する関数
const restartReconnectInterval = () => {
   if (reconnectInterval) {
      clearInterval(reconnectInterval);  // 既存の interval をクリア
   }
   reconnectInterval = setInterval(attemptReconnect, reconnectFrequencySeconds * 1000);  // 新しい interval を設定
};

// 初期の再接続インターバルの開始
restartReconnectInterval();
