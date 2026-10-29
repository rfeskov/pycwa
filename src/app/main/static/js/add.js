const form = document.getElementById('add');

form.addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(form),
        formObject = Object.fromEntries(formData.entries()),
        jsonString = JSON.stringify(formObject);

  const toastError = bootstrap.Toast.getOrCreateInstance(document.getElementById('toastError')),
        toastSuccess = bootstrap.Toast.getOrCreateInstance(document.getElementById('toastSuccess'));

  fetch('/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: jsonString 
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
    if(!data.success) toastError.show();
    else {
      form.reset();
      toastSuccess.show();
    }  
  })
  .catch(error => { console.error(error); });
});