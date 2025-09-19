document.addEventListener('DOMContentLoaded', function () {
    const selectField = document.getElementById('id_check');  // Use the actual field ID

    if (selectField) {
        selectField.addEventListener('change', function (event) {
            console.log("chicked")
            if (selectField.checked){
                title = document.getElementById('id_name').value
                auther = document.getElementById('id_auther').value
                department = document.getElementById('id_department').value
                // console.log({"title":title,"auther":auther,"department":department})
                if (title != "",auther != "Not defined",department != "---"){
                    fetch('http://127.0.0.1:8000/books/predict/', {
                    method: 'POST', // Specify the method as POST
                    headers: {
                        'Content-Type': 'application/json', // Indicate the content type of the body
                        // Add other headers as needed, e.g., 'Authorization': 'Bearer YOUR_TOKEN'
                    },
                    body: JSON.stringify({ // Convert the JavaScript object to a JSON string for the body
                        "title": title,
                        "auther": auther,
                        "department": department
                        // Add your data here
                    })
                    })
                    .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json(); // Parse the JSON response
                    })
                    .then(data => {
                        console.log(data);
                        document.getElementById("id_catagory_display").value = data['subjects'] // Handle the successful response data
                    })
                    .catch(error => {
                    console.error('Error:', error); // Handle any errors during the request
                    });
                console.log({"title":title,"auther":auther,"department":department})

                }
            }
        });
    }
    
});


