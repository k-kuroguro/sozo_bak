let reconnectFrequencySeconds = 2;
let reconnectInterval;

const createEventSource = () => {
   let es = new EventSource('/monitor');

   es.addEventListener('message', function (event) {
      console.log(event.data);
   });
   es.addEventListener('error', function (event) {
      console.log('Error', event);
      es.close();
   });
   es.addEventListener('open', function (event) {
      reconnectFrequencySeconds = 2;
      if (reconnectInterval) {
         clearInterval(reconnectInterval);
      }
   });
   window.addEventListener('beforeunload', function () {
      es.close();
      attemptReconnect();
   });

   return es;
};


const attemptReconnect = () => {
   if (es.readyState === 2) {
      es = createEventSource();
      reconnectFrequencySeconds = Math.min(reconnectFrequencySeconds * 2, 64); 
      console.log(reconnectFrequencySeconds);
      restartReconnectInterval();
   }
};

const restartReconnectInterval = () => {
   if (reconnectInterval) {
      clearInterval(reconnectInterval);
   }
   reconnectInterval = setInterval(attemptReconnect, reconnectFrequencySeconds * 1000);
};

es = createEventSource();
attemptReconnect();
