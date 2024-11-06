document.addEventListener("DOMContentLoaded", function () {
   const fetchScore = () => {
      fetch('/concentration_status')
         .then(response => response.json())
         .then(data => {
            document.getElementById('score').innerHTML = `Score: ${data.overall_score}, Sleeping: ${data.sleeping_confidence}`;
         })
         .catch(error => console.error('Error fetching score:', error));
   };
   fetchScore();
   setInterval(fetchScore, 5000);
});
