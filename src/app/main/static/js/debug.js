const form = document.getElementById('debug'),
      query = document.getElementById('query'),
      query64 = document.getElementById('query64');

form.addEventListener('submit', function (event) {
  event.preventDefault();

  if(!query.value) return;

  query64.value = btoa(query.value);
  
  form.submit();
})