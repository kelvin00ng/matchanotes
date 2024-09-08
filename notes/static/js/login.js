$(document).ready(function() {
    var inP = $('.input-field');

    inP.on('blur', function () {
        if (!this.value) {
            $(this).parent('.f_row').removeClass('focus');
        } else {
            $(this).parent('.f_row').addClass('focus');
        }
    }).on('focus', function () {
        $(this).parent('.f_row').addClass('focus');
        $('.btn').removeClass('active');
        $('.f_row').removeClass('shake');
    });

    $('.resetTag').click(function(e) {
        e.preventDefault();
        $('.formBox').addClass('level-forget').removeClass('level-reg');
    });

    $('.back').click(function(e) {
        e.preventDefault();
        $('.formBox').removeClass('level-forget').addClass('level-login');
    });

    $('.regTag').click(function(e) {
        e.preventDefault();
        $('.formBox').removeClass('level-reg-revers');
        $('.formBox').toggleClass('level-login').toggleClass('level-reg');
        if (!$('.formBox').hasClass('level-reg')) {
            $('.formBox').addClass('level-reg-revers');
        }
    });

    $('.btn').each(function() {
        $(this).on('click', function(e) {
            e.preventDefault(); // Prevent default form submission
            
            var form = $(this).closest('form'); // Find the closest form
            var finp = form.find('.input-field'); // Get input fields within the form
            var allFilled = true;

            // Check if all input fields are filled
            finp.each(function() {
                if ($(this).val() === '') {
                    allFilled = false;
                    $(this).parent('.f_row').addClass('shake');
                } else {
                    $(this).parent('.f_row').removeClass('shake');
                }
            });

            if (allFilled) {
                $(this).addClass('active');
                
                // Submit the form if all fields are filled
                form.off('submit').submit();
            } else {
                // Focus on the first empty input field
                finp.filter(function() {
                    return $(this).val() === '';
                }).first().focus();
            }
        });
    });
});
