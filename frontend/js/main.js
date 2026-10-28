/* ==========================================================
   AsynLab — main.js
   1. Menu mobile · 2. Link ativo · 3. Ano do rodapé
   4. Formulário (validação + envio preparado para a API)
   ========================================================== */

(function () {
  "use strict";

  /* ---------- 1. MENU MOBILE ---------- */
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("menu-principal");
  const mobileQuery = window.matchMedia("(max-width: 820px)");

  function setMenu(open) {
    toggle.setAttribute("aria-expanded", String(open));
    toggle.querySelector(".visually-hidden").textContent = open ? "Fechar menu" : "Abrir menu";
    nav.classList.toggle("is-open", open);
  }

  // Em telas pequenas o menu fechado fica fora do alcance do teclado (visibility: hidden via CSS).
  toggle.addEventListener("click", function () {
    setMenu(toggle.getAttribute("aria-expanded") !== "true");
  });

  // Fecha ao clicar em qualquer link do menu.
  nav.addEventListener("click", function (event) {
    if (event.target.closest("a")) setMenu(false);
  });

  // Fecha com Esc e devolve o foco ao botão.
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setMenu(false);
      toggle.focus();
    }
  });

  // Fecha ao clicar fora do cabeçalho.
  document.addEventListener("click", function (event) {
    if (!event.target.closest(".site-header")) setMenu(false);
  });

  // Ao voltar para tela grande, garante o estado padrão.
  mobileQuery.addEventListener("change", function () { setMenu(false); });

  /* ---------- 2. LINK ATIVO NO MENU ---------- */
  const navLinks = document.querySelectorAll(".nav-list a:not(.btn)");
  const sections = Array.from(navLinks)
    .map(function (link) { return document.querySelector(link.getAttribute("href")); })
    .filter(Boolean);

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (link) {
          const active = link.getAttribute("href") === "#" + entry.target.id;
          link.classList.toggle("is-active", active);
          if (active) link.setAttribute("aria-current", "true");
          else link.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });

    sections.forEach(function (section) { observer.observe(section); });
  }

  /* ---------- 3. ANO DO RODAPÉ ---------- */
  const year = document.getElementById("ano");
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- 4. FORMULÁRIO ---------- */

  /*
   * ┌────────────────────────────────────────────────────────┐
   * │ INTEGRAÇÃO COM O DJANGO REST FRAMEWORK                 │
   * │ Quando o backend existir, preencha o endereço abaixo,  │
   * │ por exemplo: "https://api.seudominio.com.br/api/leads/"│
   * │ Enquanto estiver vazio, NENHUM dado é enviado e        │
   * │ NENHUMA mensagem de sucesso é exibida.                 │
   * └────────────────────────────────────────────────────────┘
   */
  const API_ENDPOINT = "";

  const SUCCESS_MESSAGE =
    "Solicitação enviada com sucesso! Obrigado pelo interesse na AsynLab. " +
    "Recebemos seus dados e entraremos em contato assim que possível.";

  const form = document.getElementById("form-contato");
  const submitButton = document.getElementById("botao-enviar");
  const statusBox = document.getElementById("form-status");
  let isSubmitting = false; // impede envios duplicados

  const validators = {
    nome: function (value) {
      if (!value) return "Informe seu nome.";
      if (value.length < 3) return "O nome precisa ter pelo menos 3 caracteres.";
      return "";
    },
    email: function (value) {
      if (!value) return "Informe seu e-mail.";
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
        return "Digite um e-mail válido, como nome@exemplo.com.";
      }
      return "";
    },
    whatsapp: function (value) {
      if (!value) return "Informe seu WhatsApp.";
      let digits = value.replace(/\D/g, "");
      if (digits.startsWith("55") && digits.length > 11) digits = digits.slice(2);
      if (digits.length < 10 || digits.length > 11) {
        return "Digite o número com DDD, por exemplo (11) 91234-5678.";
      }
      return "";
    }
  };

  function getField(name) { return form.elements[name]; }

  function showFieldError(name, message) {
    const input = getField(name);
    const wrapper = input.closest(".field");
    const errorBox = document.getElementById(name + "-erro");
    errorBox.textContent = message;
    wrapper.classList.toggle("has-error", Boolean(message));
    if (message) input.setAttribute("aria-invalid", "true");
    else input.removeAttribute("aria-invalid");
  }

  function validateField(name) {
    const message = validators[name](getField(name).value.trim());
    showFieldError(name, message);
    return !message;
  }

  function validateForm() {
    let firstInvalid = null;
    Object.keys(validators).forEach(function (name) {
      if (!validateField(name) && !firstInvalid) firstInvalid = getField(name);
    });
    if (firstInvalid) firstInvalid.focus();
    return !firstInvalid;
  }

  function setStatus(type, message) {
    statusBox.className = "form-status" + (type ? " is-" + type : "");
    statusBox.textContent = message;
  }

  function setLoading(loading) {
    isSubmitting = loading;
    submitButton.disabled = loading;
    submitButton.classList.toggle("is-loading", loading);
    submitButton.setAttribute("aria-busy", String(loading));
    submitButton.querySelector(".btn__label").textContent = loading ? "Enviando" : "Solicitar orçamento";
  }

  // Valida ao sair do campo e limpa o erro enquanto a pessoa corrige.
  Object.keys(validators).forEach(function (name) {
    const input = getField(name);
    input.addEventListener("blur", function () {
      if (input.value.trim() !== "" || input.closest(".field").classList.contains("has-error")) validateField(name);
    });
    input.addEventListener("input", function () {
      if (input.closest(".field").classList.contains("has-error")) validateField(name);
    });
  });

  /**
   * Envia os dados para a API.
   * Só deve resolver (sucesso) se o backend confirmar o salvamento (resposta 2xx).
   */
  async function sendToApi(data) {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(data)
      // Se o Django usar CSRF/CORS específicos, ajuste aqui (credentials, headers).
    });
    if (!response.ok) throw new Error("HTTP " + response.status);
    return response;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    if (isSubmitting) return;

    setStatus("", "");
    if (!validateForm()) return;

    const data = {
      nome: getField("nome").value.trim(),
      email: getField("email").value.trim(),
      whatsapp: getField("whatsapp").value.trim()
    };

    // API ainda não configurada: não envia nada e NÃO alega sucesso.
    if (!API_ENDPOINT) {
      setStatus("info", "O envio do formulário ainda não está disponível. Seus dados não foram enviados. Por enquanto, entre em contato pelo Instagram da AsynLab.");
      statusBox.focus();
      return;
    }

    setLoading(true);
    try {
      await sendToApi(data);
      // Sucesso confirmado pelo backend: só agora a mensagem aparece.
      form.reset();
      Object.keys(validators).forEach(function (name) { showFieldError(name, ""); });
      setStatus("success", SUCCESS_MESSAGE);
    } catch (error) {
      // Mantém os dados digitados para a pessoa tentar de novo.
      setStatus("error", "Não foi possível enviar sua solicitação agora. Seus dados foram mantidos: verifique sua conexão e tente novamente.");
    } finally {
      setLoading(false);
      statusBox.focus();
    }
  });
})();
