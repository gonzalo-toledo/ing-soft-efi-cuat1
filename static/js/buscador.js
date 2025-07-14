document.addEventListener('DOMContentLoaded', function () {
    // Set default date to tomorrow
    const fechaInput = document.getElementById('fecha');
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    fechaInput.value = tomorrow.toISOString().split('T')[0];

    // Tom Select para origen
    new TomSelect('#origen', {
        create: false,
        highlight: true,
        maxOptions: 10,
        loadingClass: 'is-loading',
        score: function (search) {
            return function (item) {
                return item.text.toLowerCase().includes(search.toLowerCase()) ? 1 : 0;
            };
        }
    });

    // Tom Select para destino
    new TomSelect('#destino', {
        create: false,
        highlight: true,
        maxOptions: 10,
        loadingClass: 'is-loading',
        score: function (search) {
            return function (item) {
                return item.text.toLowerCase().includes(search.toLowerCase()) ? 1 : 0;
            };
        }
    });

    // Validación visual rápida (opcional, para mejorar UX)
    const form = document.getElementById('form-busqueda');
    form.addEventListener('submit', function (e) {
        const origen = document.getElementById('origen').value;
        const destino = document.getElementById('destino').value;
        const fecha = fechaInput.value;
        const hoy = new Date().toISOString().split('T')[0];

        if (origen === destino && origen !== '') {
            alert("El origen y destino no pueden ser iguales.");
            // No cancelamos el envío, dejamos que el backend maneje también.
            //para cancelar el envio:
            //e.preventDefault();
            //return
        }

        if (fecha < hoy) {
            alert("La fecha no puede ser anterior a hoy.");
            // No cancelamos el envío, dejamos que el backend maneje también
            //para cancelar el envio:
            //e.preventDefault();
            //return


        }
    });
});