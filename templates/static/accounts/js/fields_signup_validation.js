document.addEventListener('DOMContentLoaded', () => {
    function validateField(
        field,
        feedbackArea,
        apiUrl,
        password_confirm_field = null
    ) {
        field.classList.remove('field-is-invalid');
        field.classList.remove('field-is-valid');
        feedbackArea.style.display = 'none';
        
        console.log('input_password', password_confirm_field);

        field.addEventListener('keyup', (e) => {
            const fieldValue = e.target.value;
    
            if (fieldValue.length > 0) {
                // Remove the classes and hide the feedback area initially
                
        
                
                if (password_confirm_field) {
                    var body = { field_input: fieldValue , confirm_field_input: password_confirm_field.value};
                } else {
                    var body = { field_input: fieldValue };
                };

                fetch(apiUrl, {
                    body: JSON.stringify(body),
                    method: 'POST',
                })
                    .then((res) => res.json())
                    .then((data) => {
                        console.log('data', data);
                        if (data.field_error) {
                            if (!field.classList.contains('field-is-invalid')){
                                field.classList.add('field-is-invalid');
                                feedbackArea.style.display = 'block';
                                feedbackArea.innerHTML = `<p> ${data.field_error} </p>`;
                                field.classList.remove('field-is-valid');
                            }
                        } else {
                            field.classList.remove('field-is-invalid');
                            field.classList.add('field-is-valid');
                            feedbackArea.style.display = 'none';
                        }
                    });
            } else {
                // If the input is empty, remove both classes and hide the feedback area
                field.classList.remove('field-is-invalid');
                field.classList.remove('field-is-valid');
                feedbackArea.style.display = 'none';
            }
        });
    }

    const username_field = document.getElementById('username_field');
    const email_field = document.getElementById('email_field');
    const password_field = document.getElementById('password_field');
    const confirm_password_field = document.getElementById('confirm_password_field');

    const nameFeedBackArea = document.getElementById('username_feedback_error');
    const emailFeedBackArea = document.getElementById('email_feedback_error');
    const confirmPasswordFeedBackArea = document.getElementById('password_confirm_feedback_error');
    const passwordFeedBackArea = document.getElementById('password_feedback_error');

    validateField(username_field, nameFeedBackArea, '/validate_username/');
    validateField(email_field, emailFeedBackArea, '/validate_email/');
    validateField(confirm_password_field, confirmPasswordFeedBackArea,'/validate_password/', password_field);
});