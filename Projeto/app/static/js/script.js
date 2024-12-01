function handleFileUpload(event) {
    const files = event.target.files;

    if (files.length > 0) {
        // Cria um FormData para enviar a pasta
        const formData = new FormData();

        // Adiciona os arquivos da pasta ao FormData
        for (let i = 0; i < files.length; i++) {
            formData.append('images', files[i]);
        }

        // Envia os arquivos para o backend via POST
        fetch('/upload-folder', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            // Cria um link para download do arquivo zipado
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'predicted_images.zip';
            link.click();
        })
        .catch(error => alert('Erro ao enviar a pasta.'));
    } else {
        alert("Por favor, selecione uma pasta com imagens.");
    }
}
