import { lerMotivo } from "../utils/storage.js";

const detalhe = lerMotivo();
const elemento = document.getElementById("motivo-detalhe");

if (elemento && detalhe) elemento.textContent = detalhe;
