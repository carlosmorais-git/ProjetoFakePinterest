document.addEventListener("DOMContentLoaded", function () {
  // ---------------- HOME --------------------------------------------------------//
  const images = document.querySelectorAll("img");

  images.forEach((img) => {
    const carregarImagem = () => {
      img.classList.remove("loaded");
      img.classList.add("loaded");
    };

    if (img.complete) {
      carregarImagem();
    } else {
      img.onload = carregarImagem;
    }
  });

  // ---------------- PERFIL --------------------------------------------------------//

  const input = document.getElementById("foto");
  const imagemArquivo = document.getElementById("imagem-arquivo");
  const form = document.getElementById("form-upload-foto");
  const btnCancelar = document.getElementById("btn-cancelar-escolher");
  const galeriaFotos = document.getElementById("galeria-fotos"); // adicione o id na sua galeria onde estão as fotos
  const bt_postar_imgem = document.getElementById("bt-postar-img");
  const bloco_arquivo = document.getElementById("bloco-arquivo-img");
  if (input) {
    input.addEventListener("change", () => {
      let inputImagem = input.files[0];

      if (inputImagem) {
        imagemArquivo.classList.add("visivel");
        imagemArquivo.innerText = inputImagem.name;

        const reader = new FileReader();
        reader.onload = function (event) {
          imagemArquivo.innerHTML = `<img src="${event.target.result}" alt="Preview" style="width: 120px; height: 120px; border-radius: 10px; margin-top: 10px;">`;
          if (btnCancelar) {
            btnCancelar.style.display = "inline-block";
            bt_postar_imgem.style.display = "inline-block";
            bloco_arquivo.style.display = "none"; // Esconde o botão de escolher arquivo
          }
        };
        reader.readAsDataURL(inputImagem);
      }
    });
  }

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault(); // impede o submit tradicional

      const formData = new FormData(form);
      const uploadUrl = form.dataset.uploadUrl;

      fetch(uploadUrl, {
        method: "POST",
        headers: { "X-Requested-With": "XMLHttpRequest" },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.imagem) {
            exibirMensagemFlash("Foto enviada com sucesso!", "success");

            adicionarNovaImagemNaGaleria(data.imagem);

            // Limpa o formulário e o preview
            imagemArquivo.innerHTML = "";
            form.reset();
            if (btnCancelar) {
              btnCancelar.style.display = "none";
              bt_postar_imgem.style.display = "none";
              bloco_arquivo.style.display = "inline-flex"; // Mostra o botão de escolher arquivo novamente
            }
          } else {
            alert(`Erro ao enviar foto.`);
          }
        })
        .catch((error) => {
          console.error("Erro:", error);
          alert("Erro ao enviar foto.");
        });
    });
  }

  if (btnCancelar) {
    btnCancelar.addEventListener("click", function () {
      imagemArquivo.innerHTML = "";
      form.reset();
      if (btnCancelar) {
        btnCancelar.style.display = "none";
        bt_postar_imgem.style.display = "none";
        bloco_arquivo.style.display = "inline-flex"; // Mostra o botão de escolher arquivo novamente
      }
    });
  }

  function adicionarNovaImagemNaGaleria(urlImagem) {
    if (galeriaFotos) {
      // Cria o bloco principal
      const bloco = document.createElement("div");
      bloco.classList.add("bloco-imagem");

      // Sorteia se terá classe extra como 'grid-row-2'
      const classesPossiveis = ["grid-row-2", "", ""];
      const classeSorteada =
        classesPossiveis[Math.floor(Math.random() * classesPossiveis.length)];
      if (classeSorteada) {
        bloco.classList.add(classeSorteada);
      }

      // Define o atributo 'img-id' usado para exclusão (temporário)
      bloco.setAttribute("img-id", "imagem-nova-temporaria");

      // Cria o HTML interno
      bloco.innerHTML = `
        <div class="acoes-img">
          <a href="#" class="btn-ver" onclick="return false;">Ver</a>
          <a href="#" class="btn-excluir" onclick="return false;">Excluir</a>
        </div>
        <a href="#">
          <img src="${urlImagem}" alt="Nova foto enviada" loading="lazy" />
        </a>
      `;

      // Adiciona no início da galeria
      galeriaFotos.prepend(bloco);

      // Animação de fade-in
      bloco.style.opacity = "0";
      bloco.style.transition = "opacity 0.5s";
      setTimeout(() => {
        bloco.style.opacity = "1";
      }, 50);

      // Aguarda uns segundos depois de mostrar a imagem, e recarrega a página
      setTimeout(() => {
        location.reload();
      }, 1500); // Espera 1,5 segundos antes de recarregar
    }
  }

  // ---------------- FOTOS SALVAS --------------------------------------------------------//
  const botaoMenuSalvos = document.getElementById("botao-menu-salvos");
  if (botaoMenuSalvos) {
    botaoMenuSalvos.addEventListener("click", alternarMenuSalvos);
  }

  window.alternarMenuSalvos = () => {
    const menu = document.getElementById("menu-salvos");
    const icone = document.getElementById("icone-botao");

    menu.classList.toggle("ativo");
    icone.textContent = menu.classList.contains("ativo") ? "✖" : "☰";
    menu.style.display = menu.classList.contains("ativo") ? "block" : "none";
  };

  window.removerSalvo = async function (id) {
    try {
      const resposta = await fetch(`/salvo/${id}/remover`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const resultado = await resposta.json();
      exibirMensagemFlash(resultado.mensagem, resultado.status);

      const blocoImagem = document.querySelector(`[data-salvo-id='${id}']`);
      if (blocoImagem) {
        blocoImagem.remove();
      }
    } catch (erro) {
      console.error("Erro ao remover imagem salva:", erro);
      exibirMensagemFlash("Erro ao remover imagem salva.", "danger");
    }
  };

  // ---------------- MODAL EXCLUIR --------------------------------------------------------//
  let urlExclusaoTemporaria = "";

  window.executarExclusao = function (url) {
    urlExclusaoTemporaria = url;
    document.getElementById("modal-confirmacao").style.display = "flex";
  };

  window.fecharModal = function () {
    document.getElementById("modal-confirmacao").style.display = "none";
  };

  window.confirmarExclusao = async function () {
    try {
      const resposta = await fetch(urlExclusaoTemporaria, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const resultado = await resposta.json();
      exibirMensagemFlash(resultado.mensagem, resultado.status);

      const blocoImagem = document.querySelector(
        `[img-id='${urlExclusaoTemporaria}']`
      );
      if (blocoImagem) blocoImagem.remove();
    } catch (erro) {
      console.error("Erro ao excluir:", erro);
      exibirMensagemFlash("Erro ao remover imagem salva.", "danger");
    }

    fecharModal();
  };

  // ---------------- FLASH --------------------------------------------------------//
  window.salvarImagem = async function (id) {
    const botao = document.getElementById(`btn-salvar-${id}`);

    try {
      const resposta = await fetch(`/foto/${id}/salvar`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const resultado = await resposta.json();

      botao.textContent = resultado.ativo ? "Salvo" : "Salvar";
      botao.classList.toggle("ativo", resultado.ativo);
      botao.dataset.ativo = resultado.ativo.toString();

      exibirMensagemFlash(resultado.mensagem, resultado.status);
    } catch (erro) {
      console.error("Erro ao salvar imagem:", erro);
      exibirMensagemFlash("Erro ao salvar imagem.", "danger");
    }
  };

  window.exibirMensagemFlash = function (texto, tipo) {
    const containerExistente = document.querySelector(".alert");
    if (containerExistente) containerExistente.remove();

    const container = document.createElement("div");
    container.className = `alert alert-${tipo}`;
    container.innerText = texto;
    container.style = `
      position:fixed; top:80px; right:20px; z-index:9999;
      padding:12px 16px; border-radius:8px; color:#fff;
      background:${
        tipo === "success"
          ? "#28a745"
          : tipo === "danger"
          ? "#dc3545"
          : "#17a2b8"
      };
      box-shadow:0 2px 20px rgba(0,0,0,0.20); transition:opacity 0.5s;
      opacity:1; font-size:14px;
    `;
    document.body.appendChild(container);

    setTimeout(() => container.remove(), 3000);
  };
});
