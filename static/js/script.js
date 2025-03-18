document.getElementById("formRecomendacao").addEventListener("submit", async function(event) {
    event.preventDefault();

    let formData = new FormData(this);
    const file = document.getElementById("pdfExame").files[0];

    const nome = document.getElementById("nome").value;
    formData.append("nome", nome);

    if (file) {
        console.log("PDF selecionado:", file.name);
        formData.append("pdfExame", file);
    }

    try {
        const response = await fetch("/upload_pdf", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Dados recebidos:", data);

            if (data.resultados) {
                document.getElementById("colesterol_total").value = data.resultados.colesterol || '';
                document.getElementById("glicose").value = data.resultados.glicose || '';
                document.getElementById("t3").value = data.resultados.t3 || '';
                document.getElementById("t4").value = data.resultados.t4 || '';
                document.getElementById("tsh").value = data.resultados.tsh || '';
                document.getElementById("triglicerideos").value = data.resultados.triglicerideos || '';

                mostrarRecomendacoes(data.recomendacoes);
            }
        } else {
            console.log("Falha no envio do PDF.");
        }
    } catch (error) {
        console.error("Erro ao enviar o PDF:", error);
    }
});

function mostrarRecomendacoes(recomendacoes) {
    console.log("Recomendações recebidas:", recomendacoes);
    const lista = document.getElementById("listaRecomendacoes");
    lista.innerHTML = "";

    if (recomendacoes) {
        for (const [parametro, avaliacao] of Object.entries(recomendacoes)) {
            const item = document.createElement("li");
            item.innerHTML = `<strong>${parametro}:</strong> <span style="color: ${avaliacao === 'Muito bem! Continue assim.' ? 'green' : 'red'}">${avaliacao}</span>`;
            lista.appendChild(item);
        }
        document.getElementById("recomendacao").style.display = "block"; 
    }
}