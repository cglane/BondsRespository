(function($) {
    $(function() {
        var selectField = $('#id_discharged_date_1'),
            explanation  = $('.field-discharged_explanation');

        function toggleExplanation(value) {
            if (value) {
                explanation.show();
            } else {
                explanation.hide();
            }
        }

        // show/hide on load based on pervious value of selectField
        toggleExplanation(selectField.val());

        // show/hide on change
        selectField.change(function() {
            toggleExplanation($(this).val());
        });
    });
})(django.jQuery);