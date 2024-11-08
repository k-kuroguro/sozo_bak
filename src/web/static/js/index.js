const createEventSource = () => {
   const es = new EventSource('/monitor');

   es.addEventListener('status_msg', function (event) {
      console.log(event.data);
   });
   es.addEventListener('error_msg', function (event) {
      console.log(event.data);
   });
   es.addEventListener('error', function (event) {
      console.log('Error', event);
   });
   es.addEventListener('open', function (event) { });

   return es;
};

es = createEventSource();
