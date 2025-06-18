document.getElementById("Registro").addEventListener("submit", function(event) {
  event.preventDefault(); // Impede o recarregamento da página

  const formData = new FormData(this);
  const data = {
    nome: formData.get("nome"),
    email: formData.get("email"),
    senha: formData.get("senha"),
    csenha: formData.get("csenha")
  };

  fetch("https://potential-bassoon-4jgwrq9xwv53jpvp-5000.app.github.dev/usuarios", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  .then(resp => resp.json())
  .then(json => {
    console.log(json);
    alert(json.mensagem || "Usuário registrado com sucesso!");
  })
  .catch(err => {
    console.error("Erro:", err);
    alert("Erro ao registrar.");
  });
});