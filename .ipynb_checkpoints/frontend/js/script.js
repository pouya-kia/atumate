var btnLangE = document.querySelector('.btn-lang-item-E');
var btnLangF = document.querySelector('.btn-lang-item-F');

const clickHandlerE = event => {
    btnLangE.classList.add('lang-active');
    btnLangF.classList.remove('lang-active');
}

btnLangE.addEventListener('click', clickHandlerE);

///////////////////////

const clickHandlerF = event => {
    btnLangF.classList.add('lang-active');
    btnLangE.classList.remove('lang-active');
}

btnLangF.addEventListener('click', clickHandlerF);

///////////////////////

var btnUp = document.querySelector('.btn-item-up');
var btnIn = document.querySelector('.btn-item-in');

const hoverUpBtn = event => {
    btnIn.classList.add('mark');
}

btnUp.addEventListener('mouseover', hoverUpBtn);

const mouseoutUpBtn = event => {
    btnIn.classList.remove('mark');
}

btnUp.addEventListener('mouseout', mouseoutUpBtn);

////////////////////////////////

let uploadedDataJson = null;

document.getElementById('fileInput').addEventListener('change', function () {
  const file = this.files[0];
  const fileNameDisplay = document.getElementById('fileName');
  const progressBar = document.getElementById('progressBar');
  const progressContainer = document.querySelector('.progress-container');
  const showArrow = document.querySelector('.arrow');
  const showBtnArrow = document.querySelector('.btn-arrow');

  if (!file) return;

  fileNameDisplay.textContent = file.name;
  progressContainer.style.display = "block";
  let progress = 0;

  const interval = setInterval(() => {
    if (progress >= 100) {
      clearInterval(interval);
      showArrow.classList.remove('d-hide');
      showArrow.classList.add('d-show');
      showBtnArrow.classList.remove('d-hide');
      showBtnArrow.classList.add('d-show');
      progressContainer.classList.add('d-hide');
    } else {
      progress += 10;
      progressBar.style.width = progress + "%";
    }
  }, 500);

  // ✅ Convert CSV to JSON
  const reader = new FileReader();
  reader.onload = function (e) {
    const csv = e.target.result;
    const lines = csv.split("\n").filter(line => line.trim() !== "");
    const headers = lines[0].split(",");

    const jsonData = [];

    for (let i = 1; i < lines.length; i++) {
      const obj = {};
      const currentLine = lines[i].split(",");

      if (currentLine.length === headers.length) {
        headers.forEach((header, index) => {
          obj[header.trim()] = currentLine[index].trim();
        });
        jsonData.push(obj);
      }
    }

    uploadedDataJson = JSON.stringify(jsonData);
    console.log("✅ File converted to JSON:", uploadedDataJson);
    alert("✅ File successfully loaded and converted to JSON!");
  };

  reader.readAsText(file);
});

/////////////////////////////////////

window.addEventListener('resize', function () {
    if (window.innerWidth <= 992) {
        document.querySelector('about').id("About-sub");
    }
});

/////////////////////////////////////

// ✅ Submit JSON + config to API
document.getElementById("submitToAPI").addEventListener("click", function () {
  if (!uploadedDataJson) {
    alert("⛔️ Please upload a file first.");
    return;
  }

  const config = {
    drop_columns: ["id"],
    encoding: ["gender"],
    model: {
      mode: "supervised",
      type: "logistic",
      target: "target",
      scaler: "standard"
    }
  };

  fetch("http://127.0.0.1:8000/api/run-pipeline", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      data: uploadedDataJson,
      config: config
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log("✅ API Response:", result);
      alert("✅ Pipeline executed! Check console for details.");
    })
    .catch(error => {
      console.error("❌ Error calling API:", error);
      alert("❌ Failed to call pipeline API.");
    });
});
