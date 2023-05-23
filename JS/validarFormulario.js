const $form = document.querySelector('#form')

$form.addEventListener('submit', handleSubmit)

async function handleSubmit(event){
    event.preventDefault()
    const form =  new FormData(this)
    const reponse = await fetch(this.action,{
        method: this.method,
        body: form,
        header:{
            'Acept':'aplication/json'
        }
    })
    if (reponse.ok){
        this.reset()
        alert('Gracias por contactarte con nosotros, en breve responderemos tu consuta')
    }
}