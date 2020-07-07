(function($) {
    $(function() {
        var selectField = $('#id_discharged_date_1'),
            explanation  = $('.field-discharged_explanation');
        console.log("hello world")
        function toggleExplanation(value) {
            console.log(value, "value")
            if (value) {
                explanation.show();
            } else {
                explanation.hide();
            }
        }

        // show/hide on load based on previous value of selectField
        toggleExplanation(selectField.val());

        // show/hide on change
        selectField.change(function() {
            toggleExplanation($(this).val());
        });

    });
})(django.jQuery);