from fastapi.responses import HTMLResponse


def accueil():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>CREDIT SCORING</title>
<style>
  body { font-family: sans-serif; max-width: 700px; margin: 30px auto; padding: 0 15px; }
  h1 { font-size: 22px; }
  label { font-weight: bold; display: block; margin-top: 12px; }
  input { width: 100%; padding: 5px; box-sizing: border-box; }
  button { margin-top: 25px; padding: 12px 24px; font-size: 16px; cursor: pointer; }
  #resultat { margin-top: 20px; font-weight: bold; font-size: 18px; padding: 10px; }
</style>
</head>
<body>

<h1>Simulation de scoring crédit — Prêt à Dépenser</h1>

<form id="scoringForm">
  <label for="sk_id_curr">SK_ID_CURR</label>
  <input type="number" step="1" id="sk_id_curr" name="SK_ID_CURR" value="100002" required>
  <button type="submit">Prédire</button>
</form>

<div id="resultat"></div>

<script>
document.getElementById("scoringForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  const resultDiv = document.getElementById("resultat");
  const id = parseInt(document.getElementById("sk_id_curr").value, 10);

  if (!Number.isInteger(id)) {
    resultDiv.textContent = "Erreur : l'identifiant doit être un entier.";
    return;
  }

  resultDiv.textContent = "Envoi en cours...";

  try {
    const response = await fetch(`/Predict?SK_ID_CURR=${id}`, {
      method: "POST"
    });
    if (!response.ok) throw new Error("Erreur lors de la prédiction (" + response.status + ")");
    const result = await response.json();
    const premier = Array.isArray(result) ? result[0] : result;
    resultDiv.textContent = typeof premier === "object" ? JSON.stringify(premier) : premier;
  } catch (err) {
    resultDiv.textContent = "Erreur : " + err.message;
  }
});
</script>

</body>
</html>
""")