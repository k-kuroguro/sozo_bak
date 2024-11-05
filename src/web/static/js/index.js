document.addEventListener("DOMContentLoaded", function () {
   const fetchScore = () => {
      fetch('/score')
         .then(response => response.json())
         .then(data => {
            document.getElementById('score').innerHTML = `Score: ${data.score}`;
         })
         .catch(error => console.error('Error fetching score:', error));
   };
   fetchScore();
   setInterval(fetchScore, 5000);
});
