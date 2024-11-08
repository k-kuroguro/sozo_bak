const createEventSource = () => {
   const es = new EventSource('/monitor');

   es.addEventListener('message', function (event) {
      console.log(event.data);
   });
   es.addEventListener('error', function (event) {
      console.log('Error', event);
   });
   es.addEventListener('open', function (event) { });

   return es;
};

es = createEventSource();
