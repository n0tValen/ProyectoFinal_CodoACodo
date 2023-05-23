var form = document.getElementById('form')

async function handleSubmit(event) {
    event.preventDefault();
    const $form = new FormData(this)
    const response = await fetch(this.action, {
        method: this.method,
        body: $form,
        headers: {
            'Accept': 'application/json'
        }
    })
    if (response.ok) {
        this.reset()
        alert('Gracias por contactarte, en breve responderemos tu consuta')
    }

}

form.addEventListener('submit', handleSubmit)