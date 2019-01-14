const FloatLabel = (() => {

    // add active class and placeholder 
    const handleFocus = (e) => {
        const target = e.target;
        target.parentNode.classList.add('active');
        target.removeAttribute('placeholder');
        var label = target.parentNode.getElementsByTagName("label")[0];
        label.style.display = "inline-block";
    };

    // remove active class and placeholder
    const handleBlur = (e) => {
        const target = e.target;
        if (!target.value) {
            target.parentNode.classList.remove('active');
            var label = target.parentNode.getElementsByTagName("label")[0];
            label.style.display = "none";
        }
        target.setAttribute('placeholder', target.getAttribute('data-placeholder'));
    };

    // register events
    const bindEvents = (element) => {
        const floatField = element.querySelector('input');
        floatField.addEventListener('focus', handleFocus);
        floatField.addEventListener('blur', handleBlur);
        target = floatField;
        if (target.value) {
            var label = target.parentNode.getElementsByTagName("label")[0];
            label.style.display = "inline-block";
        }
        target.setAttribute('placeholder', target.getAttribute('data-placeholder'));
    };

    // get DOM elements
    const init = () => {
        const floatContainers = document.querySelectorAll('.float-container');

        floatContainers.forEach((element) => {
            if (element.querySelector('input').value) {
                element.classList.add('active');
            }

            bindEvents(element);
        });
    };

    return {
        init: init
    };
})();

FloatLabel.init();